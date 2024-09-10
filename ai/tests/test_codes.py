import sys
import os
import json


# #%%
# os.chdir('backend/src/main/java/com/ktb19/moviechatbot/ai')
# sys.path.append(os.getcwd())
#%%
from app.services.query_ai_process import vectorize_documents, process_documents_and_question, generate_response,query_reprocess, location_type
from app.services.embeddings import KoBERTEmbeddings

#%%
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
#%%

areas = [
    {
        "wideArea": "서울시",
        "basicArea": [
            "강남구",
            "강동구",
            "강북구",
            "강서구",
            "관악구",
            "광진구",
            "구로구",
            "금천구",
            "노원구",
            "도봉구",
            "동대문구",
            "동작구",
            "마포구",
            "서대문구",
            "서초구",
            "성동구",
            "성북구",
            "송파구",
            "양천구",
            "영등포구",
            "용산구",
            "은평구",
            "종로구",
            "중구",
            "중랑구",
        ]
    },
    {
        "wideArea": "경기도",
        "basicArea": [
            "광주시",
            "구리시",
            "군포시",
            "김포시",
            "남양주시",
            "동두천시",
            "부천시",
            "성남시",
            "수원시",
            "시흥시",
            "안산시",
            "안성시",
            "안양시",
            "오산시",
            "용인시",
            "의왕시",
            "의정부시",
            "이천시",
            "파주시",
            "평택시",
            "하남시",
            "화성시",
            "가평군",
            "양주시",
            "양평군",
            "여주군",
            "연천군",
            "포천시",
            "고양시",
            "과천시",
            "광명시",
        ]
    },
    {
        "wideArea": "강원도",
        "basicArea": [
            "양양군",
            "영월군",
            "인제군",
            "정선군",
            "철원군",
            "평창군",
            "홍천군",
            "화천군",
            "횡성군",
            "강릉시",
            "동해시",
            "삼척시",
            "속초시",
            "원주시",
            "춘천시",
            "태백시",
            "고성군",
            "양구군",
        ]
    },
    {
        "wideArea": "충청북도",
        "basicArea": [
            "제천시",
            "청주시",
            "충주시",
            "괴산군",
            "단양군",
            "보은군",
            "영동군",
            "옥천군",
            "음성군",
            "진천군",
            "청원군",
            "증평군",
        ]
    },
    {
        "wideArea": "충청남도",
        "basicArea": [
            "공주시",
            "논산시",
            "보령시",
            "서산시",
            "아산시",
            "천안시",
            "금산군",
            "당진군",
            "부여군",
            "서천군",
            "예산군",
            "청양군",
            "태안군",
            "홍성군",
            "계룡시",
        ]
    },
    {
        "wideArea": "경상북도",
        "basicArea": [
            "경산시",
            "경주시",
            "구미시",
            "김천시",
            "문경시",
            "상주시",
            "안동시",
            "영주시",
            "영천시",
            "포항시",
            "고령군",
            "군위군",
            "봉화군",
            "성주군",
            "영덕군",
            "영양군",
            "예천군",
            "울릉군",
            "울진군",
            "의성군",
            "청도군",
            "청송군",
            "칠곡군",
        ]
    },
    {
        "wideArea": "경상남도",
        "basicArea": [
            "합천군",
            "창원시 마산합포구",
            "창원시 마산회원구",
            "창원시 성산구",
            "창원시 의창구",
            "창원시 진해구",
            "거제시",
            "김해시",
            "밀양시",
            "사천시",
            "양산시",
            "진주시",
            "창원시",
            "통영시",
            "거창군",
            "고성군",
            "남해군",
            "산청군",
            "의령군",
            "창녕군",
            "하동군",
            "함안군",
            "함양군",
        ]
    },
    {
        "wideArea": "전라북도",
        "basicArea": [
            "진안군",
            "군산시",
            "김제시",
            "남원시",
            "익산시",
            "전주시",
            "정읍시",
            "고창군",
            "무주군",
            "부안군",
            "순창군",
            "완주군",
            "임실군",
            "장수군",
        ]
    },
    {
        "wideArea": "전라남도",
        "basicArea": [
            "광양시",
            "나주시",
            "목포시",
            "순천시",
            "여수시",
            "강진군",
            "고흥군",
            "곡성군",
            "구례군",
            "담양군",
            "무안군",
            "보성군",
            "신안군",
            "영광군",
            "영암군",
            "완도군",
            "장성군",
            "장흥군",
            "진도군",
            "함평군",
            "해남군",
            "화순군",
        ]
    },
    {
        "wideArea": "제주도",
        "basicArea": [
            "서귀포시",
            "제주시",
            "남제주군",
            "북제주군",
        ]
    },
    {
        "wideArea": "부산시",
        "basicArea": [
            "강서구",
            "금정구",
            "남구",
            "동구",
            "동래구",
            "부산진구",
            "북구",
            "사상구",
            "사하구",
            "서구",
            "수영구",
            "연제구",
            "영도구",
            "중구",
            "해운대구",
            "기장군",
        ]
    },
    {
        "wideArea": "대구시",
        "basicArea": [
            "남구",
            "달서구",
            "동구",
            "북구",
            "서구",
            "수성구",
            "중구",
            "달성군",
        ]
    },
    {
        "wideArea": "대전시",
        "basicArea": [
            "대덕구",
            "동구",
            "서구",
            "유성구",
            "중구",
        ]
    },
    {
        "wideArea": "울산시",
        "basicArea": [
            "남구",
            "동구",
            "북구",
            "중구",
            "울주군",
        ]
    },
    {
        "wideArea": "인천시",
        "basicArea": [
            "계양구",
            "남구",
            "남동구",
            "동구",
            "부평구",
            "서구",
            "연수구",
            "중구",
            "강화군",
            "웅진군",
        ]
    },
    {
        "wideArea": "광주시",
        "basicArea": [
            "광산구",
            "남구",
            "동구",
            "북구",
            "서구"
        ]
    },
    {
        "wideArea": "세종시",
        "basicArea": [
            "연기군",
        ]
    },
]



