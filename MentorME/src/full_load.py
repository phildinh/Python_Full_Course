from sqlalchemy import create_engine

engine = create_engine(
    "mssql+pyodbc://PHIL\\SQLEXPRESS/mentorme"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

with engine.connect() as conn:
    print("Connected successfully!")