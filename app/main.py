from fastapi import FastAPI
from .consumer import client
from .config import settings
from .routes import main_router
from .models.user import User

app = FastAPI()
app.include_router(main_router)


@app.on_event("startup")
async def startup_event():
    # Adding users
    User("ahmed"), User("ali"), User("khaled"), User("mohamed")

    # Connect to message queue & starting the loop in a new thread
    client.connect_async(settings.MQTT_HOST, settings.MQTT_PORT)
    client.loop_start()


@app.on_event("shutdown")
def shutdown_event():
    client.loop_stop()
