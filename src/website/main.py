from flask import Flask, render_template, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from src.db.connect import session
from src.db.model.LiteraryWorks import LiteraryWorks
from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.service.LiteraryWorksService import LiteraryWorksService

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(LiteraryWorks, session))

@app.route('/')
def index():
    literary_works_service = LiteraryWorksService(LiteraryWorksRepository)

    # Получаем номер страницы, по умолчанию 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Количество записей на страницу

    # Запрашиваем данные с учетом пагинации
    literary_works, total_pages = literary_works_service.get_list_response(page, per_page)

    return render_template('index.html', literary_works=literary_works, page=page, total_pages=total_pages)


def web():
    app.run()


if __name__ == "__main__":
    web()
