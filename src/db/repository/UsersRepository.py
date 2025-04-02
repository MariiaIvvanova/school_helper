from datetime import datetime

from src.db.model.Users import Users


class UsersRepository:
    def __init__(self, session):
        self.session = session

    def create(self, telegram_id, user_name, email):
        now = datetime.now()
        now_date = now.isoformat(timespec='milliseconds')
        new_user = Users(
            id=telegram_id,
            user_name=user_name,
            email=email,
            create_date=now_date,
            updata_date=now_date
        )
        self.session.add(new_user)
        self.session.commit()

    def set_block(self, telegram_id, is_block):
        self.session.query(Users).filter(Users.id == telegram_id).update({"is_block": is_block})
        self.session.commit()

    def get_by_telegram_id(self, id):
        return self.session.query(Users).filter(Users.id == id).first()
