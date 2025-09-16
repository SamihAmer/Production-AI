from src.common.config import Settings
from src.iot_proxies.weather_proxy import WeatherProxy

def main():
    s = Settings()
    proxy = WeatherProxy(city=s.owm_city, api_key=s.owm_api_key,
                         iothub_device_conn_str=s.iothub_device_conn_str, device_id=s.iothub_device_id)
    msg = proxy.run_once()
    print("Weather sent:", msg)

if __name__ == "__main__":
    main()
