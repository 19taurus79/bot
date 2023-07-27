from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine


DB = PostgresEngine(
    config={
        "database": "eridon_kharkiv_db",
        "user": "admin",
        "password": "root",
        "host": "195.189.226.96",
        "port": 5432,
    }
)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["pic.piccolo_app"])