#%%

embeddings_model = KoBERTEmbeddings()
vectorize_documents(documents,embeddings_model,'KoBERT_vector_store','jamodict')
#%%
question = "데드풀 토요일 5시에 보고 싶어"
#%%
## 함수 실행 예시
result = process_documents_and_question(question,'KoBERT_vector_store','jamodict')
entities = json.loads(result)
json_response = generate_response(entities)
parsed_response = json.loads(json_response)
print(parsed_response)

#%%
def chat_test(question,re_question):
    result = process_documents_and_question(question,'KoBERT_vector_store','jamodict')
    entities = json.loads(result)
    json_response = generate_response(entities)
    parsed_response = json.loads(json_response)
    re_result = query_reprocess(re_question,'KoBERT_vector_store','jamodict', entities)
    re_entities = json.loads(re_result)
    json_response = generate_response(re_entities)
    re_parsed_response = json.loads(json_response)
    return parsed_response, re_parsed_response
#%%
question = "데드풀 토요일 5시에 보고 싶어"
re_question = "강남에서 보고싶어"
#%%
print(chat_test(question, re_question))
#%%
answer_key = [
    ["울버린 이번 주 토요일 5시에 보고 싶어", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "강남에서 보고 싶어.", "데드풀과 울버린"],
    ["늘봄가든 내일 저녁에 볼 수 있을까?", "시간, 장소 누락, {영화 : 포함, 장소: 없음, 시간 : 없음, 날짜 포함}", "강남에서 저녁 7시에 보고 싶어.", "늘봄가든"],
    ["빅토리 오늘 서울 연수구에서 어디서 상영하나요?", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 2시에 보고 싶어.", "빅토리"],
    ["세븐틴 투어 일요일 3시에 볼 수 있어?", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "홍대에서 보고 싶어.", "세븐틴 투어 ‘팔로우’ 어게인 투 시네마"],
    ["코난 이번 주말에 부산 부산대 근처에서 상영하는 곳 있어?", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 4시에 보고 싶어.", "명탐정 코난: 100만 달러의 펜타그램"],
    ["에이리언 오늘 저녁에 대구 동성로에서 상영하는 곳 있나요?", "완전한 질문, {영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "에이리언: 로물루스"],
    ["토끼 이번 주 토요일 오후 2시에 보고 싶어", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "서초구에서 보고 싶어.", "토끼는 어디로 갔나요?"],
    ["쥬라기캅스 내일 오전 11시에 인천 연수구에서 어디서 볼 수 있나요?", "완전한 질문, {영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "쥬라기캅스 극장판: 전설의 고대생물을 찾아라"],
    ["행복의 나라 오늘 오후 5시에 상영하나요?", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "광화문에서 보고 싶어.", "행복의 나라"],
    ["슈퍼배드 이번 주 금요일에 광주 충장로에서 보고 싶어", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 6시에 보고 싶어.", "슈퍼배드 4"],
    ["이준호 콘서트 다음 주 화요일 7시에 대전 둔산동에서 보고 싶어", "완전한 질문, {영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "이준호 콘서트 : 다시 만나는 날"],
    ["사랑의 하츄핑 이번 주 목요일 수원 영통구에서 볼 수 있어?", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 3시에 보고 싶어.", "사랑의 하츄핑"],
    ["우마무스메 주말에 부산 해운대에서 볼 수 있는 시간 있나요?", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오전 10시에 보고 싶어.", "우마무스메 프리티 더비 새로운 시대의 문"],
    ["옥토넛 오늘 오후에 서울 강남구에서 어디서 상영해?", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 2시에 보고 싶어.", "바다 탐험대 옥토넛 어보브 앤 비욘드 : 바다가 위험해"],
    ["이매지너리 다음 주 월요일 제주도 서귀포에서 상영하나요?", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 1시에 보고 싶어.", "이매지너리"],
    ["2023 영탁 콘서트 이번 주 일요일 오후 5시에 상영하나요?", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "대전에서 보고 싶어.", "2023 영탁 단독 콘서트 : 탁쇼2"],
    ["헬로카봇 올스타 주말에 대전 둔산동에서 보고 싶어", "시간, 날짜 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 없음}", "오후 3시에 보고 싶어.", "헬로카봇 올스타 스페셜"],
    ["탈출 프로젝트 오늘 저녁 9시에 상영하나요?", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "인천에서 보고 싶어.", "탈출: 프로젝트 사일런스"],
    ["봇치 더 록 이번 주 금요일 오후 4시에 서울 강남구에서 상영하는 곳 있나요?", "완전한 질문, {영화 : 포함, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "극장총집편 봇치 더 록! 전편"],
    ["도라에몽 다음 주 수요일 강남에서 보고 싶어", "시간 누락, {영화 : 포함, 장소: 포함, 시간 : 없음, 날짜 포함}", "오후 3시에 보고 싶어.", "극장판 도라에몽: 진구의 지구 교향곡"],
    ["스파이더맨 주말에 서울 홍대에서 상영하는 곳 있나요?", "완전한 질문, {영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "스파이더맨 (예시)"],
    ["어벤져스 다음 주 목요일 부산 서면에서 상영하나요?", "시간 누락, {영화 : 없음, 장소: 포함, 시간 없음, 날짜 포함}", "오후 5시에 보고 싶어.", "어벤져스 (예시)"],
    ["해리포터 금요일 저녁 8시에 볼 수 있는 곳?", "완전한 질문, {영화 : 없음, 장소: 없음, 시간 포함, 날짜 포함}", "답변 필요 없음.", "해리포터 (예시)"],
    ["인셉션 오늘 저녁에 강남 신촌에서 상영하나요?", "완전한 질문, {영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "인셉션 (예시)"],
    ["아이언맨 3 오늘 오후 6시에 보고 싶어", "완전한 질문, {영화 : 없음, 장소: 없음, 시간 포함, 날짜 포함}", "답변 필요 없음.", "아이언맨 3 (예시)"],
    ["겨울왕국 내일 오전에 대구 수성구에서 볼 수 있는 곳?", "시간 누락, {영화 : 없음, 장소: 포함, 시간 없음, 날짜 포함}", "오전 9시에 보고 싶어.", "겨울왕국 (예시)"],
    ["토이스토리 오후 3시에 상영하는 곳 있나요?", "날짜 누락, {영화 : 없음, 장소: 없음, 시간 : 포함, 날짜 없음}", "내일 보고 싶어.", "토이스토리 (예시)"],
    ["라라랜드 다음 주 화요일 오후에 서울 서울대 근처에서 상영하나요?", "시간 누락, {영화 : 없음, 장소: 포함, 시간 없음, 날짜 포함}", "오후 4시에 보고 싶어.", "라라랜드 (예시)"],
    ["타이타닉 오늘 오후 2시에 부산 해운대에서 어디서 볼 수 있나요?", "완전한 질문, {영화 : 없음, 장소: 포함, 시간 포함, 날짜 포함}", "답변 필요 없음.", "타이타닉 (예시)"],
    ["퍼시픽림 오늘 밤 9시에 볼 수 있는 곳 있나요?", "장소 누락, {영화 : 없음, 장소: 없음, 시간 포함, 날짜 포함}", "홍대에서 보고 싶어.", "퍼시픽림 (예시)"]
]
for question_and_answer in answer_key:
    question, requestion = question_and_answer[0], question_and_answer[2]
    chat_test_answers = chat_test(question,re_question)
    answer, final_answer = chat_test_answers[0], chat_test_answers[1]
#%%
question_and_answer = ["울버린 이번주 토요일 5시에 보고 싶어", "장소 누락, {영화 : 포함, 장소: 없음, 시간 포함, 날짜 포함}", "논현에서 보고 싶어.", "데드풀과 울버린"]
question, re_question = question_and_answer[0], question_and_answer[2]
chat_test_answers = chat_test(question, re_question)
answer, pre_final_answer = chat_test_answers[0], chat_test_answers[1]
final_answer = location_type(pre_final_answer)
print(question, re_question, chat_test_answers, pre_final_answer, final_answer)
print(question)
print(answer)
print(re_question)
print(pre_final_answer)
print(final_answer)

