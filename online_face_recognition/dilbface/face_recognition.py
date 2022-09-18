import cv2
from .dlib_tools import DilbTools

import numpy as np
from .face_128D import FaceFeatureTo128D


class FaceRecognition:
    """
    Face recognize part, using the image that upload from the front-end and compare this image with the image that
    stored in the database to determine whether it is the same person

    """
    @classmethod
    def face_compare(cls, face_image):
        """
        """
        features = FaceFeatureTo128D.feature_out_db()
        detector = DilbTools.get_detector()
        predictor = DilbTools.get_predictor()
        model = DilbTools.get_face_model()
        rgb_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
        faces = detector(rgb_image, 1)
        if len(faces) == 0:
            print("Face not observed!")
            return -2
        else:
            for face_id, feature in features:
                array = np.array([])
                shape = predictor(rgb_image, faces[0])
                face_desc = model.compute_face_descriptor(rgb_image, shape)
                for _, desc in enumerate(face_desc):
                    array = np.append(array, desc)
                if cls.face_recogition(array, feature):
                    return face_id
            return -1

    @classmethod
    def face_recogition(cls, face1, face2):
        """
        """
        distance = np.linalg.norm(face1 - face2)
        print('euclidean metric:%s' % distance)
        if (distance < 0.5):
            return True
        else:
            return False
