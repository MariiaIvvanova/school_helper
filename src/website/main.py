import os
from flask import Flask, render_template, request, current_app, session, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from src.config import config
from src.db.connect import get_session
from src.db.model.LiteraryWorks import LiteraryWorks
from src.db.model.RatingLiteraryWorks import RatingLiteraryWorks
from src.db.model.Users import Users
from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.db.repository.RatingLiteraryWorksRepository import RatingLiteraryWorksRepository
from src.service.LiteraryWorksService import LiteraryWorksService
from src.service.RatingLiteraryWorksService import RatingLiteraryWorksService


class SecureModelView(ModelView):
    # Разрешаем просмотр поля id
    column_display_pk = True  # Показывать первичный ключ (обычно id)

    # Если поле исключено, убираем из excluded
    form_excluded_columns = ()

    def is_accessible(self):
        return session.get('logged_in', False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-please-change-in-production')
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(SecureModelView(Users, get_session()))
admin.add_view(SecureModelView(LiteraryWorks, get_session()))
admin.add_view(SecureModelView(RatingLiteraryWorks, get_session()))

PASSWORD = config.ADMIN_PASSWORD

@app.route('/')
def index():
    try:
        literary_works_repo = LiteraryWorksRepository(get_session())
        rating_literary_works_repo = RatingLiteraryWorksRepository(get_session())

        literary_works_service = LiteraryWorksService(literary_works_repo, RatingLiteraryWorksService(rating_literary_works_repo, literary_works_repo), rating_literary_works_repo)

        page = request.args.get('page', 1, type=int)
        per_page = 10
        literary_works, total_pages = literary_works_service.get_list_response(page, per_page)

        return render_template('index.html', literary_works=literary_works, page=page, total_pages=total_pages)
    except Exception as e:
        current_app.logger.error(f"Ошибка при отображении главной страницы: {str(e)}")
        return render_template('error.html', error="Произошла ошибка при загрузке данных"), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect('/admin')
        return "Неверный пароль", 403

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

def web():
    app.run()


if __name__ == "__main__":
    web()
