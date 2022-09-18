import dlib
import  os
basedir = os.path.abspath(os.path.dirname(__file__))
face_model_path = basedir +'/dlib_face_recognition_resnet_model_v1.dat'
predictor_path = basedir+ '/shape_predictor_5_face_landmarks.dat'

class DilbTools:

    @classmethod
    def get_detector(cls):
        """
        Get face detector
        """
        return dlib.get_frontal_face_detector()

    @classmethod
    def get_predictor(cls):
        """
        Get face predictor
        """
        return dlib.shape_predictor(predictor_path)

    @classmethod
    def get_face_model(cls):
        """
        Get face model
        """
        return dlib.face_recognition_model_v1(face_model_path)
