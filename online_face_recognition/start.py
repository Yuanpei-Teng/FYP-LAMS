import datetime
from sqlalchemy import and_, or_
from flask import render_template, jsonify, request, Response
from model.model import *
import base64
import numpy as np
from dilbface.face_recognition import FaceRecognition
import cv2
from api.student import st
from api.teacher import tc

app = config.create_app()
# Register Student and Teacher api Blueprint
app.register_blueprint(st)
app.register_blueprint(tc)
manager = config.manager
config.init_session()
db = config.get_db()


# Class sign-in function
@app.route('/sign/course/<int:cid>', methods=["POST"])
def sign_in(cid):
    data = request.json
    photos = data.get("photos")
    if photos:
        # Change the photo into BASE64 format
        for photo in photos:
            photo = base64.b64decode(photo)
            img11 = cv2.imdecode(np.asarray(bytearray(photo), dtype=np.uint8), -1)
            state = FaceRecognition.face_compare(img11)
            if state == -1:
                jsonify({"code": 400, "msg": "Failed to sign-in, no record for this face model！"})
            elif state == -2:
                jsonify({"code": 400, "msg": "Failed to sign-in, face not detected. Try again!"})
            else:
                student = Student.query.filter_by(number=state).first()
                # Filter sign-in record for this class, if exist, not keep increasing attendance score
                sing_in = SignRecord.query.filter(and_(SignRecord.cid == cid, SignRecord.sid == student.id)).first()
                if sing_in is not None:
                    return jsonify(
                        {"code": 400, "msg": "You already signed-in for this class！", "name": student.firstName + student.lastName})
                # Add attendance score for this class
                studentCourse = StudentCourse.query.filter(
                    and_(StudentCourse.cid == cid, StudentCourse.sid == student.id)).first()
                if studentCourse is None:
                    return jsonify(
                        {"code": 400, "msg": "You haven't enroll into this course！", "name": student.firstName + student.lastName})
                studentCourse.score += 1
                sign_record = SignRecord()
                sign_record.cid = cid
                sign_record.sid = studentCourse.sid
                try:
                    db.session.add(sign_record)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    return jsonify({"code": 400, "msg": "Sign-in Success! But failed to increase attendance score, database error!"})
                return jsonify({"code": 200, "msg": "Sign-in Success！", "name": student.firstName + student.lastName})
    return jsonify({"code": 400, "msg": "Failed to sign-in, please refresh the page and try again!"})


# Clear sign-in record
@app.route('/sign_record/clear/<int:id>', methods=["GET"])
def sign_record(id):
    """
    Clear sign-in record each time after click start sign-in button
    :return:
    """
    data = {"code": 200, "msg": "Clean sign-in successful！"}
    SignRecord.query.filter(SignRecord.cid == id).delete()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        data = {"code": 400, "msg": "Failed to clean the sign-in record."}
    return jsonify(data)


@app.route('/api/updateCourse/<int:id>', methods=["GET"])
def updateCourse(id):
    """
    Update Course
    :return:
    """
    course = Course.query.filter_by(id=id).first()
    course.enable = 0 if course.enable == 1 else 1
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        jsonify({"code": 400, "msg": "Database error"})
    return jsonify({"code": 200, "msg": "Update successful"})


# Get class info from email method
@app.route('/api/getCourseById/<int:id>', methods=["GET"])
def getCourseById(id):
    """
    Get Course
    :return:
    """
    course = Course.query.filter_by(id=id).first()
    if course is None:
        return jsonify({"code": 200, "msg": "Edit successful", "data": None})
    return jsonify({"code": 200, "msg": "Edit successful", "data": [course.toDict()]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # Used when update new table in database or update tables in database
    # manager.run()
