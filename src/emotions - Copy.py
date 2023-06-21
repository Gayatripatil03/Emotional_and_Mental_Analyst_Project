import numpy as np
import argparse
import matplotlib.pyplot as plt
import speech_recognition as sr
import pyttsx3
import cv2
import pymysql
import xlwt
from xlwt import Workbook
import xlrd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import time
from gtts import gTTS
import random
from playsound import playsound

r=sr.Recognizer()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

mydb=pymysql.connect(host="localhost",user="root",password="root",database="emotionanalyst")
mycursor=mydb.cursor()


# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
mode = ap.parse_args().mode

playsound("raw/welcome.mp3")

# plots accuracy and loss curves
def plot_model_history(model_history):
    """
    Plot Accuracy and Loss curves given the model_history
    """
    fig, axs = plt.subplots(1,2,figsize=(15,5))
    # summarize history for accuracy
    axs[0].plot(range(1,len(model_history.history['accuracy'])+1),model_history.history['accuracy'])
    axs[0].plot(range(1,len(model_history.history['val_accuracy'])+1),model_history.history['val_accuracy'])
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,len(model_history.history['accuracy'])+1),len(model_history.history['accuracy'])/10)
    axs[0].legend(['train', 'val'], loc='best')
    # summarize history for loss
    axs[1].plot(range(1,len(model_history.history['loss'])+1),model_history.history['loss'])
    axs[1].plot(range(1,len(model_history.history['val_loss'])+1),model_history.history['val_loss'])
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,len(model_history.history['loss'])+1),len(model_history.history['loss'])/10)
    axs[1].legend(['train', 'val'], loc='best')
    fig.savefig('plot.png')
    plt.show()

# Define data generators
train_dir = 'data/train'
val_dir = 'data/test'

num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50

train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(48,48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')

validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(48,48),
        batch_size=batch_size,
        color_mode="grayscale",
        class_mode='categorical')

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))
mode="display"
#---------------------Reading from excel-------------------------------
loc = ("Questions.xls")
loc1 = ("Answer.xls")
wb = xlrd.open_workbook(loc)
wb1= xlwt.Workbook(encoding="utf-8")
sheet1 = wb1.add_sheet('Sheet 1')

sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
print(sheet.nrows)
rows=sheet.nrows
#list to stored quetion dataset
que=[]
cat=[]
indices=[]
answers=[]
for i in range(1,rows):
    que.append(sheet.cell_value(i, 0))
    cat.append(sheet.cell_value(i, 1))
    answers.append(sheet.cell_value(i, 2))

MyText=""

# If you want to train the same model or try other models, go for this
if mode == "train":
    model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])
    model_info = model.fit_generator(
            train_generator,
            steps_per_epoch=num_train // batch_size,
            epochs=num_epoch,
            validation_data=validation_generator,
            validation_steps=num_val // batch_size)
    plot_model_history(model_info)
    model.save_weights('model.h5')

# emotions will be displayed on your face from the webcam feed
elif mode == "display":
    model.load_weights('model.h5')

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    mytext=""
    # start the webcam feed
    cap = cv2.VideoCapture(0)
    writecount=0
    while True:
        print("started")
        # Find haar cascade to draw bounding box around face
        ret, frame = cap.read()
        if not ret:
            break
        facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
      
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            print(emotion_dict[maxindex])
            r1 = random.randint(1,10000000)
            r2 = random.randint(1,10000000)
            randfile = str(r2)+"randomtext"+str(r1) +".mp3"
            #-----------------Random Question Pattern generation--------------
            ind=0
            print("emotion",emotion_dict[maxindex])
            emotion=emotion_dict[maxindex]
            for x in cat:
                if(x==emotion):
                    indices.append(ind)
                ind=ind+1
                print(x)
            ele=random.choice(indices)
            
            mytext=que[ele]
            print(mytext)
            lan='en'
            a1=gTTS(text=mytext,lang=lan,slow=False)
            a1.save(randfile)
            playsound(randfile)

            #--------------------speech to text--------------------
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print(""+MyText)
                
                sql="insert into uanswer (Answer,Cat)values(%s,%s)"
                values=(""+MyText,""+emotion_dict[maxindex])
                mycursor.execute(sql,values)
                mydb.commit()
               
        cv2.imshow('Video', cv2.resize(frame,(600,960),interpolation = cv2.INTER_CUBIC))    
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    cap.release()
    cv2.destroyAllWindows()
