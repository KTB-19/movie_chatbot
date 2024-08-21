import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend/src/main/java/com/ktb19/moviechatbot/ai'))
from vector_store import FAISS_vectorize_documents, jamo_vectorize_documents
from embeddings import KoBERTEmbeddings, query_embedding, jamodict_search, format_docs
import pickle
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import openai
from time_format import format_date_time,kor_today
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
        if not entities.get(key):
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
        user_message = f"{entities['date']} {entities['time']}에 {entities['region']}에서 {entities['movieName']}을(를) 보시고 싶으신 게 맞으신가요?"

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

def generate_response(entities):
    system_message = (
        "당신은 사용자에게 영화관을 추천해주는 고객지원 챗봇 '무비빔밥'입니다."
        "사용자의 입력을 바탕으로 적절한 응답을 생성하세요."
        "사용자가 필요한 모든 엔티티(영화 이름, 지역, 날짜, 시간)를 제공한 경우 확인 질문을 생성하세요. "
        "예를 들어, 사용자가 영화 이름, 지역, 날짜, 시간을 제공했다면, 다음과 같이 응답하세요: "
        "'{date}(에) {time}에 {region}에서 {movieName}을(를) 보시고 싶으신 게 맞으신가요?' "
        "만약 어떤 엔티티가 누락되었다면, 해당 정보를 요청하는 질문을 생성하세요. "
        "예를 들어, 지역 정보가 누락된 경우 '어느 지역에서 영화를 보고 싶으신가요?'라고 물어보세요. "
        "영화 이름이 불명확하거나 불완전한 경우, 이를 확인하는 질문을 생성하세요. "
        "항상 예매를 완료하기 위해 필요한 모든 정보를 수집하는 것을 목표로 하세요."
        "단, 사용자에게 영화 예매를 도와주겠다는 응답은 하지 마세요."
    )

    user_message, entities = check_entities(entities)
    chatbot_response = api_call(system_message, user_message)

    # 불필요한 origin, similar 엔티티 제거
    entities = {k: entities[k] for k in ['movieName', 'region', 'date', 'time'] if k in entities}
    # entities에 response 추가
    entities['response'] = chatbot_response

    # json 형태로 변환하여 return
    return json.dumps(entities, ensure_ascii=False)