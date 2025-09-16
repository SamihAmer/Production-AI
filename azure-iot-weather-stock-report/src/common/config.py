"""
Config helpers: loads environment variables (optionally via .env) and exposes a simple typed accessor.
"""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    # IoT Hub device (for proxies)
    iothub_device_conn_str: str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING", "")
    iothub_device_id: str = os.getenv("IOTHUB_DEVICE_ID", "")

    # IoT Hub Event Hub–compatible (for collector)
    eventhub_conn_str: str = os.getenv("EVENTHUB_CONN_STR", "")
    eventhub_name: str = os.getenv("EVENTHUB_NAME", "")

    # Service Bus
    sb_conn_str: str = os.getenv("SB_CONN_STR", "")
    sb_topic: str = os.getenv("SB_TOPIC", "weather-stock-topic")
    sb_subscription: str = os.getenv("SB_SUBSCRIPTION", "console-receiver")

    # External APIs
    owm_api_key: str = os.getenv("OWM_API_KEY", "")
    owm_city: str = os.getenv("OWM_CITY", "Seattle,US")
    marketstack_key: str = os.getenv("MARKETSTACK_KEY", "")
    stock_symbol: str = os.getenv("STOCK_SYMBOL", "MSFT")
