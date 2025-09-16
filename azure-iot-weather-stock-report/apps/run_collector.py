import asyncio
from src.common.config import Settings
from src.collector.combine_service import DataCollectorCombine

def main():
    s = Settings()
    service = DataCollectorCombine(
        eventhub_conn_str=s.eventhub_conn_str,
        eventhub_name=s.eventhub_name,
        sb_conn_str=s.sb_conn_str,
        sb_topic=s.sb_topic
    )
    asyncio.run(service.run_forever())

if __name__ == "__main__":
    main()
