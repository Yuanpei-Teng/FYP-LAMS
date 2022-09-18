import datetime
from sqlalchemy import and_, or_
from flask import render_template, jsonify, request, Response, Blueprint
from model.model import *

import base64
import numpy as np
from dilbface.face_128D import FaceFeatureTo128D
from dilbface.face_recognition import FaceRecognition
import cv2

st = Blueprint("student", __name__)


# Upload face info
@st.route('/upload/<int:id>', methods=["POST"])
def upload(id):
    data = request.json
    student = Student.query.filter_by(number=id).first()
    if student:
        print(student.lastName + student.firstName)
    photo = data.get("photo")
    if photo:
        # Change the format of the photo to base64
        photo = base64.b64decode(photo)
        img11 = cv2.imdecode(np.asarray(bytearray(photo), dtype=np.uint8), -1)
        try:
            FaceFeatureTo128D.feature_in_db(img11, id)
        except Exception as e:
            print(e)
            return jsonify({"code": 400, "msg": "Get Face model Failed！info：{} Please retry".format(e)})
    return jsonify({"code": 200, "msg": "Get Face Model Successful！"})


# Edit student info
@st.route('/api/s/update', methods={"POST"})
def modifiedInfo():
    data = request.json
    id = data.get("id")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    email = data.get("email")
    student = Student.query.filter_by(number=id).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Student ID not exist！"})
    student.firstName = firstName if firstName != "" and firstName is not None else student.firstName
    student.lastName = lastName if lastName != "" and lastName is not None else student.lastName
    student.email = email if email != "" and email is not None else student.email
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Update Failed! Database error！"})
    return jsonify({"code": 200, "msg": "Update profile successful！"})


# Activation Account
@st.route('/api/s/enable/<string:email>/<int:code>', methods={"GET"})
def enable_email(email, code):
    student = Student.query.filter_by(email=email).first()
    if student is None:
        return render_template("forward.html", code=400, msg="Account activation failed, there is no account information! Please contact the administrator!")
    ac = ActivationCode.query.filter_by(email=email).first()
    if ac is None:
        return render_template("forward.html", code=400, msg="Account activation failed. There is no activation verification code for the account! Please contact the administrator!")
    if str(code) != ac.activationCode:
        return render_template("forward.html", code=400, msg="Account activation failed! This activation link has expired, please check! Please contact the administrator!")
    if str(code) == ac.activationCode:
        student.enable = 2
        ActivationCode.query.filter_by(email=email).delete()
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return render_template("forward.html", code=400, msg="Account activation failed !  Database exception !")
    return render_template("forward.html", code=200)


# Change student password
@st.route('/api/s/pwd/update', methods=["POST"])
def s_pwd_update():
    data = request.json
    sid = data.get("id")
    student = Student.query.filter_by(number=sid).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Change Password Failed！Student not exist！"})
    oldPwd = data.get("oldPwd")
    if student.password != oldPwd:
        return jsonify({"code": 400, "msg": "Change Password Failed！Wrong old password !"})
    newPwd = data.get("newPwd")
    secondayPwd = data.get("secondayPwd")
    if newPwd != secondayPwd:
        return jsonify({"code": 400, "msg": "Change Password Failed！Two new passwords not match！"})
    student.password = newPwd
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Change Password Failed！Database error！"})
    return jsonify({"code": 200, "msg": "Change Password Successful！"})


# Student Login
@st.route('/api/login', methods={"POST"})
def login():
    loginJson = request.json
    number = loginJson.get("number")
    password = loginJson.get("password")
    if not all([number, password]):
        return jsonify({"code": 400, "msg": "Wrong Account or Password！"})
    student = Student.query.filter_by(number=number).first()
    if student:
        if student.enable != 2:
            return jsonify({"code": 400, "msg": "Your account is not activated, please login to your email and active your account！"})
        if student.password == password:

            if student.featureArray is None:
                return jsonify({"code": 200, "msg": "You have not entered your facial information！"})
            return jsonify({"code": 200, "msg": "Login Successfully！"})
    return jsonify({"code": 400, "msg": "Wrong Account or Password！"})


from Config import send_async_email
import random


