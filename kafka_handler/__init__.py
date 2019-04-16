import logging
from typing import Any, Optional

import kafka


ENCODING = "utf-8"


class KafkaLogHandler(logging.StreamHandler):
    def __init__(
        self,
        topic: str,
        key: Optional[str] = None,
        partition: Optional[int] = None,
        raw_logging: bool = False,
        **kwargs: Any,
    ):
        super().__init__()
        self.topic = topic
        self.key = key.encode(ENCODING) if key else None
        self.partition = partition
        self.raw_logging = raw_logging

        self.producer = kafka.KafkaProducer(**kwargs)

    def emit(self, message: logging.LogRecord):
        def _create_dict_without_none_values(**kwargs: Any) -> dict:
            result = {}

            for k, v in kwargs.items():
                if v is not None:
                    result[k] = v

            return result

        value = message.msg
        if self.raw_logging:
            value += f" - {message.lineno}: {message.pathname}"

        self.producer.send(
            **_create_dict_without_none_values(
                topic=self.topic,
                value=value.encode(ENCODING),
                key=self.key.encode(ENCODING),
                partition=self.partition,
            )
        )
