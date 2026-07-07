from flask import session, redirect, url_for

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from database import db
from models import User, News


# 1. Захист головної сторінки адмінки (/admin/)
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # Якщо в сесії є позначка, що користувач увійшов — пускаємо
        return session.get('logged_in') == True

    def inaccessible_callback(self, name, **kwargs):
        # Якщо ні — перенаправляємо на нашу сторінку входу
        return redirect(url_for('login'))


# 2. Захист сторінок керування моделями (наприклад, керування новинами)
class SecureModelView(ModelView):
    def is_accessible(self):
        return session.get('logged_in') == True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))


def init_admin(app):
    """Ініціалізує Flask-Admin і прив'язує його до app."""
    admin = Admin(
        app,
        name='Панель Керування',
        index_view=SecureAdminIndexView()
    )
    admin.add_view(SecureModelView(News, db.session))
    admin.add_view(SecureModelView(User, db.session))
    return admin