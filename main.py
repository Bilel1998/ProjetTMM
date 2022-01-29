from PyQt5 import QtWidgets
import sys
import cv2 as cv
import face
import function as fn
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np
class designWindow(QtWidgets.QMainWindow,face.Ui_MainWindow):
    def __init__(self): #initialiser l'interface graphique
        super(designWindow, self).__init__()
        self.setupUi(self)
        self.figimg=fn.makeFigure(self.verticalLayout)
        self.image = fn.makeFigure(self.verticalLayout_2)
        self.capture = fn.makeFigure(self.verticalLayout_3)
        self.pushButton.clicked.connect(self.getImage) #connecter les bouton avec les foncions
        self.pushButton_2.clicked.connect(self.showIm)
        self.pushButton_3.clicked.connect(self.showVid)
    def getImage(self): #parcourir les fichiers image et l'afficher
        file = QtWidgets.QFileDialog.getOpenFileName(self, "choose image", "", "image files (*.jpg)")
        if file[0]:
            self.img = cv.imread(file[0]) #charge l'image a partir de fichiers specifié
            self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB) #conversion de BGR to RGB
            # Affichage de l'image orginale
            self.figimg.clf() #netyoer la fig
            ax = self.figimg.add_subplot(444)
            ax.imshow(self.img, "gray")
            ax.axis("off")
            self.figimg.canvas.draw()

    def showIm(self):
            face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
            classifier = load_model('model32.h5')

            class_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']


            labels = []
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    # make a prediction on the ROI, then lookup the class

                    preds = classifier.predict(roi)[0]
                    print("\nprediction = ", preds)
                    label = class_labels[preds.argmax()]
                    print("\nprediction max = ", preds.argmax())
                    print("\nlabel = ", label)
                    label_position = (x, y)

                    cv2.putText(self.img, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

                else:
                    cv2.putText(self.img, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                print("\n\n")

            #cv2.imshow('Emotion Detector',self.img)

            ax = self.image.add_subplot(111)
            ax.imshow(self.img, "gray")
            ax.axis("off")
            self.image.canvas.draw()







    def showVid(self):
        face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
        classifier = load_model('model32.h5')

        class_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

        cap = cv2.VideoCapture(0)

        while True:
            # Grab a single frame of video
            ret, frame = cap.read()
            labels = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray]) != 0:
                    roi = roi_gray.astype('float') / 255.0
                    roi = img_to_array(roi)
                    roi = np.expand_dims(roi, axis=0)

                    # make a prediction on the ROI, then lookup the class

                    preds = classifier.predict(roi)[0]
                    print("\nprediction = ", preds)
                    label = class_labels[preds.argmax()]
                    print("\nprediction max = ", preds.argmax())
                    print("\nlabel = ", label)
                    label_position = (x, y)
                    cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                else:
                    cv2.putText(frame, 'No Face Found', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                print("\n\n")
            cv2.imshow('Emotion Detector', frame)
            ax = self.capture.add_subplot(111)
            ax.imshow(frame)
            ax.axis("off")
            self.capture.canvas.draw()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break





def main():
    app = QtWidgets.QApplication(sys.argv)
    form =designWindow()
    form.show()
    app.exec_()
if __name__ == "__main__":
    main()