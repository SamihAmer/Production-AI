"""
ServiceBusTopicClient: thin wrapper to send and receive messages via a Topic.
"""
import json
import logging
from typing import Dict, Any, Callable

from azure.servicebus import ServiceBusMessage
from azure.servicebus import ServiceBusClient

logger = logging.getLogger(__name__)

class ServiceBusTopicClient:
    def __init__(self, connection_string: str, topic_name: str, subscription_name: str | None = None):
        self._conn_str = connection_string
        self._topic = topic_name
        self._subscription = subscription_name

    def send(self, body: Dict[str, Any]) -> None:
        with ServiceBusClient.from_connection_string(self._conn_str) as sb:
            sender = sb.get_topic_sender(topic_name=self._topic)
            with sender:
                msg = ServiceBusMessage(json.dumps(body))
                logger.info("Publishing to SB topic '%s': %s", self._topic, body)
                sender.send_messages(msg)

    def receive_forever(self, on_message: Callable[[Dict[str, Any]], None]) -> None:
        assert self._subscription, "Subscription name required for receiving"
        with ServiceBusClient.from_connection_string(self._conn_str) as sb:
            receiver = sb.get_subscription_receiver(topic_name=self._topic, subscription_name=self._subscription, max_wait_time=None)
            with receiver:
                for msg in receiver:
                    try:
                        body = json.loads(str(msg))
                        on_message(body)
                        receiver.complete_message(msg)
                    except Exception as exc:
                        logger.exception("Failed to process message: %s", exc)
                        receiver.abandon_message(msg)
