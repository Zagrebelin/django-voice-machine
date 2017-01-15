import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BaseModel = declarative_base()

class ScheduleItem(BaseModel):
    __tablename__ = 'schedule_item'
    use_holiday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_workday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_monday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_tuesday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_wednesday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_thursday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_friday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_saturday = sqlalchemy.Column(sqlalchemy.Boolean)
    use_sunday = sqlalchemy.Column(sqlalchemy.Boolean)

    time = sqlalchemy.Column(sqlalchemy.Time)
    message = sqlalchemy.Column(sqlalchemy.String)
    order = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    @property
    def holiday_or_weekday(self):
        if self.use_holiday and self.use_workday:
            return 'Будни и выходные'
        elif self.use_holiday and not self.use_workday:
            return 'Будни'
        elif not self.use_holiday and self.use_workday:
            return 'Выходные'
        elif not self.use_holiday and not self.use_workday:
            return 'Никогда'
        else:
            return '???'

    @property
    def weekdays(self):
        ret = []
        if self.use_monday: ret.append('Пн')
        if self.use_tuesday: ret.append('Вт')
        if self.use_wednesday: ret.append('Ср')
        if self.use_thursday: ret.append('Чт')
        if self.use_friday: ret.append('Пт')
        if self.use_saturday: ret.append('Сб')
        if self.use_sunday: ret.append('Вс')
        if len(ret) == 7:
            ret = ['Каждый день']
        elif len(ret) == 0:
            ret = ['Никогда']
        return ', '.join(ret)


class Holiday(BaseModel):
    __tablename__ = 'holiday'
    year = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.Date)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)


engine = sqlalchemy.create_engine('sqlite:///./sample_db_2.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
BaseModel.metadata.create_all(engine)