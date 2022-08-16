from pydantic import BaseSettings


class Settings(BaseSettings):
    MQTT_HOST: str = "vernemq"
    MQTT_PORT: int = 1883
    MQTT_TOPIC: str
    TEST_STOCK_ID: str = "1a06c5a3-6c44-4ffb-aa88-dc8acaf78df8"


settings = Settings()
