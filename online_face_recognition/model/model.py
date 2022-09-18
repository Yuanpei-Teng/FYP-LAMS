import datetime

from Config import config

db = config.db
app = config.app

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    lastName = db.Column(db.String(64), unique=False)
    firstName = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=False)
    age = db.Column(db.Integer)
    featureArray = db.Column(db.LargeBinary)  # facial feature values
    email = db.Column(db.String(64), unique=True)
    enable = db.Column(db.Integer)  # Account activate or not, 1 is non-active, 2 is activated.

    def _dict_(self):
        return {"name": "{}{}".format(self.firstName, self.lastName),
                "number": self.number, "email": self.email, "age": self.age
                }
# Insert a new table into database
# >python start.py db migrate Generate DDL script
# python start.py db upgrade submit and execute ddl script


class ActivationCode(db.Model):
    __tablename__ = "student_activate"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    activationCode = db.Column(db.String(64), unique=False)
    #
    # def toDict(self):
    #     return {"id": self.id, "sid": self.sid, "activationCode": self.activationCode}


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    password = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    firstName = db.Column(db.String(64), unique=True)
    lastName = db.Column(db.String(64), unique=True)

    def toDict(self):
        return {"id": self.id, "number": self.number, "email": self.email, "firstName": self.firstName,
                "lastName": self.lastName}


class StudentCourse(db.Model):
    __tablename__ = "student_course"
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer)  # Student id
    cid = db.Column(db.Integer)  # Course id
    score = db.Column(db.Integer)  # attendance score

    def toDict(self):
        return {"id": self.id, "sid": self.sid, "score": self.score}


class Course(db.Model):
    """
    Course table
    """
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False)
    teacherId = db.Column(db.Integer)
    teacher = db.Column(db.String(64), unique=False)
    week = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    beginTime = db.Column(db.String(8))
    address = db.Column(db.String(255))
    count = db.Column(db.Integer)
    createTime = db.Column(db.DateTime)

    def toDict(self):
        return {
            "id": self.id, "name": self.name, "teacherId": self.teacherId,
            "teacher": self.teacher, "week": self.week, "duration": self.duration,
            "beginTime": self.beginTime, "address": self.address, "count": self.count,
            "createTime": self.createTime
        }


class SignRecord(db.Model):
    """
    SignRecord table
    """
    __tablename__ = "sign_record"
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, unique=False)
    cid = db.Column(db.Integer, unique=False)
    createTime = db.Column(db.Date)
