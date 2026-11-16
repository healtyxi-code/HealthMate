
from models.jurnal import JurnalKesehatan


class JurnalService:

    # MENAMBAHKAN JURNAL
    @staticmethod
    def tambah_jurnal(tanggal, berat, tidur, aktivitas, kondisi, user_id):
        jurnal = JurnalKesehatan(
            tanggal=tanggal,
            berat=berat,
            tidur=tidur,
            aktivitas=aktivitas,
            kondisi=kondisi,
            user_id=user_id
        )
        return jurnal.tambah_jurnal()

    # MENGAMBIL SEMUA JURNAL
    @staticmethod
    def ambil_semua(user_id, kata_kunci="", tanggal_filter=""):
        jurnal = JurnalKesehatan()
        return jurnal.ambil_semua(
            user_id=user_id,
            kata_kunci=kata_kunci,
            tanggal_filter=tanggal_filter
        )

    # MENCARI JURNAL BERDASARKAN ID
    @staticmethod
    def cari_berdasarkan_id(jurnal_id, user_id):
        jurnal = JurnalKesehatan()
        return jurnal.cari_berdasarkan_id(
            jurnal_id=jurnal_id,
            user_id=user_id
        )

    # MEMPERBARUI JURNAL
    @staticmethod
    def perbarui_jurnal(jurnal_id, user_id, tanggal, berat, tidur, aktivitas, kondisi):
        jurnal = JurnalKesehatan(
            tanggal=tanggal,
            berat=berat,
            tidur=tidur,
            aktivitas=aktivitas,
            kondisi=kondisi,
            user_id=user_id
        )
        return jurnal.perbarui(
            jurnal_id=jurnal_id,
            user_id=user_id
        )

    # MENGHAPUS JURNAL
    @staticmethod
    def hapus_jurnal(jurnal_id, user_id):
        jurnal = JurnalKesehatan()
        return jurnal.hapus(
            jurnal_id=jurnal_id,
            user_id=user_id
        )
