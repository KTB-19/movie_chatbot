#%%
# 필요 의존성 설치
# !pip install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'
# !pip install langchain
# !pip install transformers
# !pip install sentence-transformers
# !pip install faiss-cpu
# !pip install -q langchain langchain-community
# !pip install langchain_openai
# !pip install python-Levenshtein
# !pip install transformers datasets torch
# !pip install jamo
# !pip install konlpy
from turtledemo.penrose import start

from kobert_tokenizer import KoBERTTokenizer
import torch
from transformers import BertModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import json
from datetime import datetime
import pytz
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import Levenshtein
from jamo import h2j, j2h, j2hcj
from konlpy.tag import Okt
# import jpype
#
# jvm_path = "/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home/lib/libjli.dylib"
# if not jpype.isJVMStarted():
#     print("jpype start")
#     jpype.startJVM(jvm_path)

# KoBERT 토크나이저와 모델 초기화
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
model = BertModel.from_pretrained('skt/kobert-base-v1')

class KoBERTEmbeddings(HuggingFaceEmbeddings):
    def embed_documents(self, documents):
        embeddings = []
        for doc in documents:
            inputs = tokenizer(doc, return_tensors="pt", padding=True, truncation=True, max_length=512)
            with torch.no_grad():
                outputs = model(**inputs)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy())
        return embeddings

# FAISS 벡터화 함수
def FAISS_vectorize_documents(documents, embeddings_model):
    print("FAISS_vectorize_documents start")
    vector_store = FAISS.from_texts(documents, embedding=embeddings_model)
    return vector_store

# 쿼리 임베딩 함수
def query_embedding(query, k, embeddings_model, vector_store):
    query_embedded = embeddings_model.embed_documents([query])[0]
    results1 = vector_store.similarity_search_by_vector(query_embedded, k=k)
    results2 = vector_store.max_marginal_relevance_search_by_vector(query_embedded, k=k)
    #results3 = vector_store.search_by_vector(query_embedded, k=k)
    return results1, results2#, results3

# 문서 포맷팅 함수
def format_docs(docs):
    return '\n'.join([f'"{d.page_content}"' for d in docs])

#%%
# 한글을 자모로 변환하는 함수
def hangul_to_jamo(text):
    return ''.join(j2hcj(h2j(text)))

# 자모를 한글로 변환하는 함수
def jamo_to_hangul(jamo_text):
    return j2h(jamo_text)

# 문서들을 자모 사전으로 변환하는 함수
def documents_to_jamodict(documents):
    okt = Okt()
    jamodict = {}
    for doc in documents:
        docnouns = [""]  # 첫 번째 항목은 모든 명사를 합친 문자열
        for noun in okt.nouns(doc):
            jamo_noun = hangul_to_jamo(noun)
            docnouns[0] += jamo_noun
            docnouns.append(jamo_noun)
        jamodict[doc] = docnouns
    return jamodict

# 자모 사전을 검색하여 레벤슈타인 거리가 가장 가까운 결과를 반환하는 함수
def jamodict_search(query, jamodict):
    jamo_query = hangul_to_jamo(query)
    distance_list = []

    for k, v in jamodict.items():
        k_distance = Levenshtein.distance(hangul_to_jamo(k), jamo_query)
        v_distances = [Levenshtein.distance(jamo, jamo_query) for jamo in v]
        distance_list.append([k, k_distance, v_distances])

    sorted_distance_list = sorted(distance_list, key=lambda x: min(x[2]))
    return sorted_distance_list

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY1')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# 메인 함수
def process_documents_and_question(documents, question):
    # 한국 시간대 설정
    kst = pytz.timezone('Asia/Seoul')
    utc_now = datetime.now(pytz.utc)
    kst_now = utc_now.astimezone(kst)
    today = kst_now.strftime('%m/%d')
    weekday = kst_now.strftime('%A')

    # LLM 초기화
    llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.3, max_tokens=200)

    # LLMChain 설정
    template1 = '''너는 영화 예매를 도와주는 챗봇이야. 영화 이름, 날짜, 시간, 장소를 구분하는 역할을 수행해.
    context는 상영중인 영화 리스트이다.
    context:{context}
    영화 이름은 현재 상영중인 영화 리스트에서 구분한다.
    또는 {question} 와 유사한 이름의 영화가 상영중인 영화 리스트에 있다면 영화이름을 리스트에 있는 이름으로 대체하고 similar에는 상영중인 영화 리스트에서 이름 넣는다.
    만약 없다면 null로 넣는다.
    오늘 날짜는 {today}이고 요일은 {weekday}다.
    만약 요일만 있다면 이번주로 계산한다.
    Question: {question}문장 안에 영화 이름, 장소, 날짜, 시간이 포함되어 있는지 확인해 줘.
    영화는 movie : , 장소는 region: , 날짜는 date: , 시간은 time: , 문장에서 찾은 영화 이름은 Original:에 대입해줘, context와  유사한 이름 상영중인 영화이름은 Similar: 이라고 알려줘.
     빈 항목은 null를 채워서 마지막 줄에있는 출력형식으로만 대답해줘
    {{"movieName" : null, "region": null, "date": null, "time": null, "original": null, "similar": null}}
    '''

    template2 = '''
    "context 는 현재 상영중인 영화 리스트 : {context}"
    "대답은 무조건 context 리스트 안에서 대답한다."
    "context에 있는{movie}와 비슷한 이름을 movieName에 지정한다."
    "{movie}은 original로 지정한다."
    Question: {movie} 는 영화 이름의 일부분이다. {movie} 를 포함거나 유사한 영화 이름이 context에 포함되어 있는지 확인하여 채운다,
    없는 경우는 빈 항목으로 null를 채워서 마지막 줄에있는 출력형식으로만 대답해줘"
     {{"movieName" : null, "original": null}}
    '''

    prompt1 = ChatPromptTemplate.from_template(template1)
    prompt2 = ChatPromptTemplate.from_template(template2)

    chain1 = prompt1 | llm | StrOutputParser()
    chain2 = prompt2 | llm | StrOutputParser()

    # 임베딩 모델 초기화 및 벡터화
    embeddings_model = KoBERTEmbeddings()
    vector_store = FAISS_vectorize_documents(documents, embeddings_model)
    jamodict = documents_to_jamodict(documents)
    # 쿼리 임베딩 및 첫 번째 LLM 호출
    query_results = query_embedding(question, k=5, embeddings_model=embeddings_model, vector_store=vector_store)
    response1 = chain1.invoke({
        'context': format_docs(query_results[1]),
        'question': question,
        'today': today,
        'weekday': weekday
    })
    print("response1 : " + response1)

    responseDict = json.loads(response1)
    print("responseDict : " + responseDict)

    if responseDict["similar"] is None:
        movieNameQuery = jamodict_search(responseDict["movieName"],jamodict)
        response2 = chain2.invoke({
            'context': movieNameQuery,
            'movie': responseDict["movieName"]
        })
        responseReDict = json.loads(response2)
        responseDict["original"] = responseDict["movieName"]
        responseDict["similar"] = responseReDict["movieName"]
        responseDict["movieName"] = responseReDict["movieName"]
    elif responseDict["similar"] and responseDict["movieName"] is None:
        jamoQuestion = jamodict_search(question,jamodict)
        response2 = chain2.invoke({
            'context': jamoQuestion,
            'movie': question
        })
        responseReDict = json.loads(response2)
        responseDict["original"] = responseDict["movieName"]
        responseDict["similar"] = responseReDict["movieName"]
        responseDict["movieName"] = responseReDict["movieName"]
    return json.dumps(responseDict)