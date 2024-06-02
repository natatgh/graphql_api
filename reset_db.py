from database import engine, Base

# Importar todos os modelos aqui
import models

def reset_database():
    Base.metadata.drop_all(bind=engine)  # Remove todas as tabelas
    Base.metadata.create_all(bind=engine)  # Recria todas as tabelas

if __name__ == "__main__":
    reset_database()
