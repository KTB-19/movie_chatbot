import logging

from fastapi import APIRouter

from app.api.dto.recommend_request import RecommendRequest
from app.models.recommend import Recommend
from app.services.recommend_response import recommend_theaters

router = APIRouter()
logger = logging.getLogger("uvicorn")

@router.post("/recommend")
async def get_recommend(request: RecommendRequest) -> Recommend:
    logger.info(request)

    entities = {
        "movieName": "2023 심규선 단독 콘서트 : 우리 앞의 세계",
        "region": "성남시 분당구",
        "date": "2024-08-19",
        "time": "15:00"
    }

    recommendation = recommend_theaters(entities, request)
    logger.info(recommendation)

    result = {
        "message": recommendation
    }

    return Recommend(**result)