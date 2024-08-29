import logging

from fastapi import APIRouter

from app.api.dto.recommend_request import RecommendRequest
from app.models.recommend import Recommend

router = APIRouter()
logger = logging.getLogger("uvicorn")

@router.post("/recommend")
async def get_recommend(request: RecommendRequest) -> Recommend:
    logger.info(request)

    result = { "message" : "example message" }

    return Recommend(**result)