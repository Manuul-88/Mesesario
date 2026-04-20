#conecta con sqlite
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./mesesario.db" #crea un archivo sqlite en el proyecto

engine = create_engine( #cinecta con la bd
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #abre sesiones para consultar y guardar
Base = declarative_base() #sirve para definir tablas