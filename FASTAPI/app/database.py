from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address>/hostname/<database_name>
SQLALCHEMY_DATABASE_URL = f'mysql+mysqldb://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# ##Esto sirve para hacer una conexion a la base de datos mysql pero hay que cambiar pequeñas cosas para usar otro motor
# ##Este codigo en si esta mal porque estamos mostrando nuestros datos de la base de datos
# while True:
#     try:
#         conn = mysql.connector.connect(host='localhost', database='fastapi', user="root ",
#                                        password="root",)
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SHOW DATABASES")
#         for bd in cursor:
#             print(bd)
#         print("Database connection was succesfull!!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)