import json

from fastapi import APIRouter
from sqlalchemy import text

from app.api.dto.additional_infos_request import AdditionalInfosRequest
from app.db.database import engine
from app.models.info import Info
from app.services.query_ai_process import vectorize_documents, process_documents_and_question, query_reprocess, generate_response, location_type
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn")


@router.get("/infos")
async def get_infos(message: str = "") -> Info:
    logger.info("get_infos start")
    logger.info(f"message : {message}")

    entities = json.loads(process_documents_and_question(message, "faiss_vector", "jamo_vector"))
    logger.info(f"entities : {entities}")

    if entities["region"] is not None:
        entities = location_type(entities)

    response: Info = Info(**json.loads(generate_response(entities)))
    logger.info(f"response : {response}")

    return response


@router.post("/infos/additional")
async def get_infos_additional(request: AdditionalInfosRequest) -> Info:
    logger.info("get_infos_additional start")
    logger.info(f"parsedQuery : {request.parsedQuery}")
    logger.info(f"message : {request.message}")

    entities = json.loads(query_reprocess(request.message, "faiss_vector", "jamo_vector", request.parsedQuery))
    logger.info(f"entities : {entities}")

    if entities["region"] is not None and not isinstance(entities["region"], list):
        entities = location_type(entities)

    response: Info = Info(**json.loads(generate_response(entities)))
    logger.info(f"response : {response}")

    return response


    # union_entities = union(request.parsedQuery, entities)
    # logger.info(f"union_entities : {union_entities}")
    #
    # response: Info = Info(**json.loads(generate_response(union_entities)))
    # logger.info(f"response : {response}")
    #
    # return response

#
# def union(parsedQuery, entities):
#     entity_info = [
#         ("movieName", "영화 제목"),
#         ("region", "지역"),
#         ("date", "날짜"),
#         ("time", "시간")
#     ]
#
#     for key, message in entity_info:
#         if getattr(parsedQuery, key):
#             entities[key] = getattr(parsedQuery, key)
#
#     return entities


async def read_movies():
    query = text("SELECT title FROM movie")
    async with engine.connect() as conn:
        result = await conn.execute(query)
        movies = [row[0] for row in result.fetchall()]
    return movies
