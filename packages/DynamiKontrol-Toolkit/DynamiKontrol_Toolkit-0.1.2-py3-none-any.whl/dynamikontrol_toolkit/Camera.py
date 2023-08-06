import cv2
import mediapipe as mp

class Face():
    def __init__(self, face_landmarks):
        # face
        left = face_landmarks.landmark[227].x
        right = face_landmarks.landmark[454].x
        upper = face_landmarks.landmark[10].y
        lower = face_landmarks.landmark[152].y
        width = right - left
        height = abs( upper - lower )  

        self.x1 = left
        self.y1 = upper
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

        # lips
        self.lips_left = face_landmarks.landmark[62].x
        self.lips_right = face_landmarks.landmark[292].x
        self.lips_upper = face_landmarks.landmark[13].y
        self.lips_lower = face_landmarks.landmark[14].y
        self.lips_width = self.lips_right - self.lips_left
        self.lips_height = abs( self.lips_upper - self.lips_lower )

        self.lips = Lips( x1 = self.lips_left, y1 = self.lips_upper, width = self.lips_width, height = self.lips_height )

    def is_located_left(self):
        left = self.center_x <= 0.4
        return left
    def is_located_right(self):
        right = self.center_x >= 0.6
        return right
    def is_located_top(self):
        up = self.center_y <= 0.4
        return up
    def is_located_bottom(self):
        return self.center_y >= 0.6

    def is_mouth_opened(self, ratio = 0.3 ):
        open = (self.lips_height) >= (self.width*ratio)
        return open
    
    def __repr__(self):
        return 'center_x: %.2f, center_y: %.2f, width: %.2f, height: %.2f' % (self.center_x, self.center_y, self.width, self.height)

class Lips():
    def __init__(self,x1,y1,width,height):
        self.x1 = x1
        self.y1 = y1
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.center_x = (self.x1 + self.x2) / 2
        self.center_y = (self.y1 + self.y2) / 2

class Camera():
    def __init__(self, path:any=0, width:int = None, height:int = None ) -> None:

        self.camera = cv2.VideoCapture(path)

        if width is None or height is None:     
            self.width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        else:
            self.width = int(width)
            self.height = int(height)

    def is_opened(self, close_key: int or str = 27) -> bool:
        if not self.camera.isOpened():
            return False

        ret, img = self.camera.read()

        if not ret:
            return False

        if len(str(close_key)) == 1:
            close_key = ord(close_key)
            print(close_key)
            if cv2.waitKey(20) & 0xFF == close_key:
                return False
        else:
            if cv2.waitKey(20) & 0xFF == close_key:
                return False

        self.frame = img
        self.frame = cv2.resize(self.frame, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

        return True

    def get_frame(self, mirror_mode = True):

        if mirror_mode is True:
            self.frame = cv2.flip(self.frame, 1)
        elif mirror_mode is False:
            pass

        return self.frame

    def show(self, frame, window_name = "Window"):
        return cv2.imshow(window_name, frame)

    def draw_faces(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.x1)), int(round(self.height*face.y1))),
                    (int(round(self.width*face.x2)),int(round(self.height*face.y2))),
                    (0,255,0), 3)
    
    def draw_lips(self, faces):
        for face in faces:
            cv2.rectangle(self.frame, (int(round(self.width*face.lips.x1)), int(round(self.height*face.lips.y1))),
                    (int(round(self.width*face.lips.x2)),int(round(self.height*face.lips.y2))),
                    (0,255,0), 3)

    def detect_face(self, frame, max_num_face = 1 , draw_face = True, draw_lips = True) -> object or None:

        mp_face_mesh = mp.solutions.face_mesh

        face = []

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_face,
            refine_landmarks=True,
            min_detection_confidence=0.4, 
            min_tracking_confidence=0.5) as face_mesh:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:  
                        face.append( Face(face_landmarks) )

        if draw_face:
            self.draw_faces(face)

        if draw_lips:
            self.draw_lips(face)

        if len(face) == 1 and max_num_face == 1:
            return face[0]

        return None

    def detect_faces(self, frame, max_num_faces = 99, draw_faces =True, draw_lips = True) -> list:
 
        mp_face_mesh = mp.solutions.face_mesh

        faces = []

        with mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=0.4, 
            min_tracking_confidence=0.5) as face_mesh:

                frame.flags.writeable = False
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame)

                frame.flags.writeable = True
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:  
                        faces.append( Face(face_landmarks) )

        if draw_faces:
            self.draw_faces(faces)

        if draw_lips:
            self.draw_lips(faces)

        return faces




