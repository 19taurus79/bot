from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
import os
from dotenv import load_dotenv
load_dotenv()
DB = PostgresEngine(
    config={
        "database": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST"),
        "port": os.getenv("POSTGRES_PORT"),
    }
)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["pic.piccolo_app"])
