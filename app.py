from flask import Flask, request, redirect, url_for, render_template, flash, jsonify, session
import os
from dotenv import load_dotenv
from models import db, Users
from flask_migrate import Migrate


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_fallback_secret_key') # Penting untuk flash messages dan session

db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_host = os.getenv('MYSQL_HOST')
db_name = os.getenv('MYSQL_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    # Arahkan langsung ke halaman otentikasi jika belum login
    # Atau ke dashboard jika sudah login (implementasi nanti)
    if 'user_id' in session:
         # return redirect(url_for('dashboard')) # Ganti 'dashboard' dengan rute tujuan Anda
         return f"Welcome {session.get('user_name')}! <a href='/logout'>Logout</a>" # Placeholder
    return redirect(url_for('auth'))

@app.route('/auth')
def auth():
    if 'user_id' in session:
        # Jika sudah login, arahkan ke halaman utama/dashboard
        # return redirect(url_for('dashboard'))
         return redirect(url_for('index')) # Arahkan ke index yang akan menampilkan welcome
    # Tampilkan halaman login/register
    return render_template('auth.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email dan password diperlukan.', 'error')
            return redirect(url_for('auth'))

        # --- Logika Database (Menggunakan SQLAlchemy & Model Users) ---
        try:
            # Cari user berdasarkan email
            user = Users.query.filter_by(email=email).first()

            # Periksa apakah user ada dan password cocok (gunakan metode model)
            if user and user.check_password(password):
                # Login berhasil
                session['user_id'] = user.id # Simpan id pengguna di session
                session['user_name'] = user.username # Simpan username pengguna di session
                
                # Update waktu login terakhir
                user.update_last_login() 
                # db.session.commit() # Commit sudah dilakukan di dalam update_last_login

                flash(f"Selamat datang kembali, {user.username}!", 'success')
                # Arahkan ke halaman dashboard atau halaman utama setelah login
                # return redirect(url_for('dashboard')) # Ganti 'dashboard' dengan rute tujuan Anda
                return redirect(url_for('index')) # Arahkan ke index setelah login
            else:
                # Login gagal
                flash('Email atau password salah.', 'error')
                return redirect(url_for('auth'))

        except Exception as e:
            # Log error untuk debugging
            app.logger.error(f"Error during login: {e}")
            flash(f'Terjadi kesalahan saat login. Silakan coba lagi.', 'error')
            return redirect(url_for('auth'))
        # --- Akhir Logika Database ---

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname') # Diambil dari form
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms') # Checkbox value is 'on' if checked, None otherwise

        # Validasi dasar
        if not all([fullname, email, password, confirm_password]):
            flash('Semua field wajib diisi.', 'error')
            return redirect(url_for('auth'))

        if password != confirm_password:
            flash('Password dan konfirmasi password tidak cocok.', 'error')
            return redirect(url_for('auth'))

        # Pastikan panjang password memenuhi syarat (opsional)
        if len(password) < 8:
             flash('Password minimal harus 8 karakter.', 'error')
             return redirect(url_for('auth'))

        if not terms:
             flash('Anda harus menyetujui Syarat & Ketentuan.', 'error')
             return redirect(url_for('auth'))

        # --- Logika Database (Menggunakan SQLAlchemy & Model Users) ---
        try:
            # Periksa apakah email sudah ada
            existing_user = Users.query.filter_by(email=email).first()
            if existing_user:
                flash('Email sudah terdaftar. Silakan gunakan email lain atau login.', 'error')
                return redirect(url_for('auth'))

            # Periksa apakah username (dari fullname) sudah ada (jika username harus unik)
            # Catatan: Model Users.py mendefinisikan username sebagai unik.
            existing_username = Users.query.filter_by(username=fullname).first()
            if existing_username:
                 flash(f'Nama pengguna "{fullname}" sudah digunakan. Silakan pilih nama lain.', 'error')
                 return redirect(url_for('auth'))

            # Buat instance user baru
            # Memetakan 'fullname' dari form ke field 'username' model
            new_user = Users(username=fullname, email=email)
            # Set password menggunakan metode model (sudah termasuk hashing)
            new_user.set_password(password)

            # Tambahkan user baru ke sesi database dan simpan
            db.session.add(new_user)
            db.session.commit()

            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth')) # Arahkan ke login setelah registrasi

        except Exception as e:
            db.session.rollback() # Batalkan transaksi jika terjadi error
            # Log error untuk debugging
            app.logger.error(f"Error during registration: {e}")
            flash(f'Terjadi kesalahan saat registrasi: {e}', 'error')
            return redirect(url_for('auth'))
        # --- Akhir Logika Database ---

@app.route('/logout')
def logout():
    session.pop('user_id', None) # Hapus user_id dari session
    session.pop('user_name', None) # Hapus user_name dari session
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('auth'))


if __name__ == '__main__':
    app.run(debug=True)