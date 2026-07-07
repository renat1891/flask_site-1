from datetime import datetime

from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<User {self.username} ({self.age})>'

    def __str__(self):
        return f'{self.username} ({self.age})'


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False, default="Редакція")
    categories = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    img = db.Column(db.String(255), nullable=True)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    published_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def category_list(self):
        return [c.strip() for c in self.categories.split(",") if c.strip()]

    def has_category(self, category):
        return category in self.category_list

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, categories={self.categories})>"

    def __str__(self):
        return f"{self.title}"