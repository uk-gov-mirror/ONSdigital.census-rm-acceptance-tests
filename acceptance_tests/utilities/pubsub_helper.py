import json
import logging
from google.cloud import pubsub_v1

from structlog import wrap_logger

from config import Config

logger = wrap_logger(logging.getLogger(__name__))

subscriber = pubsub_v1.SubscriberClient()


def publish_to_pubsub(message, project, topic, **kwargs):
    publisher = pubsub_v1.PublisherClient()

    topic_path = publisher.topic_path(project, topic)

    future = publisher.publish(topic_path, data=message.encode('utf-8'), **kwargs)

    future.result(timeout=30)
    logger.info("Sent PubSub message", topic=topic, project=project)


def synchronous_consume_of_aims_pubsub_topic(context):
    subscription_path = subscriber.subscription_path(Config.AIMS_NEW_ADDRESS_PROJECT,
                                                     Config.AIMS_NEW_ADDRESS_SUBSCRIPTION)
    response = subscriber.pull(subscription_path, max_messages=1, timeout=30)
    context.aims_new_address_message = json.loads(response.received_messages[0].message.data)

    ack_ids = [message.ack_id for message in response.received_messages]

    subscriber.acknowledge(subscription_path, ack_ids)


def purge_aims_new_address_topic():
    max_messages = 100
    subscription_path = subscriber.subscription_path(Config.AIMS_NEW_ADDRESS_PROJECT,
                                                     Config.AIMS_NEW_ADDRESS_SUBSCRIPTION)
    response = subscriber.pull(subscription_path, max_messages=max_messages, timeout=5)

    # Temporary extra debug logging
    if response.received_messages:
        print('Messages purged from AIMs new address topic:')
        for message in response.received_messages:
            print(message.ack_id, message.message.data)

    ack_ids = [message.ack_id for message in response.received_messages]

    if ack_ids:
        subscriber.acknowledge(subscription_path, ack_ids)

    # It's possible (though unlikely) that they could be > max_messages on the topic so keep deleting till empty
    if len(response.received_messages) == max_messages:
        purge_aims_new_address_topic()
