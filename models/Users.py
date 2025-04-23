from .database import db
from datetime import timezone
from sqlalchemy import func
import bcrypt

class Users(db.Model):
    """
    Model untuk tabel pengguna (users).
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True))

    def set_password(self, password):
        """Membuat hash dari password yang diberikan dan menyimpannya."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Memeriksa apakah password yang diberikan cocok dengan hash yang tersimpan."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        """Memperbarui waktu login terakhir pengguna."""
        self.last_login = func.now()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'