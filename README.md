# Kafka Python Log Handler
Handler for the standard `logging` module which puts logs through to Kafka.
The current implementation is very basic to accommodate our needs, but additional functionality may be coming when the parent project grows.

## Install
This was developed in Python 3.6.7, using `kafka-python` 1.4.3 and Kafka 2.12

#### Development
Tests will try to connect to a Kafka instance via the defaults.
Optionally setting `KAFKA_HOST` and `KAFKA_PORT` to the appropriate location on your machine will change this.

Install the dev requirements

        $ pip install -r requirements-dev.txt

Set the pre-commit hook

        $ pre-commit install

## How to use
The only necessary thing to create this handler is a `topic` to push the values to.
Optionally, a `key` and/or `partition` may be provided.
Any additional keyword-value configuration provided to the Handler will be used to initialize the `kafka.KafkaProducer`.

To add a handler to the python logger is very simple:

```python
import logging


from kafka_handler import KafkaLogHandler

handler = KafkaLogHandler(topic="example_topic", key="example_key")  # Default parameters for Kafka connection are used

logger = logging.getLogger()  # No name gives you the root logger
logger.setLevel("WARNING")
logger.addHandler(example_handler)

logger.warning("This will push this message to the 'example_topic' in Kafka.")
```

### Configuring Kafka Connection
By default each handler will create a `kafka.KafkaProducer` instance, passing on each argument from their `__init__(**kwargs)` to the KafkaProducer's instantiation.
This means you can configure the connection as specific as you'd like, but every argument should be provided with its keyword; `Handler(host="localhost")` instead of `Handler("localhost")`.
All available configuration options are available in the [kafka-python documentation](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html).

```python
handler = KafkaLogHandler(topic="topic", bootstrap_servers="other_host:9092", retries=0)
```

### Configure message logging
Every handler has the `raw_logging` option which can be provided optionally.
Omitting it from the initialisation, will default it to `False`, meaning the message being logged will be purely what's sent.
If you set it to `True`, first the content will be logged, then appended to the line number and finally the pathname.

```python
raw_handler = KafkaLogHandler(topic="topic", raw_logging=True)
...
logging.info("Test message")
```
A pure handler would emit a message like so: `Test message.`,  
the `raw_handler` however, will emit a message like so: `Test message. - 2: /.../file.py`.
