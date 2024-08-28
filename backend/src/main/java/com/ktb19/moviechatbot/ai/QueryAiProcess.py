#%%
# 필요 의존성 설치
# pip install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'
# pip install langchain
# pip install transformers
# pip install sentence-transformers
# pip install faiss-cpu
# pip install -q langchain langchain-community
# pip install langchain_openai
# pip install python-Levenshtein
# pip install transformers datasets torch
# pip install jamo
# pip install openai
# pip install kiwi
# pip install torch torchvision torchaudio
# pip install torch
# pip install python-dotenv

#%%
from kobert_tokenizer import KoBERTTokenizer
import torch
from transformers import BertModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import json
from datetime import datetime
import pytz
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import Levenshtein
from jamo import h2j, j2h, j2hcj
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
from kiwipiepy import Kiwi
# import tensorflow as tf
# from tensorflow import keras

#%%
# OPENAI_API_KEY
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(
    api_key = OPENAI_API_KEY,
)
#%%
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
# def documents_to_jamodict(documents):
#     okt = Okt()
#     jamodict = {}
#     for doc in documents:
#         docnouns = [""]  # 첫 번째 항목은 모든 명사를 합친 문자열
#         for noun in okt.nouns(doc):
#             jamo_noun = hangul_to_jamo(noun)
#             docnouns[0] += jamo_noun
#             docnouns.append(jamo_noun)
#         jamodict[doc] = docnouns
#     return jamodict

# 문서들을 자모 사전으로 변환하는 함수
def documents_to_jamodict(documents):
    kiwi = Kiwi()
    jamodict = {}
    for doc in documents:
        docnouns = [""]  # 첫 번째 항목은 모든 명사를 합친 문자열
        for sentence in kiwi.analyze(doc):
            for word, tag, _, _ in sentence[0]:
                if tag in ['NNG', 'NNP']:  # 일반 명사(NNG) 및 고유 명사(NNP)
                    jamo_noun = hangul_to_jamo(word)
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
    # 기존에 입력한 영화 이름을 original에, full name을 movieName과 similar에
    responseDict = json.loads(response1)
    if responseDict["movieName"] in query_results[1]:
        return
    elif responseDict["similar"] is None and responseDict["movieName"] is not None:
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



from datetime import datetime
import re

# 날짜, 시간 형식 변경
def format_date_time(date, time):
    formatted_date = format_date(date)
    formatted_time = format_time(time)
    return formatted_date, formatted_time

def format_date(date):
    if not date:
        return date
    try:
        # 입력된 date 파싱 + 현재 연도: YYYY-MM-DD 형식으로 변환
        date_obj = datetime.strptime(date, '%m/%d')
        return date_obj.replace(year=datetime.now().year).strftime('%Y-%m-%d')
    except ValueError:
        return date    # 파싱 실패 시 원래 입력값 리턴

def format_time(time):
    if not time:
        return time

    # 다양한 시간 입력 패턴 문자열
    time_patterns = {
        r'^\d{1,2}:\d{2}$': lambda t: t,    # HH:MM 형식
        r'^\d{1,2}시\s?\d{1,2}분$': lambda t: datetime.strptime(t, '%H시 %M분').strftime('%H:%M'),    # HH시 MM분 형식
        r'^\d{1,2}시$': lambda t: f"{(int(t[:-1]) % 12 + 12):02}:00",    # HH시 (우선 오후로 간주)
        r'^(오전|오후)\s?\d{1,2}시$': parse_am_pm,    # 오전/오후 HH시
        r'^(오전|오후|저녁|심야)$': lambda t: {'오전': '07:00', '오후': '12:00', '저녁': '18:00', '심야': '23:00'}[t]
    }

    for pattern, formatter in time_patterns.items():
        if re.match(pattern, time):
            return formatter(time)
    return time
    
# 오전/오후 시간을 HH:MM 형식으로 변환하기
def parse_am_pm(time):
    period, hour = re.match(r'^(오전|오후)\s?(\d{1,2})시$', time).groups()
    hour = int(hour)
    if period == '오전':
        return f"{hour:02}:00" if hour < 12 else "00:00"
    else:
        return f"{(hour % 12 + 12):02}:00"


