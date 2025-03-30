from datetime import datetime

from src.db.model.LiteraryWorks import LiteraryWorks


class LiteraryWorksRepository:
    def __init__(self, session):
        self.session = session

    def create(self, name, response, llm):
        now = datetime.now()
        now_date = now.isoformat(timespec='milliseconds')
        new_user = LiteraryWorks(name=name,
                                 response=response,
                                 llm=llm,
                                 create_date=now_date,
                                 updata_date=now_date)
        self.session.add(new_user)
        self.session.commit()

    def get_by_name(self, name):
        return self.session.query(LiteraryWorks).filter(LiteraryWorks.name == name).first()

    def count(self):
        return self.session.query(LiteraryWorks).count()

    def get_paginated_list(self, page, per_page):
        return (
            self.session.query(LiteraryWorks)
            .order_by(LiteraryWorks.create_date.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
