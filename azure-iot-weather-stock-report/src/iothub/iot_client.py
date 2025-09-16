"""
IoTHubClient: thin wrapper over azure-iot-device (device → cloud) for sending messages,
and azure-eventhub (consumer) for reading the IoT Hub's Event Hub–compatible endpoint.
"""
import json
import logging
from typing import AsyncIterator, Dict, Any

from azure.iot.device import IoTHubDeviceClient, Message
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub import EventData

logger = logging.getLogger(__name__)

class IoTHubClient:
    """
    For proxies: instantiate with a device connection string and call send_message().
    For collector: use the @classmethod create_eventhub_consumer to read device telemetry.
    """

    def __init__(self, device_connection_string: str):
        self._device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    def send_message(self, body: Dict[str, Any]) -> None:
        """Sends a JSON message to IoT Hub as device telemetry."""
        msg = Message(json.dumps(body))
        msg.content_type = "application/json"
        msg.content_encoding = "utf-8"
        logger.info("Sending IoT message: %s", body)
        self._device_client.connect()
        try:
            self._device_client.send_message(msg)
        finally:
            self._device_client.disconnect()

    @classmethod
    def create_eventhub_consumer(cls, conn_str: str, eventhub_name: str, consumer_group: str = "$Default") -> EventHubConsumerClient:
        """Creates an EventHubConsumerClient to read from IoT Hub's Event Hub–compatible endpoint."""
        return EventHubConsumerClient.from_connection_string(conn_str, eventhub_name=eventhub_name, consumer_group=consumer_group)

    @staticmethod
    async def iter_events(consumer: EventHubConsumerClient, partition_id: str = None) -> AsyncIterator[EventData]:
        """Async generator yielding EventData."""
        async with consumer:
            async def on_event(partition_context, event):
                yield event  # not used directly; see run() usage

            # We expose consumer for caller to handle receiving loop (see combine_service.py).
            raise NotImplementedError("Use EventHubConsumerClient.receive with your own callbacks.")