# 입력한 정보가 정확한지 확인
def check_entities(entities):
    entity_info = [
        ("movieName", "영화 제목"),
        ("region", "지역"),
        ("date", "날짜"),
        ("time", "시간")
    ]

    missing_entities = []
    for key, message in entity_info:
        if key not in entities or not entities[key]:  # None 또는 False인 값을 걸러냄
            missing_entities.append(message)

    # 엔티티가 2개 이상 누락된 경우
    if missing_entities:
        if len(missing_entities) >= 2:
            missing_str = ' 와 '.join(missing_entities)
            user_message = f"관람하고 싶은 {missing_str}을 말씀해 주세요."
        else:
            user_message = f"관람하고 싶은 {missing_entities[0]}을 말씀해 주세요."
    else:
        # 엔티티가 모두 채워진 경우 확인 문장 출력
        entities['date'], entities['time'] = format_date_time(entities['date'], entities['time'])   # 날짜, 시간 형식 변경 적용
        user_message = f"{entities['date']} {entities['time']}에 {entities['region']}에서 {entities['movieName']}을(를) 보고 싶으신 게 맞으신가요?"

    return user_message, entities


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


# api 시스템 메시지 설정
def generate_response(entities):
    system_message = (
        "당신은 사용자에게 영화 예매 정보를 확인하는 고객지원 챗봇 '무비빔밥'입니다. "
        "사용자가 입력한 영화 이름, 지역, 날짜, 시간에 대한 정보를 확인하고, 그 정보가 정확한지 물어보세요. "
        "단, 사용자에게 추가 정보를 제공하거나 다른 주제에 대해 대답하지 마세요. "
    )

    user_message, entities = check_entities(entities)
    chatbot_response = api_call(system_message, user_message)

    # 불필요한 origin, similar 엔티티 제거 후 response를 엔티티에 추가
    entities = {k: entities[k] for k in ['movieName', 'region', 'date', 'time'] if k in entities}
    entities['response'] = chatbot_response

    # json 형태로 변환하여 return
    return json.dumps(entities, ensure_ascii=False)
#%%

'''
# 사용 예시
documents = [
"데드풀과 울버린",
"늘봄가든",
"빅토리",
"세븐틴 투어 ‘팔로우’ 어게인 투 시네마",
"명탐정 코난: 100만 달러의 펜타그램",
"2023 심규선 단독 콘서트 : 우리 앞의 세계",
"에이리언: 로물루스",
"토끼는 어디로 갔나요?",
"쥬라기캅스 극장판: 전설의 고대생물을 찾아라",
"행복의 나라",
"트위스터스",
"슈퍼배드 4",
"이준호 콘서트 : 다시 만나는 날",
"사랑의 하츄핑",
"우마무스메 프리티 더비 새로운 시대의 문",
"하이퍼포커스 : 투모로우바이투게더 브이알 콘서트",
"베베핀 플레이타임",
"바다 탐험대 옥토넛 어보브 앤 비욘드 : 바다가 위험해",
"이매지너리",
"탈주",
"2023 영탁 단독 콘서트 : 탁쇼2",
"헬로카봇 올스타 스페셜",
"탈출: 프로젝트 사일런스",
"극장총집편 봇치 더 록! 전편",
"플라이 미 투 더 문",
"볼빨간사춘기: 메리 고 라운드 더 무비",
"블랙핑크 월드투어 [본 핑크] 인 시네마",
"이솝이야기",
"박정희: 경제대국을 꿈꾼 남자",
"극장판 도라에몽: 진구의 지구 교향곡",
"2024 박은빈 팬 콘서트 <은빈노트 : 디바>",
"민요 첼로",
"다큐 황은정 : 스마트폰이 뭐길래"
]

question = "데드풀 토요일 5시에 보고 싶어"

## 함수 실행 예시
result = process_documents_and_question(documents, question)
entities = json.loads(result)
json_response = generate_response(entities)
parsed_response = json.loads(json_response)
print(parsed_response)
'''

