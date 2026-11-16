
from databases.koneksi import Database


class BodyHealthMap:

    def __init__(
        self,
        user_id=None,
        body_side=None,
        body_part=None,
        keluhan=None
    ):
        self.user_id = user_id
        self.body_side = body_side
        self.body_part = body_part
        self.keluhan = keluhan

    # MENYIMPAN KELUHAN
    def simpan_keluhan(self):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor()

            sql = """
                INSERT INTO body_health_reports
                (user_id, body_side, body_part, keluhan)
                VALUES (%s, %s, %s, %s)
            """

            values = (
                self.user_id,
                self.body_side,
                self.body_part,
                self.keluhan
            )

            cursor.execute(sql, values)
            db.commit()

            return True

        except Exception as error:
            if db:
                db.rollback()

            print("Simpan keluhan error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()

    # MENGAMBIL RIWAYAT KELUHAN
    @staticmethod
    def ambil_riwayat(user_id):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            sql = """
                SELECT
                    id,
                    body_side,
                    body_part,
                    keluhan,
                    created_at
                FROM body_health_reports
                WHERE user_id = %s
                ORDER BY created_at DESC
            """

            cursor.execute(sql, (user_id,))

            return cursor.fetchall()

        except Exception as error:
            print("Ambil riwayat keluhan error:", error)
            return []

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()

    # MENGAMBIL SATU KELUHAN BERDASARKAN ID
    @staticmethod
    def ambil_berdasarkan_id(laporan_id, user_id):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor(dictionary=True)

            sql = """
                SELECT id, body_side, body_part, keluhan, created_at
                FROM body_health_reports
                WHERE id = %s AND user_id = %s
            """

            cursor.execute(sql, (laporan_id, user_id))

            return cursor.fetchone()

        except Exception as error:
            print("Ambil keluhan berdasarkan ID error:", error)
            return None

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()

    # MEMPERBARUI KELUHAN
    def perbarui_keluhan(self, laporan_id):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor()

            sql = """
                UPDATE body_health_reports
                SET body_side = %s,
                    body_part = %s,
                    keluhan = %s
                WHERE id = %s AND user_id = %s
            """

            values = (
                self.body_side,
                self.body_part,
                self.keluhan,
                laporan_id,
                self.user_id
            )

            cursor.execute(sql, values)
            db.commit()

            return cursor.rowcount > 0

        except Exception as error:
            if db:
                db.rollback()

            print("Perbarui keluhan error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()

    # MENGHAPUS KELUHAN
    @staticmethod
    def hapus_keluhan(laporan_id, user_id):

        db = None
        cursor = None

        try:
            db = Database.koneksi()
            cursor = db.cursor()

            sql = """
                DELETE FROM body_health_reports
                WHERE id = %s AND user_id = %s
            """

            cursor.execute(sql, (laporan_id, user_id))
            db.commit()

            return cursor.rowcount > 0

        except Exception as error:
            if db:
                db.rollback()

            print("Hapus keluhan error:", error)
            return False

        finally:
            if cursor:
                cursor.close()

            if db:
                db.close()