# Student register
@st.route('/api/register', methods={"POST"})
def register():
    userJson = request.json
    id = userJson.get("number")
    firstName = userJson.get("firstName")
    lastName = userJson.get("lastName")
    email = userJson.get("email")
    password = userJson.get("password")
    age = userJson.get("age")
    try:
        if int(age) >= 50 or int(age) <= 15:
            return jsonify({"code": 400, "msg": "Age between 15~50！Please enter correct age"})
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Wrong age！Please enter again"})
    if not all([firstName, lastName, email, password, id, age]):
        return jsonify({"code": 400, "msg": "Incomplete student information！Please check for empty columns。"})
    student = Student.query.filter_by(number=id).first()
    if student:
        return jsonify({"code": 400, "msg": "Student ID has been registered"})
    student = Student.query.filter_by(email=email).first()
    if student:
        return jsonify({"code": 400, "msg": "Email has been registered"})
    # create activate code
    code = [random.randint(0, 9) for i in range(0, 6)]
    codestr = ""
    for c in code:
        codestr += str(c)
    ac = ActivationCode()
    ac.email = email
    ac.activationCode = codestr
    try:
        db.session.add(ac)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"code": 400, "msg": "Error，Create activation code failed！"})
    # Send activation email
    template = """
        <h1>Hello, Student</h1>
                Your accout is inactive, please click the link below to active your account, otherwise you cannot Log in.
                <br>
                <a href="http://localhost:5000/api/s/enable/{}/{}">Active Account</a>
    """.format(email, ac.activationCode)
    email_data = {"subject": "Account Activation", "to": email, "body": template}
    send_async_email(email_data)
    student = Student()
    student.firstName = firstName
    student.lastName = lastName
    student.number = id
    student.age = age
    student.email = email
    student.enable = 1
    student.password = password
    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"code": 400, "msg": "Register Failed！Database error！"})
    return jsonify({"code": 200, "msg": "Register Successful！"})


# Check the student ID
@st.route('/api/checkNumber/<int:id>', methods={"GET"})
def checkNumber(id):
    student = Student.query.filter_by(number=id).first()
    if student:
        return jsonify({"code": 200, "msg": "false"})
    return jsonify({"code": 200, "msg": "true"})

# Enroll into class
@st.route('/api/s/addCourse', methods=["POST"])
def student_addCourse():
    """
    Get class
    :return:
    """
    data = request.json
    sid = data.get("sid")
    cid = data.get("cid")
    if not all([sid, cid]):
        return jsonify({"code": 400, "msg": "Student ID of Course ID cannot be empty!"})
    student = Student.query.filter_by(number=sid).first()
    course = Course.query.filter_by(id=cid).first()
    print(student, course)
    if not all([student, course]):
        return jsonify({"code": 400, "msg": "Student or Course not exist"})
    sc = StudentCourse()
    sc.sid = sid
    sc.cid = cid
    sc.score = 0
    try:
        db.session.add(sc)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Database error！"})

    return jsonify({"code": 200, "msg": "Add Course successful!"})


# Student delete class
@st.route('/api/s/batchRemove', methods=["POST"])
def remove():
    """
    Student delete class
    :return:
    """
    data = request.json
    sid = data.get("sid")
    cids = data.get("cids")
    print(sid, cids)
    if not all([sid, cids]):
        return jsonify({"code": 400, "msg": "Please check empty columns！"})
    student = Student.query.filter_by(number=sid).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Student not exist！"})
    try:
        StudentCourse.query.filter(and_(StudentCourse.cid.in_(cids), StudentCourse.sid == student.id)).delete(
            synchronize_session=False)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        jsonify({"code": 400, "msg": "Database error!"})
    return jsonify({"code": 200, "msg": "Delete Course Successful！"})


# Reterive the classes which are not enrolled yet
@st.route('/api/s/getNotCourse/<int:id>', methods=["GET"])
def getNotAddCourse(id):
    """
    reterive the rest of the classes
    :return:
    """
    sc = StudentCourse.query.filter_by(sid=id).all()
    ids = []
    for sc1 in sc:
        ids.append(sc1.cid)
    courses = Course.query.filter(Course.id.notin_(ids)).all()
    data = []
    for course in courses:
        data.append(
            {"cid": course.id, "name": course.name, "teacher": course.teacher, "create_time":
                course.createTime.today().strftime('%Y-%m-%d'), "enable": False if course.enable == 0 else True})
    return jsonify({"code": 200, "msg": "Enroll Course successful", "data": data})


