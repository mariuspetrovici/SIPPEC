import psycopg2
from psycopg2 import sql
import os

def create_database():
    try:
        # Conectare la PostgreSQL (fără specificarea bazei de date)
        conn = psycopg2.connect(
            dbname="postgres",  # Conectare la baza de date implicită
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "postgres"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432")
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Verifică dacă baza de date există
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='sippec_db'")
        exists = cursor.fetchone()

        if not exists:
            # Creare baza de date
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("sippec_db")))
            print("Baza de date 'sippec_db' a fost creată.")

            # Creare utilizator și setare parolă
            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier("sippec_user")), ["sippec_password"])
            print("Utilizatorul 'sippec_user' a fost creat.")

            # Acordare drepturi
            cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier("sippec_db"),
                sql.Identifier("sippec_user")
            ))
            print("Drepturile au fost acordate.")
        else:
            print("Baza de date 'sippec_db' există deja.")

    except Exception as e:
        print(f"Eroare: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    create_database()