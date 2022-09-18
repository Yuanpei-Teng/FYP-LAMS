from flask import render_template, jsonify, request, Response, Blueprint
from model.model import *
from sqlalchemy import and_, or_

tc = Blueprint("teacher", __name__)


@tc.route('/api/teacher_login', methods=["POST"])
def teacher_login():
    """
    Teacher login
    :return:
    """
    data = request.json
    number = data.get("number")
    password = data.get("password")

    if not all([number, password]):
         return jsonify({"code": 400, "msg": "Account or Password cannot be empty!"})

    teacher = Teacher.query.filter_by(number=number).first()

    if teacher:
        if teacher.password == password:
            return jsonify({"code": 200, "msg": "Log in Successful"})
    return jsonify({"code": 400, "msg": "Log in Failed"})


@tc.route('/api/t/<int:id>/getCourse', methods=["GET"])
def get_course(id):
    """
    Get Course List created by current teacher
    :return:
    """
    teacher = Teacher.query.filter_by(number=id).first()
    if teacher is None:
        return jsonify({"code": 400, "msg": "Teacher not exists！"})
    courses = Course.query.filter_by(teacherId=id).all()
    data = []
    for course in courses:
        data.append(course.toDict())
    return jsonify({"code": 200, "msg": "Get course lists successful！", "data": data})


# Delete course by teacher
@tc.route('/api/t/remove', methods=["POST"])
def t_remove():
    """
    Get course
    :return:
    """
    data = request.json
    try:
        Course.query.filter(Course.id.in_(data)).delete(
            synchronize_session=False)
        #     Delete the course associated with the student
        StudentCourse.query.filter(StudentCourse.cid.in_(data)).delete(
            synchronize_session=False)
        db.session.commit()
    except Exception as e:
        print(e)
        jsonify({"code": 400, "msg": "Database error"})
    return jsonify({"code": 200, "msg": "Delete Successful！"})


import datetime

# Create Course
@tc.route('/api/addCourse', methods=["POST"])
def addCourse():
    """
    Create course
    address: "",
        name: "",
        enable: false,
        teacher: 0,
        beginTime: "",
        count: 1,
        week: "",
    :return:
    """
    course = Course()
    data = request.json
    name = data.get("name")
    tid = data.get("teacher")
    address = data.get("address")
    beginTime = data.get("beginTime")
    count = data.get("count")
    week = data.get("week")
    duration = data.get("duration")
    if not all([name, tid, address, beginTime, week, count, duration]):
        return jsonify({"code": 400, "msg": "Failed to add Course！Please fill in all the course details"})
    # Get teacher's name
    teacher = Teacher.query.filter_by(number=tid).first()
    if not teacher:
        return jsonify({"code": 400, "msg": "Failed to add Course！Lecturer ID {} not exists".format(tid)})
    if teacher:
        course = Course.query.filter_by(beginTime=beginTime,week=week,name=name).first()
        if course:
            return jsonify({"code": 400, "msg": "Failed to add Course！Course already exist".format(tid)})
    course = Course()
    course.name = name
    course.duration = duration
    course.teacherId = tid
    course.teacher = teacher.firstName + teacher.lastName
    course.address = address
    course.beginTime = beginTime
    course.count = count
    course.week = week
    course.createTime = datetime.datetime.now()
    try:
        db.session.add(course)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"code": 400, "msg": "Failed to add Course！Database error！"})
    return jsonify({"code": 200, "msg": "Course Added !"})


# Update Course Info
@tc.route('/api/updCourse', methods=["POST"])
def updCourse():
    """
    Update the Course Info
    address: "",
        name: "",
        enable: false,
        teacher: 0,
        beginTime: "",
        count: 1,
        week: "",
    :return:
    """
    data = request.json
    id = data.get("id")
    name = data.get("name")
    tid = data.get("teacherId")
    address = data.get("address")
    beginTime = data.get("beginTime")
    count = data.get("count")
    week = data.get("week")
    duration = data.get("duration")
    if not all([name, tid, address, beginTime, week, count, duration, id]):
        return jsonify({"code": 400, "msg": "Update Course failed！Please fill in all the course details!"})

    teacher = Teacher.query.filter_by(number=tid).first()
    if not teacher:
        return jsonify({"code": 400, "msg": "Update Course Failed！Lecturer ID {} Not exist".format(tid)})
    course = Course.query.filter_by(id=id).first()
    if not course:
        return jsonify({"code": 400, "msg": "Update Course Failed！Course ID {} not exist".format(id)})
    print(beginTime)
    course.name = name
    course.duration = duration
    course.teacherId = tid
    course.teacher = teacher.firstName + teacher.lastName
    course.address = address
    course.beginTime = beginTime
    course.count = count
    course.week = week
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"code": 400, "msg": "Update Course Failed！Database error！"})
    return jsonify({"code": 200, "msg": "Update Course Successfully!"})


