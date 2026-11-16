
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User


class AuthService:

    # PROSES REGISTRASI
    @staticmethod
    def registrasi(nama, email, password):

        nama = nama.strip()
        email = email.strip().lower()

        if not nama or not email or not password:
            return False, "Semua kolom wajib diisi."

        if len(password) < 8:
            return False, "Password minimal 8 karakter."

        try:
            # MEMERIKSA EMAIL
            user_lama = User.cari_berdasarkan_email(email)

            if user_lama:
                return False, "Email sudah terdaftar."

            # MENGENKRIPSI PASSWORD
            password_hash = generate_password_hash(password)

            # MENYIMPAN PENGGUNA
            berhasil = User.tambah_user(
                nama,
                email,
                password_hash
            )

            if berhasil:
                return True, "Registrasi berhasil!"

            return False, "Registrasi gagal."

        except Exception as error:
            print("Registrasi Service error:", error)
            return False, "Terjadi kesalahan saat registrasi."

    # PROSES LOGIN
    @staticmethod
    def login(email, password):

        email = email.strip().lower()

        if not email or not password:
            return None

        try:
            # MENGAMBIL DATA PENGGUNA
            user = User.ambil_data_login(email)

            if not user:
                return None

            # MEMERIKSA PASSWORD
            if check_password_hash(user["password"], password):
                return user

            return None

        except Exception as error:
            print("Login Service error:", error)
            raise
