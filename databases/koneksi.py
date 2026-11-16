
import os
import mysql.connector


class Database:

    @staticmethod
    def koneksi():
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "healthmate"),
            port=int(os.getenv("DB_PORT", "3306"))
        )

    @staticmethod
    def cek_koneksi():
        try:
            db = Database.koneksi()

            if db.is_connected():
                print("Koneksi database HealthMate berhasil!")

            db.close()
            return True

        except mysql.connector.Error as error:
            print("Koneksi database gagal:", error)
            return False
