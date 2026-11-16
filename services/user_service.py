
from models.user import User


class UserService:

    # MENGAMBIL PROFIL PENGGUNA
    @staticmethod
    def ambil_profil(user_id):
        try:
            user = User(id=user_id)
            return user.ambil_profil()

        except Exception as error:
            print("Ambil profil error:", error)
            raise

    # MEMPERBARUI NAMA PENGGUNA
    @staticmethod
    def perbarui_nama(user_id, nama_baru):
        nama_baru = nama_baru.strip()

        if not nama_baru:
            return False, "Nama tidak boleh kosong."

        try:
            user = User(id=user_id)
            berhasil = user.perbarui_nama(nama_baru)

            if berhasil:
                return True, "Nama berhasil diperbarui!"

            return False, "Data pengguna tidak ditemukan."

        except Exception as error:
            print("Perbarui profil error:", error)
            return False, "Terjadi kesalahan saat memperbarui profil."
