# Литературный справочник

Telegram-бот и веб-приложение для поиска информации о литературных произведениях с использованием GigaChat API.

## Описание

Проект представляет собой систему, состоящую из двух основных компонентов:
1. Telegram-бот для быстрого поиска информации о книгах
2. Веб-интерфейс для просмотра истории запросов и управления данными

### Основные возможности

- Поиск информации о литературных произведениях через Telegram
- Структурированный вывод информации о книгах
- Административный веб-интерфейс
- Система рейтинга произведений
- Кэширование результатов запросов

## Требования

- Python 3.12
- pipenv
- PostgreSQL
- Telegram Bot Token
- GigaChat API Key

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/school_helper.git
cd school_helper
```

2. Установите зависимости:
```bash
make install
```

3. Создайте файл `.env` в корневой директории проекта со следующим содержимым:
```env
TG_BOT_KEY=your_telegram_bot_token
GIGA_CHAT_AUTH_KEY=your_gigachat_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
FLASK_SECRET_KEY=your_secret_key
```

4. Создайте базу данных:
```bash
make db-create
```

## Использование

### Запуск бота

```bash
make run-bot
```

### Запуск веб-приложения

```bash
make run-web
```



## Структура проекта

```
school_helper/
├── src/
│   ├── config.py                 # Конфигурация приложения
│   ├── db/                      # Работа с базой данных
│   │   ├── connect.py
│   │   ├── model/
│   │   └── repository/
│   ├── llm/                     # Интеграция с LLM
│   │   ├── abstract_llm.py
│   │   ├── constant.py
│   │   ├── factory.py
│   │   └── giga_chat.py
│   ├── service/                 # Бизнес-логика
│   │   ├── LiteraryWorksService.py
│   │   └── UsersService.py
│   ├── telegram/                # Telegram бот
│   │   ├── bot.py
│   │   ├── commands.py
│   │   └── handler/
│   └── website/                 # Веб-приложение
│       ├── main.py
│       └── templates/
├── .env                         # Переменные окружения
├── Makefile                     # Команды для управления проектом
├── Pipfile                      # Зависимости проекта
└── README.md                    # Документация
```

## API Telegram бота

### Команды

- `/start` - Начало работы с ботом
- `/find [название книги]` - Поиск информации о книге

### Формат ответа

```
Название: [Оригинальное название + год публикации]
Автор: [ФИО автора и краткая биография]
Жанр: [Литературное направление]
Краткое описание: [2–3 предложения о сюжете]
Краткое содержание: [Основные события в 10 предложениях]
Философские вопросы: [Темы и идеи, которые поднимает книга]
```


## Авторы

- [Иванова Мария](https://github.com/MariiaIvvanova)

## Поддержка

При возникновении проблем или вопросов, пожалуйста, создайте issue в репозитории проекта. 