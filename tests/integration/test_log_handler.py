import logging

import pytest
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from kafka_handler import KafkaLogHandler


def test_handler_can_not_be_created_with_wrong_kafka_connection(topic):
    with pytest.raises(NoBrokersAvailable):
        KafkaLogHandler(topic=topic, bootstrap_servers="le_cool_host:1234")


def test_produced_logs_can_be_consumed(topic, kafka_server):
    consumer = KafkaConsumer(
        topic, bootstrap_servers=kafka_server, auto_offset_reset="latest"
    )
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(
        KafkaLogHandler(topic=topic, partition=0, bootstrap_servers=kafka_server)
    )

    logger.info("Well hello there Kafka service!")

    message = next(consumer)
    assert message
    assert isinstance(message.value, bytes)
    assert "hello there" in message.value.decode("utf-8")