# AI 정확도 평가 및 테스트(주의 토큰 소모가 클수있음.)
'''
def finaltest(question,documents):
  print("question:",question)
  result = process_documents_and_question(documents, question)
  entities = json.loads(result)
  print("entities:",entities)
  json_response = generate_response(entities)
  parsed_response = json.loads(json_response)
  print("final:",parsed_response)


answer_key = [
    "울버린 이번 주 토요일 5시에 보고 싶어",  # 완전한 질문 (영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함)
    "늘봄가든 내일 저녁에 볼 수 있을까?",  # 시간 누락 (영화 : 포함, 장소: 없음, 시간 : 없음, 날짜 포함)
    "빅토리 오늘 서울 연수구에서 어디서 상영하나요?",  # 시간 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "세븐틴 투어 일요일 3시에 볼 수 있어?",  # 완전한 질문 (영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함)
    "코난 이번 주말에 부산 부산대 근처에서 상영하는 곳 있어?",  # 시간 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "에이리언 오늘 저녁에 대구 동성로에서 상영하는 곳 있나요?",  # 시간 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "토끼 이번 주 토요일 오후 2시에 보고 싶어",  # 완전한 질문 (영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함)
    "쥬라기캅스 내일 오전 11시에 인천 연수구에서 어디서 볼 수 있나요?",  # 완전한 질문 (영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함)
    "행복의 나라 오늘 오후 5시에 상영하나요?",  # 완전한 질문 (영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함)
    "슈퍼배드 이번 주 금요일에 광주 충장로에서 보고 싶어",  # 시간 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "이준호 콘서트 다음 주 화요일 7시에 대전 둔산동에서 보고 싶어",  # 장소 추가 (영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함)
    "사랑의 하츄핑 이번 주 목요일 수원 영통구에서 볼 수 있어?",  # 시간, 장소 추가 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "우마무스메 주말에 부산 해운대에서 볼 수 있는 시간 있나요?",  # 장소 추가 (영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함)
    "옥토넛 오늘 오후에 서울 강남구에서 어디서 상영해?",  # 시간 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "이매지너리 다음 주 월요일 제주도 서귀포에서 상영하나요?",  # 시간, 장소 추가 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "2023 영탁 콘서트 이번 주 일요일 오후 5시에 상영하나요?",  # 완전한 질문 (영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함)
    "헬로카봇 올스타 주말에 대전 둔산동에서 보고 싶어",  # 시간, 날짜 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 없음)
    "탈출 프로젝트 오늘 저녁 9시에 상영하나요?",  # 완전한 질문 (영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함)
    "봇치 더 록 이번 주 금요일 오후 4시에 서울 강남구에서 상영하는 곳 있나요?",  # 장소 추가 (영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함)
    "도라에몽 다음 주 수요일 강남에서 보고 싶어",  # 시간 누락 (영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함)
    "스파이더맨 주말에 서울 홍대에서 상영하는 곳 있나요?",  # 시간, 장소 추가 (영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함)
    "어벤져스 다음 주 목요일 부산 서면에서 상영하나요?",  # 시간, 장소 추가 (영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함)
    "해리포터 금요일 저녁 8시에 볼 수 있는 곳?",  # 완전한 질문 (영화 : 없음, 장소: 없음, 시간 포함, 날짜 포함)
    "인셉션 오늘 저녁에 강남 신촌에서 상영하나요?",  # 장소 추가 (영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함)
    "아이언맨 3 오늘 오후 6시에 보고 싶어",  # 완전한 질문 (영화 : 없음, 장소: 없음, 시간 포함, 날짜 포함)
    "겨울왕국 내일 오전에 대구 수성구에서 볼 수 있는 곳?",  # 장소 추가 (영화 : 없음, 장소: 포함, 시간 없음, 날짜 포함)
    "토이스토리 오후 3시에 상영하는 곳 있나요?",  # 날짜 누락 (영화 : 없음, 장소: 없음, 시간 : 포함, 날짜 없음)
    "라라랜드 다음 주 화요일 오후에 서울 서울대 근처에서 상영하나요?",  # 시간 누락 (영화 : 없음, 장소: 포함, 시간 없음, 날짜 포함)
    "타이타닉 오늘 오후 2시에 부산 해운대에서 어디서 볼 수 있나요?",  # 장소 추가 (영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함)
    "퍼시픽림 오늘 밤 9시에 볼 수 있는 곳 있나요?"  # 완전한 질문 (영화 : 없음, 장소: 없음, 시간 포함, 날짜 포함)
]
annotations_with_titles = [
    "완전한 질문 (영화: 데드풀과 울버린, 장소: 없음, 시간 포함, 날짜 포함)",
    "시간 누락 (영화: 늘봄가든, 장소: 없음, 시간: 없음, 날짜 포함)",
    "시간 누락 (영화: 빅토리, 장소: 포함 - 서울 연수구, 시간: 없음, 날짜 포함)",
    "완전한 질문 (영화: 세븐틴 투어 ‘팔로우’ 어게인 투 시네마, 장소: 없음, 시간 포함, 날짜 포함)",
    "시간 누락 (영화: 명탐정 코난: 100만 달러의 펜타그램, 장소: 포함 - 부산 부산대, 시간: 없음, 날짜 포함)",
    "시간 누락 (영화: 에이리언: 로물루스, 장소: 포함 - 대구 동성로, 시간: 없음, 날짜 포함)",
    "완전한 질문 (영화: 토끼는 어디로 갔나요?, 장소: 없음, 시간 포함, 날짜 포함)",
    "완전한 질문 (영화: 쥬라기캅스 극장판: 전설의 고대생물을 찾아라, 장소: 포함 - 인천 연수구, 시간 포함, 날짜 포함)",
    "완전한 질문 (영화: 행복의 나라, 장소: 없음, 시간 포함, 날짜 포함)",
    "시간 누락 (영화: 슈퍼배드 4, 장소: 포함 - 광주 충장로, 시간: 없음, 날짜 포함)",
    "장소 추가 (영화: 이준호 콘서트 : 다시 만나는 날, 장소: 포함 - 대전 둔산동, 시간 포함, 날짜 포함)",
    "시간, 장소 추가 (영화: 사랑의 하츄핑, 장소: 포함 - 수원 영통구, 시간: 없음, 날짜 포함)",
    "장소 추가 (영화: 우마무스메 프리티 더비 새로운 시대의 문, 장소: 포함 - 부산 해운대, 시간 포함, 날짜 포함)",
    "시간 누락 (영화: 바다 탐험대 옥토넛 어보브 앤 비욘드 : 바다가 위험해, 장소: 포함 - 서울 강남구, 시간: 없음, 날짜 포함)",
    "시간, 장소 추가 (영화: 이매지너리, 장소: 포함 - 제주도 서귀포, 시간: 없음, 날짜 포함)",
    "완전한 질문 (영화: 2023 영탁 단독 콘서트 : 탁쇼2, 장소: 없음, 시간 포함, 날짜 포함)",
    "시간, 날짜 누락 (영화: 헬로카봇 올스타 스페셜, 장소: 포함 - 대전 둔산동, 시간: 없음, 날짜 없음)",
    "완전한 질문 (영화: 탈출: 프로젝트 사일런스, 장소: 없음, 시간 포함, 날짜 포함)",
    "장소 추가 (영화: 극장총집편 봇치 더 록! 전편, 장소: 포함 - 서울 강남구, 시간 포함, 날짜 포함)",
    "시간 누락 (영화: 극장판 도라에몽: 진구의 지구 교향곡, 장소: 포함 - 강남, 시간: 없음, 날짜 포함)",
    "시간, 장소 추가 (영화: 없음, 장소: 포함 - 서울 홍대, 시간 포함, 날짜 포함)",
    "시간, 장소 추가 (영화: 없음, 장소: 포함 - 부산 서면, 시간 포함, 날짜 포함)",
    "완전한 질문 (영화: 없음, 장소: 없음, 시간 포함, 날짜 포함)",
    "장소 추가 (영화: 없음, 장소: 포함 - 신촌, 시간 포함, 날짜 포함)",
    "완전한 질문 (영화: 없음, 장소: 없음, 시간 포함, 날짜 포함)",
    "장소 추가 (영화: 없음, 장소: 포함 - 대구 수성구, 시간 없음, 날짜 포함)",
    "날짜 누락 (영화: 없음, 장소: 없음, 시간: 포함, 날짜 없음)",
    "시간 누락 (영화: 없음, 장소: 포함 - 서울 서울대, 시간 없음, 날짜 포함)",
    "장소 추가 (영화: 없음, 장소: 포함 - 부산 해운대, 시간 포함, 날짜 포함)",
    "완전한 질문 (영화: 없음, 장소: 없음, 시간 포함, 날짜 포함)"
]

questions=[answer_key,annotations_with_titles]

for N in range(30):
  print("---------------------------------------------------------------------------")
  print(questions[1][N])
  finaltest(questions[0][N],documents)
  print("---------------------------------------------------------------------------")
'''
