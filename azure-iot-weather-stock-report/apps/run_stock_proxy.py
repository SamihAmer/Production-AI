from src.common.config import Settings
from src.iot_proxies.stock_proxy import StockProxy

def main():
    s = Settings()
    proxy = StockProxy(symbol=s.stock_symbol, marketstack_key=s.marketstack_key,
                       iothub_device_conn_str=s.iothub_device_conn_str, device_id=s.iothub_device_id)
    msg = proxy.run_once()
    print("Stock sent:", msg)

if __name__ == "__main__":
    main()
