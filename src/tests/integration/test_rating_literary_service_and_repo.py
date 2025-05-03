from datetime import datetime

from src.db.connect import get_session
from src.db.repository.UsersRepository import UsersRepository
from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.db.repository.RatingLiteraryWorksRepository import RatingLiteraryWorksRepository


def create_test_users(session):
    users_repo = UsersRepository(session)
    test_users_data = [
        {"telegram_id": "1", "user_name": "Test User 1", "email": "user1@test.com"},
        {"telegram_id": "2", "user_name": "Test User 2", "email": "user2@test.com"},
        {"telegram_id": "3", "user_name": "Test User 3", "email": "user3@test.com"},
    ]
    created_users = []

    for data in test_users_data:
        user = users_repo.get_by_telegram_id(data["telegram_id"])
        if not user:
            user = users_repo.create(**data)
            print(f"✅ Пользователь создан: {data['telegram_id']}")
        else:
            print(f"ℹ️ Пользователь уже существует: {data['telegram_id']}")
        created_users.append(user)

    return created_users


def create_test_work(session):
    literary_repo = LiteraryWorksRepository(session)
    test_name = "тестовое произведение"
    work = literary_repo.get_by_name(test_name)

    if not work:
        work = literary_repo.create(
            name=test_name,
            response="Автотестовое описание",
            llm="test-model"
        )
        print(f"✅ Произведение создано: {test_name}")
    else:
        print(f"ℹ️ Произведение уже существует: {test_name}")

    return work


def add_test_ratings(session, work, users):
    rating_repo = RatingLiteraryWorksRepository(session)
    ratings = [0, 0, 1]

    for user, rating in zip(users, ratings):
        try:
            rating_repo.create(
                id_literary_works=work.id,
                id_user=user.id,
                rating=rating
            )
            print(f"✅ {user.id} поставил оценку: {rating}")
        except Exception as e:
            session.rollback()
            print(f"❌ Ошибка при добавлении оценки от {user.id}: {e}")

    # Статистика
    try:
        avg = rating_repo.calculate_average_rating(work.id)
        count = rating_repo.count_ratings(work.id)
        print(f"\n📊 Средняя оценка: {avg}")
        print(f"📊 Количество оценок: {count}")
    except Exception as e:
        print(f"Ошибка при подсчёте оценок: {e}")


def run_test_data_setup():
    session = get_session()
    users = create_test_users(session)
    work = create_test_work(session)
    add_test_ratings(session, work, users)


if __name__ == "__main__":
    run_test_data_setup()
