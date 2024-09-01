import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

from app.api.endpoints.infos import read_movies
from app.services.embeddings import KoBERTEmbeddings
from app.services.query_ai_process import vectorize_documents


logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.

    # 초기 1회 실행
    await vectorize()
    # 매일 1회 실행
    scheduler.start()

    yield


async def vectorize():
    logger.info("vectorize start")
    movies = await read_movies()
    embeddings_model = KoBERTEmbeddings()
    vectorize_documents(movies, embeddings_model, "faiss_vector", "jamo_vector")
    logger.info("vectorize success")


scheduler = AsyncIOScheduler()
# 시간 설정
trigger = CronTrigger(hour=9, minute=40)
scheduler.add_job(vectorize, trigger)