import sys
import os
import pickle
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import openai

from app.services.embeddings import KoBERTEmbeddings, query_embedding, format_docs, jamodict_search, format_dict, rename_dict, parse_output_string
from app.services.datetime_format import kor_today
from app.services.check_entities import check_entities, check_json_entities
from app.services.embeddings import KoBERTEmbeddings, query_embedding, format_docs, jamodict_search, format_dict, rename_dict
from app.services.datetime_format import kor_today, format_date_time, format_date, format_time, parse_am_pm
from app.services.check_entities import check_entities
from app.services.vector_store import FAISS_vectorize_documents, jamo_vectorize_documents


# OPENAI_API_KEY
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(
    api_key = OPENAI_API_KEY,
)

def vectorize_documents(documents, Embedding_model, FAISS_name, jamo_name):
    FAISS_vectorize_documents(documents, Embedding_model, FAISS_name)
    jamo_vectorize_documents(documents, jamo_name)

def process_documents_and_question(question,FAISS_name,jamo_name):
    # 한국 시간대 설정
    today,weekday = kor_today()

    # LLM 초기화
    llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.3, max_tokens=200)

    # LLMChain 설정
    ner_tpl = '''너는 영화 예매를 도와주는 챗봇이야. 영화 이름, 날짜, 시간, 장소를 구분하는 역할을 수행해.
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

    ner_tpl_secondary = '''
    "context 는 현재 상영중인 영화 리스트 : {context}"
    "대답은 무조건 context 리스트 안에서 대답한다."

    "context에 있는{movie}와 비슷한 이름을 movieName에 지정한다."
    "{movie}은 original로 지정한다."
    Question: {movie} 는 영화 이름의 일부분이다. {movie} 를 포함거나 유사한 영화 이름이 context에 포함되어 있는지 확인하여 채운다,
    없는 경우는 빈 항목으로 null를 채워서 마지막 줄에있는 출력형식으로만 대답해줘"

     {{"movieName" : null, "original": null}}

    '''

    prompt1 = ChatPromptTemplate.from_template(ner_tpl)
    prompt2 = ChatPromptTemplate.from_template(ner_tpl_secondary)

    chain1 = prompt1 | llm | StrOutputParser()
    chain2 = prompt2 | llm | StrOutputParser()

    # 임베딩 모델 초기화 및 벡터화
    embeddings_model = KoBERTEmbeddings()

    with open(f'{FAISS_name}.pkl', 'rb') as f:
        vector_store = pickle.load(f)
    with open(f'{jamo_name}.pkl', 'rb') as f:
        jamodict = pickle.load(f)
    # 쿼리 임베딩 및 첫 번째 LLM 호출
    query_results = query_embedding(question, k=5, embeddings_model=embeddings_model, vector_store=vector_store)
    response1 = chain1.invoke({
        'context': format_docs(query_results[1]),
        'question': question,
        'today': today,
        'weekday': weekday
    })
    # 기존에 입력한 영화 이름을 original에, full name을 movieName과 similar에
    response_dict = json.loads(response1)
    if response_dict["movieName"] in query_results[1]:
        return

    elif response_dict["similar"] is None and response_dict["movieName"] is not None:
        movie_name_query = jamodict_search(response_dict["movieName"], jamodict)
        response2 = chain2.invoke({
            'context': movie_name_query,
            'movie': response_dict["movieName"]
        })
        response_redict = json.loads(response2)
        response_dict = rename_dict(response_dict, response_redict)

    elif response_dict["similar"] and response_dict["movieName"] is None:
        jamoQuestion = jamodict_search(question,jamodict)
        response2 = chain2.invoke({
            'context': jamoQuestion,
            'movie': question
        })
        response_redict = json.loads(response2)
        response_dict = rename_dict(response_dict, response_redict)

    return json.dumps(response_dict)

def query_reprocess(query,FAISS_name,jamo_name,pre_response):
    # 한국 시간대 설정
    pre_response_dict = pre_response.dict()
    today,weekday = kor_today()

    # LLM 초기화
    llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0.3, max_tokens=200)

    re_ner_tpl = '''pre_response_dict에서 null을 채우기 위해 질문에서 너는 영화 이름, 날짜, 시간, 장소를 구분하는 역할을 수행해한다.
    pre_response_dict를 그대로 가져온다. 만약 영화 이름, 날짜, 시간, 장소를 변경을 요청하는 명확한 내용이 들어있으면 수정한다.
    context는 상영중인 영화 리스트이다.
    response_dict는 이전의 대답이다.
    response_dict:{pre_response_dict}
    영화 이름 null일 경우에만 {question}에서 현재 상영중인 영화 리스트에서 구분한다.
    동일한 이름이 없다면, 유사한 이름의 영화가 상영중인 영화 리스트에 있다면 영화이름을 리스트에 있는 이름으로 대체한다.
    similar에는 상영중인 영화 리스트에서 이름 넣는다.
    만약 없다면 null로 넣는다.
    오늘 날짜는 {today}이고 요일은 {weekday}다.
    만약 요일만 있다면 이번주로 계산한다.

    Question: pre_response_dict에서 그대로 가져오고, null인 것은 {question}문장 안에 영화 이름, 장소, 날짜, 시간이 포함되어 있는지 확인해 줘.
    영화는 movie : , 장소는 region: , 날짜는 date: , 시간은 time: , 문장에서 찾은 영화 이름은 Original:에 대입해줘, context와  유사한 이름 상영중인 영화이름은 Similar: 이라고 알려줘.
     빈 항목은 null를 채워서 마지막 줄에있는 출력형식으로만 대답한다.

    {{"movieName" : null, "region": null, "date": null, "time": null, "original": null, "similar": null}}
    '''

    ner_tpl_secondary = '''
    "context 는 현재 상영중인 영화 리스트 : {context}"
    "대답은 무조건 context 리스트 안에서 대답한다."

    "context에 있는{movie}와 비슷한 이름을 movieName에 지정한다."
    "{movie}은 original로 지정한다."
    Question: {movie} 는 영화 이름의 일부분이다. {movie} 를 포함거나 유사한 영화 이름이 context에 포함되어 있는지 확인하여 채운다,
    없는 경우는 빈 항목으로 null를 채워서 마지막 줄에있는 출력형식으로만 대답해줘"

     {{"movieName" : null, "original": null}}

    '''
    prompt1 = ChatPromptTemplate.from_template(re_ner_tpl)
    prompt2 = ChatPromptTemplate.from_template(ner_tpl_secondary)


    chain1 = prompt1 | llm | StrOutputParser()
    chain2 = prompt2 | llm | StrOutputParser()

    # 임베딩 모델 초기화 및 벡터화
    embeddings_model = KoBERTEmbeddings()
    with open(f'{FAISS_name}.pkl', 'rb') as f:
        vector_store = pickle.load(f)
    with open(f'{jamo_name}.pkl', 'rb') as f:
        jamodict = pickle.load(f)
    # 쿼리 임베딩 및 첫 번째 LLM 호출
    if pre_response_dict["movieName"] is not None:
        query_for_vector = pre_response_dict["movieName"]
    else:
        query_for_vector = query
    query_results = query_embedding(query_for_vector, k=5, embeddings_model=embeddings_model, vector_store=vector_store)
    response1 = chain1.invoke({
        'context': format_docs(query_results[1]),
        'pre_response_dict': format_dict(pre_response_dict),
        'question': query,
        'today': today,
        'weekday': weekday
    })

    response_dict = check_json_entities(response1)

    if response_dict["movieName"] in query_results[1]:
        return
    elif response_dict["similar"] is None and response_dict["movieName"] is not None:
        movie_name_query = jamodict_search(response_dict["movieName"], jamodict)
        response2 = chain2.invoke({
            'context': movie_name_query,
            'movie': response_dict["movieName"]
        })
        response_redict = json.loads(response2)
        response_dict = rename_dict(response_dict, response_redict)
    elif response_dict["similar"] and response_dict["movieName"] is None:
        jamoQuestion = jamodict_search(query,jamodict)
        response2 = chain2.invoke({
            'context': jamoQuestion,
            'movie': query
        })
        response_redict = json.loads(response2)
        response_dict = rename_dict(response_dict, response_redict)

    return json.dumps(response_dict)

# api 호출
def api_call(system_message, user_message):
    try:
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=1.0
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {e}"


def generate_response(entities):
    system_message = (
        "당신은 사용자에게 영화 예매 정보를 확인하는 고객지원 챗봇 '무비빔밥'입니다. "
        "사용자가 입력한 영화 이름, 지역, 날짜, 시간에 대한 정보를 확인하고, 그 정보가 정확한지 물어보세요. "
        "단, 사용자에게 추가 정보를 제공하거나 다른 주제에 대해 대답하지 마세요. "
    )

    # 엔티티 정확한지 확인
    user_message, entities = check_entities(entities)
    # api 호출
    chatbot_response = api_call(system_message, user_message)

    # 불필요한 origin, similar 엔티티 제거 후 response를 엔티티에 추가
    entities = {k: entities[k] for k in ['movieName', 'region', 'date', 'time'] if k in entities}
    entities['response'] = chatbot_response

    # json 형태로 변환하여 return
    return json.dumps(entities, ensure_ascii=False)
def location_type(response_dict):
    # response_dict = json.loads(response)
    region_value = response_dict["region"]
    with open("./services/region_text.txt", "r", encoding="utf-8") as file:
        region_text = file.read()
    temperature = 0.3
    #print('temperature', temperature)

    # LLM 초기화
    llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=temperature, max_tokens=200)

    # LLMChain 설정
    location_tpl = f'''너는 지리에 정통한 챗봇으로, 입력된 지명이나 주소를 처리하는 일을 담당해. 아래의 가이드라인을 따를 거야:
    1. 주소를 알수 없는 지명이나, 없는 지명이라면 "null"을 반환해.
    
    2. 주어진 지명에 대해, 동일한 이름을 가진 다른 시군구의 위치를 모두 찾아줘. 
       예를 들어, 만약 여러 도시나 지역에서 같은 이름의 지명이 있다면, 그 모든 위치를 전달해줘.
       예시:
       input: ["논현동"]
       output: ["서울시 강남구 논현동", "인천시 남동구 논현동"]
    
    3. 주어진 지명이나 지역을 보다 큰 주소로 변환해 줘.
       주소는 참고지역 까지만 변환해 줘.
       예시:
       input: ["강남"]
       output: ["서울시 강남구"]
       
       input: ["광화문"]
       output: ["서울시 종로구"]
       
       input: ["남산"]
       output: ["서울시 중구", 서울시 용산구]
       
       input: ["홍제동"]
       output: ["서울시 서대문구 홍제동", "강원도 강릉시 홍제동"]
    
    4. 참조 지명에서 찾는다. region_text는 참조 지명이다.
    region_text:{region_text}
    
    
    이제, 내가 찾고자 하는 장소를 알려줄게, 없으면 None을 준다.:
    input: {region_value}
    
    출력은 아래 형식으로 해줘:
    output: 
    
    '''

    prompt = ChatPromptTemplate.from_template(location_tpl)
    chain = prompt | llm | StrOutputParser()

    # 질문에 대한 답변 생성
    response = chain.invoke({
        'region_value': region_value,
        'region_text': region_text

    })
    processed_responses = parse_output_string(response)
    try:
        # response을 처리하여 리스트로 변환

        region_list = processed_responses
        processed_responses = []  # 응답을 저장할 리스트 초기화

        for region in region_list:
            words = region.split(" ")
            # 앞의 두 단어를 추출
            response = " ".join(words[:2])
            processed_responses.append(response)

        response_dict["region"] = processed_responses

    except Exception as e:
        print(f"지역 변환 오류 발생: {e}")
    return response_dict