from pyzbar import pyzbar  # replaces zbar
from PIL import Image
import cv2
import MySQLdb  # from mysqlclient package on Python 3
import numpy as np
import os
import datetime
import time

# --- connect to MySQL from environment variables with retry ---
def connect_db_with_retry(retries=20, delay=2):
    host = os.environ.get("MYSQL_HOST", "mysql")
    user = os.environ.get("MYSQL_USER", "root")
    pwd  = os.environ.get("MYSQL_PASSWORD", "root")
    dbn  = os.environ.get("MYSQL_DB", "qr_information")
    for i in range(retries):
        try:
            print(f"Connecting to MySQL at {host} (attempt {i+1}/{retries})")
            return MySQLdb.connect(host=host, user=user, passwd=pwd, db=dbn)
        except Exception as e:
            print(f"DB not ready yet: {e}")
            time.sleep(delay)
    raise RuntimeError(f"Could not connect to MySQL at {host} after {retries} retries")

db = connect_db_with_retry()
cursor = db.cursor()
capture = cv2.VideoCapture(0)


def present(fn):
    sql = "SELECT * FROM registration WHERE `Sr_No.` = '%s'" % (fn)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        sn = row[0]
    return sn


def face_rec(sn):
    # dataset creator
    faceDetect = cv2.CascadeClassifier("recognizer/haarcascade_frontalface_default.xml")
    id = sn

    # read image from database
    sql = "SELECT * FROM registration WHERE `Sr_No.` = '%s'" % (id)
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        data = row[6]
        with open("photo1.jpg", 'wb') as f:
            f.write(data)

    img = cv2.imread('photo1.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.imwrite("dataSet/User." + str(id) + ".0.jpg", gray[y:y + h, x:x + w])
        cv2.waitKey(100)

    cv2.waitKey(1)

    # trainer
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # new API
    path = 'dataSet'

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.waitKey(100)
        return np.array(IDs), faces

    Ids, Faces = getImagesWithID(path)
    recognizer.train(Faces, Ids)
    recognizer.save('recognizer/trainingData.yml')

    rec = cv2.face.LBPHFaceRecognizer_create(threshold=125)
    rec.read("recognizer/trainingData.yml")

    loop = True
    while loop:
        ret, img = capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        cv2.imshow("Current", img)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            id, conf = rec.predict(gray[y:y + h, x:x + w])
            if id == sn:
                name = "Present "
                print(conf)
                cv2.imwrite("sample.jpg", gray[y:y + h, x:x + w])
                cv2.waitKey(100)
                loop = False
            else:
                name = "unknown "
                print(conf)
            if not loop:
                print(id)
                print(name)
                t = str(datetime.datetime.now())
                print(t)
                with open("sample.jpg", 'rb') as f:
                    pic = f.read()
                query = "INSERT INTO attendance (srno,number,time) VALUES (1,%d,'%s')" % (id, t)
                c = db.cursor()
                n = c.execute(query)
                print(n)
            cv2.putText(img, name, (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)
            cv2.imshow("Current", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        try:
            os.remove("dataSet/User." + str(id) + ".0.jpg")
            os.remove("recognizer/trainingData.yml")
            os.remove('photo1.jpg')
        except OSError:
            pass

    cv2.destroyAllWindows()


def main():
    flag = True
    qr_decoded = ''
    while flag:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret, frame = capture.read()
        cv2.imshow('Current', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # decode QR codes with pyzbar
        decoded_objects = pyzbar.decode(gray)
        for decoded in decoded_objects:
            flag = False
            qr_decoded = decoded.data.decode('utf-8')
            no = present(qr_decoded)
            cv2.waitKey(20)
            face_rec(no)
            capture.release()
            db.commit()
            db.close()


if __name__ == "__main__":
    main()