# Multiple sign-in operation
@tc.route('/api/batchSignature', methods=["POST"])
def batchSignature():
    """
    Multiple sign-in operation
    :return:
    """
    resp = {"code": 200, "msg": "Request Success！"}
    data = request.json
    cid = data.get("cid")
    sids = data.get("sids")
    count = data.get("count")
    if not all([count, cid]) or sids is None:
        return jsonify({"code": 400, "msg": "Request Failed！Please fill in all the details！"})
    print(cid, count, sids)
    course = Course.query.filter_by(id=cid).first()
    if course is None:
        return jsonify({"code": 400, "msg": "Course not exist！"})
    stus = Student.query.filter(Student.number.in_(sids)).all()
    sids = []
    for stu in stus:
        sids.append(stu.id)
    stcs = StudentCourse.query.filter(and_(StudentCourse.sid.in_(sids), StudentCourse.cid == cid)).all()
    for sc in stcs:
        sc.score += count
        if course.count < sc.score:
            sc.score = course.count
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        resp = {"code": 400, "msg": "Database error！"}
    return jsonify(resp)


# Single sign-in
@tc.route('/api/signature', methods=["POST"])
def signature():
    """
    Perform a single patch operation
    :return:
    """
    resp = {"code": 200, "msg": "Request Success！"}
    data = request.json
    cid = data.get("cid")
    sid = data.get("number")
    count = data.get("count")
    if not all([count, cid, sid]):
        return jsonify({"code": 400, "msg": "Request Failed！Please fill in all details！"})
    course = Course.query.filter_by(id=cid).first()
    if course is None:
        return jsonify({"code": 400, "msg": "Course not exist！"})
    student = Student.query.filter_by(number=sid).first()
    student_course = StudentCourse.query.filter(and_(StudentCourse.cid == cid, StudentCourse.sid == student.id)).first()
    if student_course is None:
        return jsonify({"code": 400, "msg": "This student did not enroll this course！"})
    student_course.score += count
    if course.count < student_course.score:
        student_course.score = course.count
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Failed to sign-in！Database error"})
    return jsonify(resp)


# Edit teacher personal info
@tc.route('/api/t/update', methods=["POST"])
def t_update():
    """
    Edit teacher personal info
    :return:
    """
    data = request.json
    tid = data.get("id")
    teacher = Teacher.query.filter_by(number=tid).first()
    if teacher is None:
        return jsonify({"code": 400, "msg": "Update Failed！Teacher not exists！"})
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    teacher.firstName = firstName if firstName is not None and firstName != "" else teacher.firstName
    teacher.lastName = lastName if lastName is not None and lastName != "" else teacher.lastName
    teacher.email = email if email is not None and email != "" else teacher.email
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Update Failed！Database error！"})
    return jsonify({"code": 200, "msg": "Update Successful！"})


# Change password
@tc.route('/api/t/pwd/update', methods=["POST"])
def t_pwd_update():
    """
    Change password
    :return:
    """
    data = request.json
    tid = data.get("id")
    teacher = Teacher.query.filter_by(number=tid).first()
    if teacher is None:
        return jsonify({"code": 400, "msg": "Change password failed！This teacher's info not exist！"})
    oldPwd = data.get("oldPwd")
    if teacher.password != oldPwd:
        return jsonify({"code": 400, "msg": "Change failed！Wrong old password！"})
    newPwd = data.get("newPwd")
    secondayPwd = data.get("secondayPwd")
    if newPwd != secondayPwd:
        return jsonify({"code": 400, "msg": "Change failed！New password not match！"})
    teacher.password = newPwd
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Change failed！Database error！"})
    return jsonify({"code": 200, "msg": "Change password successful！"})


# Get teacher's name by workID
@tc.route('/api/t/getName/<int:id>', methods=["GET"])
def get_name(id):
    teacher = Teacher.query.filter_by(number=id).first()
    if teacher is None:
        return jsonify({"code": 400, "msg": "Teacher ID not exist！"})
    name = teacher.firstName + teacher.lastName
    return jsonify({"code": 200, "msg": "Get name successful！", "name": name})


# Search teacher's course by using keywords
@tc.route('/api/t/searchCourse', methods=["POST"])
def search_course():
    data = request.json
    id = data.get("tid")
    keyword = data.get("keyword")
    teacher = Teacher.query.filter_by(number=id).first()
    if teacher is None:
        return jsonify({"code": 400, "msg": "This teacher's ID not exist！"})
    # Query all courses of the current teacher
    courses = Course.query.filter(and_(Course.teacherId == id, or_(Course.name.like("%{}%".format(keyword)),
                                                                   Course.id == keyword))).all()
    data = []
    for course in courses:
        course.teacher = teacher.firstName + teacher.lastName
        data.append(course.toDict())
    return jsonify({"code": 200, "msg": "Get name successful！", "data": data})


