"""
DataCollectorCombine: consume from IoT Hub Event Hub–compatible endpoint, combine latest weather & stock,
then publish a single report to Service Bus topic.
"""
from __future__ import annotations
import asyncio, json, logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from azure.eventhub.aio import EventHubConsumerClient
from ..servicebus.sb_client import ServiceBusTopicClient

logger = logging.getLogger(__name__)

@dataclass
class DataCollectorCombine:
    eventhub_conn_str: str
    eventhub_name: str
    sb_conn_str: str
    sb_topic: str

    cache: Dict[str, Any] = field(default_factory=dict)

    def _try_publish(self, sb: ServiceBusTopicClient) -> None:
        weather = self.cache.get("weather")
        stock = self.cache.get("stock")
        if weather and stock:
            report = {
                "weather": weather["payload"],
                "stock": stock["payload"],
                "ts": max(weather["ts"], stock["ts"]),
                "summary": f"Weather: {weather['payload']['condition']}, Temperature: {weather['payload']['temp_c']}°C, humidity: {weather['payload']['humidity']} | Stock {stock['payload']['symbol']}: {stock['payload']['last']}"
            }
            sb.send(report)
            logger.info("Published combined report to SB topic")

    async def _on_event(self, partition_context, event):
        try:
            body = json.loads(event.body_as_str())
            msg_type = body.get("type")
            if msg_type in ("weather", "stock"):
                self.cache[msg_type] = body
                logger.info("Cached %s update from IoT Hub", msg_type)
        except Exception:
            logger.exception("Failed to parse event")
        finally:
            await partition_context.update_checkpoint(event)

    async def run_forever(self) -> None:
        sb = ServiceBusTopicClient(self.sb_conn_str, self.sb_topic)
        consumer: EventHubConsumerClient = EventHubConsumerClient.from_connection_string(
            self.eventhub_conn_str, eventhub_name=self.eventhub_name, consumer_group="$Default"
        )
        async with consumer:
            async def callback(partition_context, event):
                await self._on_event(partition_context, event)
                self._try_publish(sb)

            await consumer.receive(on_event=callback, starting_position="-1")  # from beginning
