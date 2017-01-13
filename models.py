from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ScheduleItem(db.Model):
    use_holiday = db.Column(db.Boolean)
    use_workday = db.Column(db.Boolean)
    use_monday = db.Column(db.Boolean)
    use_tuesday = db.Column(db.Boolean)
    use_wednesday = db.Column(db.Boolean)
    use_thursday = db.Column(db.Boolean)
    use_friday = db.Column(db.Boolean)
    use_saturday = db.Column(db.Boolean)
    use_sunday = db.Column(db.Boolean)

    time = db.Column(db.Time)
    message = db.Column(db.String)
    order = db.Column(db.Integer, default=0)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

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


class Holiday(db.Model):
    date = db.Column(db.Date)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
