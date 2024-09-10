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
        "movieName": request.movieName,
        "region": request.region,
        "date": request.date,
        "time": request.time
    }

    recommendation = recommend_theaters(entities, request)
    logger.info(recommendation)

    result = {
        "message": recommendation
    }

    return Recommend(**result)