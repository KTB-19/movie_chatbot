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
