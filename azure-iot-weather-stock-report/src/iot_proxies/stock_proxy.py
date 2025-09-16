"""
StockProxy: fetch last price and publish to IoT Hub as device telemetry.
You can swap MarketStack with another provider by editing fetch_price().
"""
from __future__ import annotations
import time, requests
from typing import Dict, Any
from dataclasses import dataclass
from ..iothub.iot_client import IoTHubClient

@dataclass
class StockProxy:
    symbol: str
    marketstack_key: str
    iothub_device_conn_str: str
    device_id: str

    def fetch_price(self) -> Dict[str, Any]:
        url = "http://api.marketstack.com/v1/eod/latest"
        params = {"access_key": self.marketstack_key, "symbols": self.symbol}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        j = r.json()
        data = j["data"][0]
        return {"symbol": self.symbol, "last": float(data["close"])}

    def build_message(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "stock", "device_id": self.device_id, "ts": int(time.time()), "payload": payload}

    def run_once(self) -> Dict[str, Any]:
        payload = self.fetch_price()
        msg = self.build_message(payload)
        IoTHubClient(self.iothub_device_conn_str).send_message(msg)
        return msg
