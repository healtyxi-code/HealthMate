
from databases.koneksi import Database


class JurnalKesehatan:

    def __init__(
        self,
        id=None,
        tanggal=None,
        berat=None,
        tidur=None,
        aktivitas=None,
        kondisi=None,
        user_id=None
    ):
        self.id = id
        self.tanggal = tanggal
        self.berat = berat
        self.tidur = tidur
        self.aktivitas = aktivitas
        self.kondisi = kondisi
        self.user_id = user_id

    # MENAMBAHKAN JURNAL
    def tambah_jurnal(self):
        db = Database.koneksi()
        cursor = db.cursor()

        try:
            sql = """
                INSERT INTO jurnal_kesehatan
                (tanggal, berat, tidur, aktivitas, kondisi, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            nilai = (
                self.tanggal,
                self.berat,
                self.tidur,
                self.aktivitas,
                self.kondisi,
                self.user_id
            )

            cursor.execute(sql, nilai)
            db.commit()

            return True

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    # MENAMPILKAN DAN MENCARI JURNAL
    def ambil_semua(
        self,
        user_id,
        kata_kunci="",
        tanggal_filter=""
    ):
        db = Database.koneksi()
        cursor = db.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM jurnal_kesehatan
                WHERE user_id = %s
            """

            nilai = [user_id]

            if kata_kunci:
                sql += """
                    AND (aktivitas LIKE %s OR kondisi LIKE %s)
                """

                nilai.extend([
                    "%" + kata_kunci + "%",
                    "%" + kata_kunci + "%"
                ])

            if tanggal_filter:
                sql += " AND tanggal = %s"
                nilai.append(tanggal_filter)

            sql += " ORDER BY id DESC"

            cursor.execute(sql, tuple(nilai))
            data = cursor.fetchall()

            return data

        finally:
            cursor.close()
            db.close()

    # MENCARI JURNAL BERDASARKAN ID
    def cari_berdasarkan_id(self, jurnal_id, user_id):
        db = Database.koneksi()
        cursor = db.cursor(dictionary=True)

        try:
            sql = """
                SELECT *
                FROM jurnal_kesehatan
                WHERE id = %s AND user_id = %s
            """

            cursor.execute(sql, (jurnal_id, user_id))
            return cursor.fetchone()

        finally:
            cursor.close()
            db.close()

    # MEMPERBARUI JURNAL
    def perbarui(self, jurnal_id, user_id):
        db = Database.koneksi()
        cursor = db.cursor()

        try:
            sql = """
                UPDATE jurnal_kesehatan
                SET tanggal = %s,
                    berat = %s,
                    tidur = %s,
                    aktivitas = %s,
                    kondisi = %s
                WHERE id = %s AND user_id = %s
            """

            nilai = (
                self.tanggal,
                self.berat,
                self.tidur,
                self.aktivitas,
                self.kondisi,
                jurnal_id,
                user_id
            )

            cursor.execute(sql, nilai)
            db.commit()

            return cursor.rowcount > 0

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    # MENGHAPUS JURNAL
    def hapus(self, jurnal_id, user_id):
        db = Database.koneksi()
        cursor = db.cursor()

        try:
            sql = """
                DELETE FROM jurnal_kesehatan
                WHERE id = %s AND user_id = %s
            """

            cursor.execute(sql, (jurnal_id, user_id))
            db.commit()

            return cursor.rowcount > 0

        except Exception:
            db.rollback()
            raise

        finally:
            cursor.close()
            db.close()

    # MENGAMBIL DATA JURNAL UNTUK DASHBOARD
    @staticmethod
    def ambil_data_dashboard(user_id):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT tanggal, berat, tidur, aktivitas, kondisi
                FROM jurnal_kesehatan
                WHERE user_id = %s
                ORDER BY tanggal ASC, id ASC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()