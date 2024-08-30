import logging

from fastapi import APIRouter

from app.api.dto.recommend_request import RecommendRequest
from app.models.recommend import Recommend

router = APIRouter()
logger = logging.getLogger("uvicorn")

@router.post("/recommend")
async def get_recommend(request: RecommendRequest) -> Recommend:
    logger.info(request)

    result = { "message" : """
    example message 입니다.
    현재 위치에서 가장 가까운 영화관들 중에서 추천드릴 수 있는 영화관은 다음과 같습니다:
    1. CGV 구리
       - 영화: 2023 심규선 단독 콘서트 : 우리 앞의 세계
       - 상영 시간: 15:00, 16:00
       - 총 2회 상영
       - 위치: 구리역 1번 출구에서 도보로 3분 거리

    2. 메가박스 구리
       - 영화: 2023 심규선 단독 콘서트 : 우리 앞의 세계
       - 상영 시간: 17:00, 18:00
       - 총 2회 상영
       - 위치: 동구릉역 2번 출구에서 도보로 5분 거리

    각 영화관 위치에 대한 설명과 대중교통을 이용한 접근법을 참고해주세요. 좋은 영화 감상하시길 바랍니다!
    """ }

    return Recommend(**result)