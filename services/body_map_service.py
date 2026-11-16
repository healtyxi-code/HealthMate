
from models.body_map import BodyHealthMap


class BodyHealthMapService:

    # MENYIMPAN KELUHAN PENGGUNA
    @staticmethod
    def simpan_keluhan(user_id, body_side, body_part, keluhan):

        if not user_id:
            return False, "Pengguna belum login."

        if body_side not in ["depan", "belakang"]:
            return False, "Pilihan tampak tubuh tidak valid."

        if not body_part or not body_part.strip():
            return False, "Silakan pilih bagian tubuh."

        if not keluhan or not keluhan.strip():
            return False, "Keluhan harus diisi."

        laporan = BodyHealthMap(
            user_id=user_id,
            body_side=body_side,
            body_part=body_part.strip(),
            keluhan=keluhan.strip()
        )

        berhasil = laporan.simpan_keluhan()

        if berhasil:
            return True, "Keluhan berhasil disimpan."

        return False, "Keluhan gagal disimpan."

    # MENGAMBIL RIWAYAT KELUHAN
    @staticmethod
    def ambil_riwayat(user_id):

        if not user_id:
            return []

        return BodyHealthMap.ambil_riwayat(user_id)

    # MENGAMBIL SATU KELUHAN
    @staticmethod
    def ambil_berdasarkan_id(laporan_id, user_id):

        if not user_id or not laporan_id:
            return None

        return BodyHealthMap.ambil_berdasarkan_id(
            laporan_id,
            user_id
        )

    # MEMPERBARUI KELUHAN
    @staticmethod
    def perbarui_keluhan(
        laporan_id,
        user_id,
        body_side,
        body_part,
        keluhan
    ):

        if not user_id:
            return False, "Pengguna belum login."

        if not laporan_id:
            return False, "Data keluhan tidak ditemukan."

        if body_side not in ["depan", "belakang"]:
            return False, "Pilihan tampak tubuh tidak valid."

        if not body_part or not body_part.strip():
            return False, "Silakan pilih bagian tubuh."

        if not keluhan or not keluhan.strip():
            return False, "Keluhan harus diisi."

        laporan = BodyHealthMap(
            user_id=user_id,
            body_side=body_side,
            body_part=body_part.strip(),
            keluhan=keluhan.strip()
        )

        berhasil = laporan.perbarui_keluhan(laporan_id)

        if berhasil:
            return True, "Keluhan berhasil diperbarui."

        return False, "Keluhan gagal diperbarui atau tidak ditemukan."

    # MENGHAPUS KELUHAN
    @staticmethod
    def hapus_keluhan(laporan_id, user_id):

        if not user_id:
            return False, "Pengguna belum login."

        if not laporan_id:
            return False, "Data keluhan tidak ditemukan."

        berhasil = BodyHealthMap.hapus_keluhan(
            laporan_id,
            user_id
        )

        if berhasil:
            return True, "Keluhan berhasil dihapus."

        return False, "Keluhan gagal dihapus atau tidak ditemukan."
