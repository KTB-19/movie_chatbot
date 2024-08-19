from fastapi import APIRouter
from sqlalchemy import text

from app.api.dto.additional_infos_request import AdditionalInfosRequest
from app.db.database import engine
from app.models.info import Info
from app.services.test1 import get_response
from app.services.test2 import get_response_additional
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn")

@router.get("/infos")
async def get_infos(message: str = "") -> Info:
    logger.info("get_infos start")
    logger.info(f"message : {message}")

    movies = await read_movies()
    logger.info(f"sql result movies : {movies}")

    response: Info = Info(**get_response(movies, message))
    logger.info(f"response : {response}")

    return response


@router.post("/infos/additional")
async def get_infos_additional(request: AdditionalInfosRequest) -> Info:
    logger.info("get_infos_additional start")
    logger.info(f"parsedQuery : {request.parsedQuery}")
    logger.info(f"message : {request.message}")

    movies = await read_movies()
    logger.info(f"sql result movies : {movies}")

    response: Info = Info(**get_response_additional(movies, request.parsedQuery, request.message))
    logger.info(f"response : {response}")

    return response


async def read_movies():
    query = text("SELECT title FROM movie")
    async with engine.connect() as conn:
        result = await conn.execute(query)
        movies = [row[0] for row in result.fetchall()]
    return movies

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
