import cv2
from .dlib_tools import DilbTools
import numpy as np
from model.model import Student
from Config import config

class FaceFeatureTo128D:
    """
    Extract facial feature to a 128D vectors space
    """
    @classmethod
    def feature_in_db(self, image, face_id):
        """
        Store student's facial feature data into mysql database
        """
        detector = DilbTools.get_detector()
        predictor = DilbTools.get_predictor()
        face_model = DilbTools.get_face_model()
        # imdata = cv2.imread(image)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        has_face = detector(image_rgb, 1)
        if len(has_face) == 0:
            raise Exception("No face was detected! ")
        if len(has_face) > 1:
            raise Exception("Too many face: ")
        shape = predictor(image_rgb, has_face[0])
        face_desc = face_model.compute_face_descriptor(image_rgb, shape)
        # print('face_desc: %s' % face_desc)
        feature_array = np.array([])
        for _, desc in enumerate(face_desc):
            feature_array = np.append(feature_array, desc)
        # Store the facial features into Database
        student = Student.query.filter_by(number=face_id).first()
        if student:
            student.featureArray = feature_array.dumps()
        try:
            config.db.session.commit()
        except Exception as e:
            config.db.session.rollback()

    @classmethod
    def feature_out_db(cls):
        """
        Get the existed facial feature from the Database
        :return:
        """
        students = Student.query.filter().all()
        feature_array = []
        for student in students:
            if student.featureArray:
                feature_array.append((student.number, np.loads(student.featureArray)))
        return feature_array