# Enrol multiple classes
@st.route('/api/s/batchAddCourse', methods=["POST"])
def batchAddCourse():
    """
    Enrol multiple classes
    :return:
    """
    data = request.json
    id = data.get("id")
    cids = data.get("cids")
    if not all([id, cids]):
        return jsonify({"code": 400, "msg": "Please fill in all empty columns！"})
    student = Student.query.filter_by(number=id).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Student ID not exist！"})
    courses = Course.query.filter(Course.id.in_(cids)).all()
    for course in courses:
        sc = StudentCourse()
        sc.sid = student.id
        sc.cid = course.id
        sc.score = 0
        try:
            db.session.add(sc)
        except Exception as e:
            print(e)
            return jsonify({"code": 400, "msg": "Add multiple course failed！Database error"})
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"code": 400, "msg": "Add multiple courses failed！Database error"})
    return jsonify({"code": 200, "msg": "Add multiple courses successful"})


# Search for a class
@st.route('/api/s/searchCourse', methods=["POST"])
def searchCourse():
    """
    Search for a class
    :return:
    """
    data = request.json
    keyword = data.get("keyword")
    id = data.get("id")
    page = data.get("page")
    size = data.get("size")
    student = Student.query.filter_by(number=id).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Failed to get course info！Student ID not exist!"})
    sc = StudentCourse.query.filter_by(sid=student.id).all()
    ids = []
    for sc1 in sc:
        ids.append(sc1.cid)
    print(ids)
    if keyword is None or keyword == "":
        courses = Course.query.filter().paginate(page, size)
    else:
        courses = Course.query.filter(
            or_(Course.id == keyword, Course.name == keyword)).paginate(page, size)
    data = []
    for course in courses.items:
        if course.id in ids:
            cos = course.toDict()
            cos["exists"] = True
            data.append(cos)
        else:
            cos = course.toDict()
            cos["exists"] = False
            data.append(course.toDict())
    return jsonify({"code": 200, "msg": "Enroll Course Successful", "data": data, "total": courses.total})


# Get login name and check whether this id's face model existed.
@st.route('/api/s/getName/<int:id>', methods=["GET"])
def getName(id):
    """
    Get login name and check whether this id's face model existed.
    :return:
    """
    name = ""
    student = Student.query.filter_by(number=id).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Failure to get the name, Student ID not exists!", "name": name})
    feature = True
    if student.featureArray is None:
        feature = False
    return jsonify({"code": 200, "msg": "Get Class lists successfully", "name": student.firstName + " " + student.lastName, "feature": feature})


# Get enrolled Classes
@st.route('/api/s/getCourse/<int:id>', methods=["GET"])
def student_getCourse(id):
    """
    Get enrolled Classes
    :return:
    """
    student = Student.query.filter_by(number=id).first()
    if student is None:
        return jsonify({"code": 200, "msg": "Student ID not exists！"})
    sc = StudentCourse.query.filter_by(sid=student.id).all()
    ids = []
    for sc1 in sc:
        ids.append(sc1.cid)
    courses = Course.query.filter(Course.id.in_(ids)).all()
    data = []
    for sc1 in sc:
        for course in courses:
            if course.id == sc1.cid:
                vo = course.toDict()
                vo["score"] = sc1.score / course.count * 100 if sc1.score <= course.count else 100
                data.append(vo)
    return jsonify({"code": 200, "msg": "Get Class lists successfully", "data": data})


# Enroll into Class through email
@st.route('/api/s/addCourseByEmail', methods=["POST"])
def addCourseByEmail():
    """
    :return:
    """
    data = request.json
    cid = data.get("cid")
    course = Course.query.filter_by(id=cid).first()
    if course is None:
        return jsonify({"code": 400, "msg": "This course no longer exists！"})
    number = data.get("number")
    pwd = data.get("pwd")
    student = Student.query.filter(and_(Student.number == number, Student.password == pwd)).first()
    if student is None:
        return jsonify({"code": 400, "msg": "Validation Failed, Wrong Account or Password！"})

    sc = StudentCourse()
    sc.sid = student.id
    sc.cid = course.id
    sc.score = 0
    try:
        db.session.add(sc)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return jsonify({"code": 200, "msg": "Enroll Course Successful!"})
