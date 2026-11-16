
from models.jurnal import JurnalKesehatan


class HealthService:

    # MENGAMBIL RINGKASAN DATA DASHBOARD
    @staticmethod
    def ambil_ringkasan(user_id):

        # Mengambil data melalui Model
        data = JurnalKesehatan.ambil_data_dashboard(user_id)

        # DATA UNTUK GRAFIK
        tanggal = []
        berat = []
        tidur = []

        for row in data:

            tanggal.append(
                row["tanggal"].strftime("%Y-%m-%d")
                if hasattr(row["tanggal"], "strftime")
                else str(row["tanggal"])
            )

            berat.append(
                float(row["berat"])
                if row["berat"] is not None else None
            )

            tidur.append(
                float(row["tidur"])
                if row["tidur"] is not None else None
            )

        # JUMLAH JURNAL
        jumlah_jurnal = len(data)

        # DATA TERBARU
        if data:

            data_terbaru = data[-1]

            berat_terbaru = (
                float(data_terbaru["berat"])
                if data_terbaru["berat"] is not None else None
            )

            tidur_terbaru = (
                float(data_terbaru["tidur"])
                if data_terbaru["tidur"] is not None else None
            )

            tanggal_terbaru = str(data_terbaru["tanggal"])

        else:

            berat_terbaru = None
            tidur_terbaru = None
            tanggal_terbaru = None

        # RATA-RATA BERAT BADAN
        data_berat = [
            float(row["berat"])
            for row in data
            if row["berat"] is not None
        ]

        rata_berat = (
            round(sum(data_berat) / len(data_berat), 1)
            if data_berat else 0
        )

        # RATA-RATA DURASI TIDUR
        data_tidur = [
            float(row["tidur"])
            for row in data
            if row["tidur"] is not None
        ]

        rata_tidur = (
            round(sum(data_tidur) / len(data_tidur), 1)
            if data_tidur else 0
        )

        # DAFTAR AKTIVITAS
        daftar_aktivitas = [
            row["aktivitas"]
            for row in data
            if row["aktivitas"]
            and row["aktivitas"].strip()
        ]

        # MENGEMBALIKAN DATA DASHBOARD
        return {
            "tanggal": tanggal,
            "berat": berat,
            "tidur": tidur,
            "jumlah_jurnal": jumlah_jurnal,
            "berat_terbaru": berat_terbaru,
            "tidur_terbaru": tidur_terbaru,
            "tanggal_terbaru": tanggal_terbaru,
            "rata_berat": rata_berat,
            "rata_tidur": rata_tidur,
            "daftar_aktivitas": daftar_aktivitas
        }
