import sys
import os
import json

#%%
os.chdir('backend/src/main/java/com/ktb19/moviechatbot/ai')
sys.path.append(os.getcwd())
#%%
from main import vectorize_documents, process_documents_and_question, generate_response
from embeddings import KoBERTEmbeddings
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
