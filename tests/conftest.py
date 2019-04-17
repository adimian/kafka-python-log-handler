import os

import kafka
import pytest


def get_kafka_env_vars() -> str:
    host = os.getenv("KAFKA_HOST") or "localhost"
    port = os.getenv("KAFKA_PORT") or "9092"
    return f"{host}:{port}"


@pytest.fixture
def kafka_server() -> str:
    return get_kafka_env_vars()


@pytest.fixture
def producer() -> kafka.KafkaProducer:
    server = get_kafka_env_vars()

    return kafka.KafkaProducer(bootstrap_servers=server, retries=0, max_block_ms=1000)


@pytest.fixture
def topic() -> str:
    return "kafka-log-handler-topic"


@pytest.fixture
def mock_kafka_producer(monkeypatch):
    monkeypatch.setattr(
        kafka.client_async.KafkaClient, "check_version", lambda *args, **kwargs: (0, 10)
    )
    monkeypatch.setattr(
        kafka.KafkaProducer, "send", lambda *args, **kwargs: print(kwargs)
    )
