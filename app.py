from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

# IMPORT CLASS OOP
from services.auth_service import AuthService
from services.health_service import HealthService
from services.user_service import UserService
from services.jurnal_service import JurnalService
from services.body_map_service import BodyHealthMapService

# MEMBUAT APLIKASI FLASK
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv(
    "SECRET_KEY",
    "healthmate_development_key"
)

# MEMERIKSA LOGIN
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# HALAMAN UTAMA
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


# REGISTRASI
@app.route("/register", methods=["GET", "POST"])
def register():
    pesan_error = None

    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not nama or not email or not password:
            pesan_error = "Semua kolom wajib diisi."

        elif len(password) < 8:
            pesan_error = "Password minimal 8 karakter."

        else:
            try:
                berhasil, pesan = AuthService.registrasi(
                    nama, email, password
                )

                if berhasil:
                    return redirect(url_for("login"))
                else:
                    pesan_error = pesan

            except Exception as error:
                print("Registrasi error:", error)
                pesan_error = "Registrasi gagal. Silakan coba lagi."

    return render_template(
        "register.html",
        pesan_error=pesan_error
    )

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    pesan_error = None

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        try:
            user = AuthService.login(email, password)

            if user:
                session.clear()
                session["user_id"] = user["id"]
                session["nama"] = user["nama"]
                session["email"] = user["email"]

                return redirect(url_for("dashboard"))

            else:
                pesan_error = "Email atau password salah."

        except Exception as error:
            print("Login error:", error)
            pesan_error = "Terjadi kesalahan saat login."

    return render_template(
        "login.html",
        pesan_error=pesan_error
    )

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



# HALAMAN PROFIL PENGGUNA
@app.route("/profil", methods=["GET", "POST"])
@login_required
def profil():

    pesan_sukses = None
    pesan_error = None

    try:
        data_user = UserService.ambil_profil(
            session["user_id"]
        )

        if data_user is None:
            session.clear()
            return redirect(url_for("login"))

        if request.method == "POST":

            nama_baru = request.form.get("nama", "").strip()

            berhasil, pesan = UserService.perbarui_nama(
                session["user_id"],
                nama_baru
            )

            if berhasil:
                session["nama"] = nama_baru
                data_user["nama"] = nama_baru
                pesan_sukses = pesan
            else:
                pesan_error = pesan

        return render_template(
            "profile.html",
            user=data_user,
            pesan_sukses=pesan_sukses,
            pesan_error=pesan_error
        )

    except Exception as error:
        print("Profil error:", error)

        return "Terjadi kesalahan saat membuka profil.", 500

# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    try:
        ringkasan = HealthService.ambil_ringkasan(
            session["user_id"]
        )

        # Mengambil riwayat Body Health Map
        riwayat_keluhan = BodyHealthMapService.ambil_riwayat(
            session["user_id"]
        )

        # Mengambil keluhan terbaru
        keluhan_terakhir = (
            riwayat_keluhan[0] if riwayat_keluhan else None
        )

        return render_template(
            "dashboard.html",
            nama=session["nama"],
            tanggal=ringkasan["tanggal"],
            berat=ringkasan["berat"],
            tidur=ringkasan["tidur"],
            jumlah_jurnal=ringkasan["jumlah_jurnal"],
            berat_terbaru=ringkasan["berat_terbaru"],
            tidur_terbaru=ringkasan["tidur_terbaru"],
            tanggal_terbaru=ringkasan["tanggal_terbaru"],
            rata_berat=ringkasan["rata_berat"],
            rata_tidur=ringkasan["rata_tidur"],
            daftar_aktivitas=ringkasan["daftar_aktivitas"],
            jumlah_keluhan=len(riwayat_keluhan),
            keluhan_terakhir=keluhan_terakhir,
            pesan_error=None
        )

    except Exception as error:
        print("Dashboard error:", error)

        return render_template(
            "dashboard.html",
            nama=session["nama"],
            tanggal=[],
            berat=[],
            tidur=[],
            jumlah_jurnal=0,
            berat_terbaru=None,
            tidur_terbaru=None,
            tanggal_terbaru=None,
            rata_berat=0,
            rata_tidur=0,
            daftar_aktivitas=[],
            jumlah_keluhan=0,
            keluhan_terakhir=None,
            pesan_error="Gagal mengambil data dashboard."
        )


# HALAMAN JURNAL DAN PENCARIAN
@app.route("/jurnal", methods=["GET", "POST"])
@login_required
def jurnal():

    pesan_sukses = None
    pesan_error = None
    riwayat = []

    kata_kunci = request.args.get("q", "").strip()
    tanggal_filter = request.args.get("tanggal", "").strip()

    try:

        # MENAMBAHKAN JURNAL
        if request.method == "POST":

            JurnalService.tambah_jurnal(
                tanggal=request.form.get("tanggal"),
                berat=request.form.get("berat"),
                tidur=request.form.get("tidur"),
                aktivitas=request.form.get("aktivitas"),
                kondisi=request.form.get("kondisi"),
                user_id=session["user_id"]
            )

            pesan_sukses = "Jurnal berhasil disimpan!"

        # MENAMPILKAN DAN MENCARI JURNAL
        riwayat = JurnalService.ambil_semua(
            user_id=session["user_id"],
            kata_kunci=kata_kunci,
            tanggal_filter=tanggal_filter
        )

    except Exception as error:

        pesan_error = "Terjadi kesalahan saat mengelola jurnal."
        print("Jurnal error:", error)

    return render_template(
        "jurnal.html",
        riwayat=riwayat,
        pesan_sukses=pesan_sukses,
        pesan_error=pesan_error,
        kata_kunci=kata_kunci,
        tanggal_filter=tanggal_filter
    )


