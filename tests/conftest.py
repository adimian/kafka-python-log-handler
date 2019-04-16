import pytest
import kafka


@pytest.fixture
def producer() -> kafka.KafkaProducer:
    return kafka.KafkaProducer(
        bootstrap_servers="localhost:9092", retries=0, max_block_ms=1000
    )


@pytest.fixture
def topic() -> str:
    return "kafka-log-handler-topic"