# Search a student from a current course
@tc.route('/api/t/getMember/<int:id>', methods=["POST"])
def search_member(id):
    data = request.json
    keyword = data.get("keyword")
    select = data.get("select")
    page = data.get("page")
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return jsonify({"code": 400, "msg": "Course Not exist！"})
    stucos = StudentCourse.query.filter_by(cid=id).all()
    if stucos is None:
        return jsonify({"code": 200, "msg": "Get course member list successful！", "data": []})
    sids = []
    for stu in stucos:
        sids.append(stu.sid)
    data = []
    stus = []
    if select == "" or select == "all":
        stus = Student.query.filter(
            and_(Student.id.in_(sids),
                 or_(Student.firstName.like("%{}%".format(keyword)), Student.lastName.like("%{}%".format(keyword))
                     , Student.number == keyword
                     ))).paginate(page, 10)
    if select == "number":
        stus = Student.query.filter(
            and_(Student.id.in_(sids),
                 Student.number == keyword)).paginate(page, 10)
    if select == "firstName":
        stus = Student.query.filter(
            and_(Student.id.in_(sids),
                 Student.firstName.like("%{}%".format(keyword)))).paginate(page, 10)
    if select == "lastName":
        stus = Student.query.filter(
            and_(Student.id.in_(sids),
                 Student.lastName.like("%{}%".format(keyword)))).paginate(page, 10)
    for stuc in stucos:
        vo = {"score": stuc.score}
        for stu in stus.items:
            if stuc.sid == stu.id:
                vo["name"] = stu.firstName + stu.lastName
                vo["number"] = stu.number
                data.append(vo)
    return jsonify({"code": 200, "msg": "Get course member list successful！", "data": data, "count": stus.total})


# Remove student from a class
@tc.route('/api/t/delStudent/<int:id>/<int:cid>', methods=["GET"])
def remove_member(id, cid):
    student = Student.query.filter_by(number=id).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Student not exist！"})
    StudentCourse.query.filter(and_(StudentCourse.sid == student.id, StudentCourse.cid == cid)).delete()
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"code": 400, "msg": "Delete student failed！Database error！"})

    return jsonify({"code": 200, "msg": "Delete student successful！"})


# Batch remove students from a course
@tc.route('/api/t/batchDelStudent/<int:cid>', methods=["POST"])
def batch_remove_member(cid):
    data = request.json
    sids = data.get("sids")
    if not all([sids]):
        return jsonify({"code": 400, "msg": "Please pass in student ID！"})
    students = Student.query.filter(Student.number.in_(sids)).all()
    for student in students:
        StudentCourse.query.filter(and_(StudentCourse.sid == student.id, StudentCourse.cid == cid)).delete()
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"code": 400, "msg": "Delete multiple students Failed！Database error！"})

    return jsonify({"code": 200, "msg": "Delete multiple students Successful！"})


# Get member list who did not enrol into this course
@tc.route('/api/t/getMemberNotExists', methods=["POST"])
def get_member_not_in_course():
    data = request.json
    cid = data.get("cid")
    select = data.get("select")
    keyword = data.get("keyword")
    if not all([cid]):
        return jsonify({"code": 400, "msg": "Please input Course ID！"})
    scs = StudentCourse.query.filter_by(cid=cid).all()
    sids = []
    for sc in scs:
        sids.append(sc.sid)
    students = []
    if select == "" or select is None:
        students = Student.query.filter(and_(Student.number.notin_(sids)
                                             , or_(Student.number == keyword,
                                                   Student.firstName.like("%{}%".format(keyword))
                                                   , Student.lastName.like("%{}%".format(keyword)))
                                             )).all()
    if select == "number":
        students = Student.query.filter(and_(Student.number.notin_(sids)
                                             , Student.number == keyword
                                             )).all()
    if select == "firstName":
        students = Student.query.filter(and_(Student.number.notin_(sids)
                                             , Student.firstName.like("%{}%".format(keyword))
                                             )).all()
    if select == "lastName":
        students = Student.query.filter(and_(Student.number.notin_(sids)
                                             , Student.lastName.like("%{}%".format(keyword))
                                             )).all()
    data = []
    for student in students:
        data.append(student._dict_())
    return jsonify({"code": 200, "msg": "Get list successful！", "data": data})


from Config import send_async_email


# Send class invitation email
@tc.route('/api/t/sendEmail', methods=["POST"])
def send_email():
    data = request.json
    id = data.get("id")
    cid = data.get("cid")
    course = Course.query.filter_by(id=cid).first()
    if course is None:
        return jsonify({"code": 400, "msg": "Course ID not exist！"})
    teacher = Teacher.query.filter_by(number=id).first()
    if teacher is None:
        return jsonify({"code": 400, "msg": "Teacher ID not exist！"})
    emails = data.get("emails")
    template = """
    <h1>Hello,Student</h1>
                <span style="color:red; font-size:25px;">{}</span>Teacher published《{}》module, please click the link below to enroll.<br>
                <a href="http://localhost:{}/#/customer/add/course/{}">Enroll Now !</a>
    """.format(teacher.firstName + teacher.lastName, course.name, app.config["VUE_PORT"], cid)
    for email in emails:
        email_data = {"subject": "New Module Register", "to": email, "body": template}
        send_async_email(email_data)
    return jsonify({"code": 200, "msg": "Send invitation Successfully ！"})
