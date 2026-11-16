
import os
import mysql.connector
from dotenv import load_dotenv

# Membaca konfigurasi dari file .env
load_dotenv()


class Database:

    # KONEKSI DATABASE
    @staticmethod
    def koneksi():
        return mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "healthmate"),
            port=int(os.getenv("DB_PORT", "4000")),
            connection_timeout=20,
            ssl_ca=os.getenv("DB_SSL_CA"),
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

    # MEMERIKSA KONEKSI DATABASE
    @staticmethod
    def cek_koneksi():
        db = None

        try:
            db = Database.koneksi()

            if db.is_connected():
                print("Koneksi database HealthMate berhasil!")
                return True

            return False

        except mysql.connector.Error as error:
            print("Koneksi database gagal:", error)
            return False

        finally:
            if db is not None and db.is_connected():
                db.close()
