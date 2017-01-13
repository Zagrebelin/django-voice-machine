from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
sqlalchemy.Column
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

    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    message = db.Column(db.String)
    order = db.Column(db.Integer, default=0)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
