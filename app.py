from flask import Flask, render_template, request, redirect, url_for, session

from database import db
from models import News
from admin_view import init_admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///news.db"
app.config["SECRET_KEY"] = "dev-secret-key"

db.init_app(app)
init_admin(app)

ADMIN_PASSWORD = "admin123"

CATEGORIES = ["Усі новини", "Головне", "Політика", "Економіка", "Життя", "Технології", "Оборона", "Спорт"]

SEED_NEWS = [
    {"title": "Кличко про пам'ятник Мазепі на місці демонтованого Леніна: Офіційних звернень не надходило", "categories": "Головне,Політика", "desc": "Офіційних звернень щодо встановлення пам'ятника не надходило.", "featured": True},
    {"title": "Заборона телефонів у школах: вчені виявили неочікувані негативні наслідки таких обмежень", "categories": "Життя,Технології", "desc": "Дослідники проаналізували вплив заборони на успішність та комунікацію учнів."},
    {"title": "\"Росстату\" заборонили публікувати ціни на пальне", "categories": "Економіка", "desc": "Відомство більше не оприлюднюватиме статистику цін на пальне."},
    {"title": "Чоловік підпалив себе у банку на Кіровоградщині", "categories": "Головне", "desc": "Інцидент стався у відділенні банку, постраждалий госпіталізований."},
    {"title": "Майже 50% функцій для захисту дітей в соцмережах не працюють — звіт", "categories": "Технології,Життя", "desc": "Аналітики перевірили ефективність батьківського контролю у популярних застосунках."},
    {"title": "В Україні лише половина дітей відвідує садочки, черги в них практично зникли — опитування", "categories": "Життя,Головне", "desc": "Опитування показало зміну попиту на місця у дитячих садках."},
    {"title": "Україна піднялась у світовому волейбольному рейтингу після успішних виступів у Лізі націй", "categories": "Спорт", "desc": "Збірна покращила позицію завдяки серії перемог."},
    {"title": "На Закарпатті судитимуть депутата від ОПЗЖ, який приховав 6 мільйонів гривень", "categories": "Політика,Економіка", "desc": "Справу передано до суду після завершення досудового розслідування."},
    {"title": "ЗМІ: Польща задоволена новими обмеженнями ЄС на імпорт української сталі", "categories": "Економіка,Політика", "desc": "Обмеження мають захистити внутрішній ринок сталі в ЄС."},
    {"title": "Генштаб: на фронті зафіксовано понад 100 боєзіткнень за добу", "categories": "Оборона,Головне", "desc": "Найбільша активність спостерігається на кількох напрямках."},
    {"title": "НБУ зберіг облікову ставку без змін", "categories": "Економіка", "desc": "Регулятор пояснив рішення стабільною інфляційною динамікою."},
    {"title": "Збірна України з футболу дізналась суперників у відборі", "categories": "Спорт,Головне", "desc": "Жеребкування визначило групу національної команди."},
    {"title": "В українських школах з'явиться новий предмет з медіаграмотності", "categories": "Життя,Технології", "desc": "МОН представило програму курсу для старшокласників."},
    {"title": "Уряд ухвалив зміни до пенсійного законодавства", "categories": "Політика,Життя", "desc": "Зміни стосуються перерахунку пенсій окремим категоріям громадян."},
    {"title": "В Києві відкрили нову лінію швидкісного трамваю", "categories": "Життя", "desc": "Перша черга маршруту з'єднала два райони столиці."},
    {"title": "Стартап з Львова залучив інвестиції на розробку дрона-розвідника", "categories": "Технології,Оборона", "desc": "Компанія планує масштабувати виробництво найближчим часом."},
    {"title": "ЄС розглядає новий пакет санкцій", "categories": "Політика,Економіка", "desc": "Пакет обговорять на найближчому засіданні ради міністрів."},
    {"title": "Синоптики попередили про різке похолодання", "categories": "Життя", "desc": "У найближчі дні очікується зниження температури на кілька градусів."},
    {"title": "Українські атлети здобули медалі на міжнародному турнірі", "categories": "Спорт", "desc": "Збірна привезла кілька нагород різного ґатунку."},
    {"title": "Військові показали нову модифікацію FPV-дрона", "categories": "Оборона,Технології", "desc": "Розробку тестують у бойових умовах."},
]


def seed_if_empty():
    if News.query.count() == 0:
        for entry in SEED_NEWS:
            db.session.add(News(
                title=entry["title"],
                categories=entry["categories"],
                desc=entry["desc"],
                featured=entry.get("featured", False),
            ))
        db.session.commit()


@app.route("/")
def home():
    category = request.args.get("category", "Усі новини")
    if category == "Усі новини":
        news = News.query.order_by(News.published_at.desc()).all()
    else:
        news = [
            n for n in News.query.order_by(News.published_at.desc()).all()
            if n.has_category(category)
        ]
    return render_template(
        "home.html",
        categories=CATEGORIES,
        news=news,
        current_category=category,
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin.index"))
        error = "Невірний пароль"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))


with app.app_context():
    db.create_all()
    seed_if_empty()


if __name__ == "__main__":
    app.run(debug=True)