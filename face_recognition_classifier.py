import cv2
import numpy as np
import os

def dist(x1,x2):
    return np.sqrt(sum((x1-x2)**2))

def knn(trainset,query_point,k=5):
    X=trainset[:,:-1]
    Y=trainset[:,-1]
    m=X.shape[0]
    vals=[]
    for i in range(m):
        distance=dist(X[i],query_point)
        vals.append((distance,Y[i]))
    #print(distance)
    #vals=list(list(zip(distance,Y)))
    #print(vals)
    vals=sorted(vals)
    vals=vals[:k]
    vals=np.array(vals)
    #print(vals)
    labels_unique=np.unique(vals[:,1],return_counts=True)
    #print(labels_unique)
    index_of_max=labels_unique[1].argmax()
    return labels_unique[0][index_of_max]

cap=cv2.VideoCapture(0)
Face_cascade=cv2.CascadeClassifier("C:\\Users\\Saksham Pandey\\Desktop\\Data science coding blocks\\Face Detection harcascade classifier\\haarcascade_frontalface_alt.xml")
skip=0
face_data=[]
labels=[]
class_id=0
name={}
dataset="./data/"
for fx in os.listdir(dataset):
    if fx.endswith('.npy'):
        name[class_id]=fx[:-4]
        data_item=np.load(dataset+fx)
        face_data.append(data_item)
        target=class_id*np.ones((data_item.shape[0],))
        class_id+=1
        labels.append(target)
face_dataset=np.concatenate(face_data,axis=0)
face_labels=np.concatenate(labels,axis=0).reshape((-1,1))
train_set=np.concatenate((face_dataset,face_labels),axis=1)
print(face_dataset.shape)
print(face_labels.shape)
print(train_set.shape)

#Testing
while True:

    ret,frame=cap.read()
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if ret==False:
        continue

    faces=Face_cascade.detectMultiScale(frame,1.3,5)

    #faces=sorted(faces,key=lambda f:f[2]*f[3]) #sorting face according to size
    for x,y,w,h in faces[-1:]:  # from highest area to lowest
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        offset=10
        face_section=frame[(y-offset):(y+h+offset),(x-offset):(x+w+offset)]
        face_section=cv2.resize(face_section,(100,100))

        out=knn(train_set,face_section.flatten())
        pred_name=name[out]
        cv2.putText(frame,pred_name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
    cv2.imshow("Faces",frame)
    key_pressed=cv2.waitKey(1) & 0xFF
    if key_pressed==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
