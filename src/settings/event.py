from typing import Callable
from fastapi import FastAPI
from loguru import logger

from src.services.database.postgresql.connector import PostgresConnector
from src.services.firebase.firebase import ServiceFirebase
from src.services.mailchimp.mailchimp import MailChimpService
from src.services.minio.minio_client import MinioClient
from src.services.redis.redis_client import RedisClient
from src.services.worker.worker import ServiceWorker
from src.services.parrot.cost_manager import APICostManager

from src.settings.config import APPLICATION

config = APPLICATION

service_worker = ServiceWorker(config=config)
redis_client = RedisClient(config=config)
postgres_client = PostgresConnector(config=config)
minio_client = MinioClient(config=config)
mailchimp_client = MailChimpService(config=config)
firebase_client = ServiceFirebase(certificate="./resources/firebase/flexstack-ai-firebase.json")

cost_manager = APICostManager(postgres_client=postgres_client)


def create_start_app_handler(app: FastAPI) -> Callable:  # noqa
    async def start_app():
        service_worker.start()
        redis_client.start()
        postgres_client.start()
        minio_client.start()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # noqa
    @logger.catch
    async def stop_app() -> None:
        service_worker.stop()
        redis_client.stop()
        postgres_client.stop()
        minio_client.stop()

    return stop_app
