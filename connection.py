from sqlalchemy import create_engine

# engine = create_engine("postgresql+psycopg2://admin:root@localhost:5432/test_db")
engine = create_engine(
    "postgresql+psycopg2://admin:root@195.189.226.96:5432/eridon_kharkiv_db"
)

if __name__ == "__main__":
    print(engine)
