import logging

from kafka import KafkaConsumer

from kafka_handler import KafkaLogHandler


def test_produced_logs_can_be_consumed(topic):
    consumer = KafkaConsumer(topic, auto_offset_reset="latest")
    logger = logging.getLogger("logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(KafkaLogHandler(topic=topic, partition=0))

    logger.info("Well hello there Kafka service!")

    message = next(consumer)
    assert message
    assert isinstance(message.value, bytes)
    assert "hello there" in message.value.decode("utf-8")
