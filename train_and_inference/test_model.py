
import numpy as np
import cv2
import os
import tensorflow as tf 
from tensorflow.keras.models import load_model


#model=load_model("./vgg.h5")
model=load_model("path_to_model")

font=cv2.FONT_HERSHEY_SIMPLEX
path='./split/train'


classn=[]
file1 = open('class_list.txt', 'r') 
Lines = file1.readlines()
for line in Lines: 
    line=line.strip()
    classn.append(line)

classn=sorted(classn)


path_img="path_to_images"
list_imgs=os.listdir(path_img)

for path in list_imgs:
  imgOriginal = cv2.imread(os.path.join(path_img,path))
  img=np.asarray(imgOriginal)
  img=cv2.resize(img,(224,224))
  img=img.reshape(1,224,224,3)
  cv2.putText(imgOriginal,"CLASS:",(20,35),font,0.75,(0,0,255),2,cv2.LINE_AA)
  cv2.putText(imgOriginal,"PROBABILITY:",(20,75),font,0.75,(0,0,255),2,cv2.LINE_AA)
  predictions=model.predict(img)
  label=classn[predictions.argmax()]
  probability_Value=np.amax(predictions)
  if probability_Value>0.75:
    cv2.putText(imgOriginal,label,(120,35),font,2,(0,255,0),3)
    cv2.putText(imgOriginal,str(round(probability_Value*100,2))+"%",(180,75),font,2,(0,255,0),3)
    cv2_imshow(imgOriginal)
    
  if cv2.waitKey(1)&0xFF == ord('q'):
    break