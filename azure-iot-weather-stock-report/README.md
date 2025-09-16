# Azure IoT → Data Collector → Service Bus (Topics) → Dummy Receiver

## Python system architecture: 
1. Fetches **current weather** and a **stock price** via two *IoT proxies*.
2. Sends those proxy readings to **Azure IoT Hub** (`dev-jhu-aiclass-iothub-classhub1`).
3. A **Data Collector Combine** service consumes from the IoT Hub *Event Hub–compatible* endpoint, merges the latest weather + stock messages into a single report.
4. The report is published to an **Azure Service Bus Topic**.
5. A **Dummy Receiver** subscribes to the topic and prints a one‑line summary in the terminal.

See below the **4 components**, each with a clear API class and comments.

```
src/
  common/config.py                  # .env + CLI/env config helpers
  iothub/iot_client.py              # IoTHubClient API (send/receive abstractions)
  servicebus/sb_client.py           # ServiceBusTopicClient API
  receiver/dummy_receiver.py        # DummyReceiver API

  iot_proxies/weather_proxy.py      # WeatherProxy API (fetch + send to IoT Hub)
  iot_proxies/stock_proxy.py        # StockProxy API (fetch + send to IoT Hub)

  collector/combine_service.py      # DataCollectorCombine API (read IoT Hub, combine, publish to Topic)
apps/
  run_weather_proxy.py              # Entrypoint for weather proxy
  run_stock_proxy.py                # Entrypoint for stock proxy
  run_collector.py                  # Entrypoint for data collector
  run_receiver.py                   # Entrypoint for dummy receiver
```

## Prerequisites

- Python 3.10+
- Azure resources access:
  - **IoT Hub** (device identity created): `dev-jhu-aiclass-iothub-classhub1`
  - **Event Hub–compatible endpoint** (read access) for the IoT Hub
  - **Service Bus** namespace with a **Topic** and a **Subscription**
- API keys:
  - **OpenWeatherMap** (Current Weather API): https://openweathermap.org/current
  - **MarketStack** (Free stock data API): https://marketstack.com/ (or substitute your provider)

## Install

```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```ini
# --- IoT Hub device (for proxies) ---
IOTHUB_DEVICE_CONNECTION_STRING="HostName=...;DeviceId=...;SharedAccessKey=..."
IOTHUB_DEVICE_ID="your-device-id"

# --- IoT Hub Event Hub–compatible (for collector) ---
EVENTHUB_CONN_STR="Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=..."
EVENTHUB_NAME="your-eventhub-name"  # from IoT Hub's Event Hub–compatible name

# --- Service Bus Topic ---
SB_CONN_STR="Endpoint=sb://...;SharedAccessKeyName=...;SharedAccessKey=..."
SB_TOPIC="weather-stock-topic"
SB_SUBSCRIPTION="console-receiver"

# --- External APIs ---
OWM_API_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OWM_CITY="Seattle,US"          # choose your city
STOCK_SYMBOL="MSFT"            # pick your stock symbol
MARKETSTACK_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


## Run

Open **four** terminals (or run in background), one per component. Order is flexible; the collector and receiver can run before messages arrive.

### 1) Weather Proxy
```bash
python -m apps.run_weather_proxy
```

### 2) Stock Proxy
```bash
python -m apps.run_stock_proxy
```

### 3) Data Collector Combine
Consumes from IoT Hub’s Event Hub–compatible endpoint and publishes combined reports to Service Bus.
```bash
python -m apps.run_collector
```

### 4) Dummy Receiver
Subscribes to the Service Bus Topic and prints a one‑liner.
```bash
python -m apps.run_receiver
```

### Example Output (Receiver)
```
Weather: Rainy, Temperature: 17.2°C, humidity: 82 | Stock MSFT: 405.31
```

## Design Notes

- **Clear API classes** (one per component) with docstrings:
  - `WeatherProxy` and `StockProxy` fetch from REST, then **send telemetry** with `IoTHubClient.send_message()`.
  - `DataCollectorCombine` **reads** IoT events via Event Hub client, updates an in‑memory cache of latest readings, and when both are present, **publishes** a merged JSON to the Service Bus **topic**.
  - `DummyReceiver` **subscribes** to the topic and prints.
- **Message format:** each proxy sends JSON with a `type` field: `"weather"` or `"stock"`, plus `payload` and `ts`.
- **Resilience:** simple retry/backoff and graceful shutdown with Ctrl‑C.
- **Separation of concerns:** Azure SDK clients are wrapped in thin adapters (`IoTHubClient`, `ServiceBusTopicClient`) so the business logic stays testable.