# EDIT JURNAL
@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_jurnal(id):

    try:

        jurnal_data = JurnalService.cari_berdasarkan_id(
            jurnal_id=id,
            user_id=session["user_id"]
        )

        if jurnal_data is None:
            return "Jurnal tidak ditemukan", 404

        if request.method == "POST":

            berhasil = JurnalService.perbarui_jurnal(
                jurnal_id=id,
                user_id=session["user_id"],
                tanggal=request.form.get("tanggal"),
                berat=request.form.get("berat"),
                tidur=request.form.get("tidur"),
                aktivitas=request.form.get("aktivitas"),
                kondisi=request.form.get("kondisi")
            )

            if berhasil:
                return redirect(url_for("jurnal"))

            return "Jurnal tidak ditemukan atau gagal diperbarui", 404

        return render_template(
            "edit_jurnal.html",
            jurnal=jurnal_data
        )

    except Exception as error:

        print("Edit error:", error)
        return "Terjadi kesalahan saat mengedit jurnal.", 500


# HAPUS JURNAL
@app.route("/hapus/<int:id>", methods=["POST"])
@login_required
def hapus_jurnal(id):

    try:

        berhasil = JurnalService.hapus_jurnal(
            jurnal_id=id,
            user_id=session["user_id"]
        )

        if berhasil:
            return redirect(url_for("jurnal"))

        return "Jurnal tidak ditemukan atau gagal dihapus", 404

    except Exception as error:

        print("Hapus error:", error)
        return "Terjadi kesalahan saat menghapus jurnal.", 500

# ==========================================
# BODY HEALTH MAP
# ==========================================

@app.route("/body-map", methods=["GET", "POST"])
@login_required
def body_map():

    pesan_sukses = None
    pesan_error = None
    riwayat = []

    try:

        # MENYIMPAN KELUHAN
        if request.method == "POST":

            body_side = request.form.get("body_side", "")
            body_part = request.form.get("body_part", "")
            keluhan = request.form.get("keluhan", "")

            berhasil, pesan = BodyHealthMapService.simpan_keluhan(
                user_id=session["user_id"],
                body_side=body_side,
                body_part=body_part,
                keluhan=keluhan
            )

            if berhasil:
                pesan_sukses = pesan
            else:
                pesan_error = pesan

        # MENGAMBIL RIWAYAT KELUHAN
        riwayat = BodyHealthMapService.ambil_riwayat(
            session["user_id"]
        )

    except Exception as error:

        print("Body Health Map error:", error)
        pesan_error = "Terjadi kesalahan saat membuka Body Health Map."

    return render_template(
        "body_map.html",
        riwayat=riwayat,
        pesan_sukses=pesan_sukses,
        pesan_error=pesan_error
    )


# ==========================================
# EDIT KELUHAN BODY HEALTH MAP
# ==========================================

@app.route("/body-map/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_body_map(id):

    user_id = session["user_id"]

    try:

        laporan = BodyHealthMapService.ambil_berdasarkan_id(
            id,
            user_id
        )

        if not laporan:
            return redirect(url_for("body_map"))

        if request.method == "POST":

            body_side = request.form.get("body_side", "")
            body_part = request.form.get("body_part", "")
            keluhan = request.form.get("keluhan", "")

            berhasil, pesan = BodyHealthMapService.perbarui_keluhan(
                laporan_id=id,
                user_id=user_id,
                body_side=body_side,
                body_part=body_part,
                keluhan=keluhan
            )

            if berhasil:
                return redirect(url_for("body_map"))

            return render_template(
                "edit_body_map.html",
                laporan=laporan,
                pesan_error=pesan
            )

        return render_template(
            "edit_body_map.html",
            laporan=laporan,
            pesan_error=None
        )

    except Exception as error:

        print("Edit Body Health Map error:", error)
        return "Terjadi kesalahan saat mengedit keluhan.", 500


# ==========================================
# HAPUS KELUHAN BODY HEALTH MAP
# ==========================================

@app.route("/body-map/hapus/<int:id>", methods=["POST"])
@login_required
def hapus_body_map(id):

    try:

        berhasil, pesan = BodyHealthMapService.hapus_keluhan(
            laporan_id=id,
            user_id=session["user_id"]
        )

        if not berhasil:
            print("Hapus keluhan:", pesan)

        return redirect(url_for("body_map"))

    except Exception as error:

        print("Hapus Body Health Map error:", error)
        return "Terjadi kesalahan saat menghapus keluhan.", 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )