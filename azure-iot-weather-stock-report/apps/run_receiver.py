from src.common.config import Settings
from src.receiver.dummy_receiver import DummyReceiver

def main():
    s = Settings()
    DummyReceiver(s.sb_conn_str, s.sb_topic, s.sb_subscription).run()

if __name__ == "__main__":
    main()
