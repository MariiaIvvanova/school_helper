from datetime import datetime

from src.db.model.LiteraryWorks import LiteraryWorks
from src.llm.constant import defoult_llm


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

    def update_response(self, liter_id, response, llm=defoult_llm):
        now = datetime.now().isoformat(timespec='milliseconds')
        literary = self.session.query(LiteraryWorks).filter(LiteraryWorks.id == liter_id).first()
        if literary:
            literary.response = response
            literary.llm = llm
            literary.updata_date = now
            self.session.commit()
        else:
            raise ValueError(f"Произведение с id={liter_id} не найдено.")

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
