from types import FunctionType
from typing import Optional

import kafka
import pytest


def explore(func: FunctionType, msg_on_fail: Optional[str] = None):
    """Takes a function to execute and will fail if any exception occurs"""
    try:
        func()
    except:
        pytest.fail(msg_on_fail)


def test_create_consumer_and_producer_with_defaults():
    explore(
        lambda: kafka.KafkaProducer() and kafka.KafkaConsumer(),
        "Failed to create default Kafka Producer.",
    )


def test_create_consumer_and_producer_with_bootstrap_servers(kafka_server):
    explore(
        lambda: kafka.KafkaProducer(bootstrap_servers=kafka_server)
        and kafka.KafkaConsumer(bootstrap_servers=kafka_server),
        "Failed to create server-bootstrapped Kafka Producer.",
    )


def test_send_msg_with_topic_as_string(producer, topic):
    explore(
        lambda: producer.send(topic=topic, value=b"test_message"),
        "Failed to send message to Kafka.",
    )


def test_send_msg_with_value_as_bytes(producer, topic):
    explore(
        lambda: producer.send(topic=topic, value=b"test_message"),
        "Failed to send message to Kafka.",
    )


def test_send_msg_with_key(producer, topic):
    explore(
        lambda: producer.send(topic=topic, key=b"testing_key", value=b"testing_value"),
        "Failed to send partitioned message.",
    )


def test_consume_msgs_from_topic(producer, topic, kafka_server):
    def _consume_msgs():
        producer.send(topic, value=b"A message.")
        consumer = kafka.KafkaConsumer(
            topic, bootstrap_servers=kafka_server, auto_offset_reset="earliest"
        )

        msg = next(consumer)
        assert msg
        assert isinstance(msg.topic, str)
        assert isinstance(msg.value, bytes)

        msgs = consumer.poll(timeout_ms=300)
        assert msgs

    explore(_consume_msgs, "Failed to consume messages.")
