
from databases.koneksi import Database


class User:

    def __init__(self, id=None, nama=None, email=None):
        self.id = id
        self.nama = nama
        self.email = email

    # MENCARI PENGGUNA BERDASARKAN EMAIL
    @classmethod
    def cari_berdasarkan_email(cls, email):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, nama, email
                FROM users
                WHERE email = %s
            """, (email,))

            data = cursor.fetchone()

            if data:
                return cls(
                    id=data["id"],
                    nama=data["nama"],
                    email=data["email"]
                )

            return None

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    # MENGAMBIL DATA PENGGUNA UNTUK LOGIN
    @staticmethod
    def ambil_data_login(email):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, nama, email, password
                FROM users
                WHERE email = %s
            """, (email,))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    # MENAMBAHKAN PENGGUNA BARU
    @staticmethod
    def tambah_user(nama, email, password_hash):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO users (nama, email, password)
                VALUES (%s, %s, %s)
            """, (nama, email, password_hash))

            db.commit()
            return True

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    # MENCARI PENGGUNA BERDASARKAN ID
    @classmethod
    def cari_berdasarkan_id(cls, user_id):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, nama, email
                FROM users
                WHERE id = %s
            """, (user_id,))

            data = cursor.fetchone()

            if data:
                return cls(
                    id=data["id"],
                    nama=data["nama"],
                    email=data["email"]
                )

            return None

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    # MENGAMBIL PROFIL PENGGUNA
    def ambil_profil(self):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, nama, email
                FROM users
                WHERE id = %s
            """, (self.id,))

            return cursor.fetchone()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

    # MEMPERBARUI NAMA PENGGUNA
    def perbarui_nama(self, nama_baru):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor()

            cursor.execute("""
                UPDATE users
                SET nama = %s
                WHERE id = %s
            """, (nama_baru, self.id))

            db.commit()

            berhasil = cursor.rowcount > 0
            self.nama = nama_baru

            return berhasil

        except Exception:
            if db:
                db.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()
