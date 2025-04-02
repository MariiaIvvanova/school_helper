.PHONY: install run-bot run-web

# Установка зависимостей
install:
	pipenv install --dev


# Запуск бота
run-bot:
	pipenv run python main.py

# Запуск веб-приложения
run-web:
	pipenv run python -m src.website.main
