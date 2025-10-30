"""
Facial Emotion Recognition Module
Detects emotions from webcam using CNN
"""
import cv2
import numpy as np
import tensorflow as tf
from collections import Counter

class FacialEmotionDetector:
    def __init__(self, model_file='retrained_graph.pb', label_file='retrained_labels.txt', 
                 cascade_file='haarcascade_frontalface_alt.xml'):
        self.model_file = model_file
        self.label_file = label_file
        self.classifier = cv2.CascadeClassifier(cascade_file)
        self.emotion_dict = {'angry': '1', 'happy': '2', 'neutral or sad': '3'}
        self.predictions = []
        self.load_model()
        
    def load_model(self):
        """Load TensorFlow model"""
        tf.compat.v1.disable_eager_execution()
        self.graph = tf.Graph()
        graph_def = tf.compat.v1.GraphDef()
        with open(self.model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with self.graph.as_default():
            tf.import_graph_def(graph_def)
            
    def load_labels(self):
        """Load emotion labels"""
        labels = []
        proto_as_ascii_lines = tf.io.gfile.GFile(self.label_file).readlines()
        for l in proto_as_ascii_lines:
            labels.append(l.rstrip())
        return labels
        
    def predict_emotion(self, image_path):
        """Predict emotion from image"""
        input_height = 224
        input_width = 224
        input_mean = 128
        input_std = 128
        
        file_reader = tf.compat.v1.read_file(image_path, "file_reader")
        image_reader = tf.image.decode_jpeg(file_reader, channels=3, name='jpeg_reader')
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.compat.v1.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        
        sess = tf.compat.v1.Session()
        t = sess.run(normalized)
        
        input_name = "import/input"
        output_name = "import/final_result"
        input_operation = self.graph.get_operation_by_name(input_name)
        output_operation = self.graph.get_operation_by_name(output_name)
        
        with tf.compat.v1.Session(graph=self.graph) as sess:
            results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
        
        results = np.squeeze(results)
        top_k = results.argsort()[-5:][::-1]
        labels = self.load_labels()
        
        return labels[top_k[0]]
        
    def get_emotion_probabilities(self, image_path):
        """Get emotion probabilities for all classes"""
        # Returns dict: {'angry': 0.1, 'happy': 0.7, 'neutral': 0.2}
        emotion = self.predict_emotion(image_path)
        emotion_code = self.emotion_dict.get(emotion.lower(), '3')
        
        # Simple mapping for now
        probs = {'angry': 0.0, 'happy': 0.0, 'neutral': 0.0}
        if emotion_code == '1':
            probs['angry'] = 0.9
        elif emotion_code == '2':
            probs['happy'] = 0.9
        else:
            probs['neutral'] = 0.9
        return probs
        
    def detect_from_webcam(self, num_predictions=10):
        """Detect emotion from webcam stream"""
        webcam = cv2.VideoCapture(0)
        self.predictions = []
        size = 4
        
        while len(self.predictions) < num_predictions:
            (rval, im) = webcam.read()
            if not rval:
                break
                
            im = cv2.flip(im, 1, 0)
            mini = cv2.resize(im, (int(im.shape[1]/size), int(im.shape[0]/size)))
            faces = self.classifier.detectMultiScale(mini)
            
            for f in faces:
                (x, y, w, h) = [v * size for v in f]
                cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 4)
                sub_face = im[y:y+h, x:x+w]
                
                face_file = "test.jpg"
                cv2.imwrite(face_file, sub_face)
                
                text = self.predict_emotion(face_file)
                emotion_code = self.emotion_dict.get(text.lower(), '3')
                self.predictions.append(emotion_code)
                
                font = cv2.FONT_HERSHEY_TRIPLEX
                cv2.putText(im, emotion_code, (x+w, y), font, 1, (0,0,255), 1)
                
            cv2.imshow('Facial Emotion Detection', im)
            key = cv2.waitKey(10)
            if key == 27:  # ESC key
                break
                
        webcam.release()
        cv2.destroyAllWindows()
        
        if self.predictions:
            most_common = Counter(self.predictions).most_common(1)[0][0]
            return most_common
        return '3'  # neutral default
