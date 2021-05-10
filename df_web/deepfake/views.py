from operator import truediv
from typing import List
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http.response import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
from glob import glob
import multiprocessing
import math
import cv2 as cv
from tqdm import tqdm_notebook
import dlib
from tensorflow.keras.models import load_model
from keras.preprocessing import image
from matplotlib import pyplot
import json
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json


# from mtcnn.mtcnn import MTCNN


model = load_model(r'C:\Users\ankit\OneDrive\Desktop\deepfakes\XceptionLatest.h5')
dense = load_model(r'C:\Users\ankit\OneDrive\Desktop\deepfakes\DensenetComplete.h5')


def main(request):
    context={'a':1}
    return render(request, 'main.html',context)

@csrf_exempt 
def predictImage(request):
    if request.method == 'POST':            
        fileObj = request.FILES['imagePath']
        fs = FileSystemStorage()
        filePathName= fs.save(fileObj.name,fileObj)
        filePathName = fs.url(filePathName)
        frame_pred = {}
        list = []
        faces = []
        frames = []
        fakeList = []
        crop = []
        prob = "undefined"
        name = filePathName.split('/')[-1]
        frame_pred.update({"filename": filePathName})
        BASE_DIR=r'C:\Ankit\proj\git\fyp\df_web'
        filePathName=BASE_DIR+filePathName
        print(filePathName)
        print(BASE_DIR)
        img = cv.imread(filePathName)
        tempName = name[0:-4]
        angle = crop_faces(img)
        cropped_faces = cropped(img)
        rotated_faces = rotate(img,angle)
        x = 1
        try:
            img = cv.resize(img, (299, 299))
        except:
            pass
        filename = tempName + str(int(x)) + ".jpg"
        frames.append('./media/frames/'+filename)
        z = 1
        y = 1
        cv.imwrite('C:/Ankit/proj/git/fyp/client/deepfake/public/media/frames/'+filename, img)
        if len(cropped_faces) > 0:
            for face in cropped_faces:
                facename = tempName +  str(int(z)) + ".jpg"
                z+=1
                face = cv.resize(face, (299, 299))
                cv.imwrite('C:/Ankit/proj/git/fyp/client/deepfake/public/media/faces/'+facename, face)
                faceDict = {
                    'file':'./media/faces/'+facename,
                    'frame':x
                }
                crop.append(faceDict)

        if len(rotated_faces) > 0:
            for face in rotated_faces:
                facename = tempName +  str(int(y)) + ".jpg"
                y+=1
                face = cv.resize(face, (299, 299))
                cv.imwrite('C:/Ankit/proj/git/fyp/client/deepfake/public/media/aligned/'+facename, face)
                print("face(s) are cropped, sending to prediction")
                face = face/255
                face_ = np.expand_dims(face, axis=0)
                prob = model.predict_proba(face_)[0][0]
                if prob>0.5:
                    fakeDict = {
                    'prob':str(prob),
                    'file':'./media/aligned/'+facename,
                    'frame':x
                    }
                    fakeList.append(fakeDict)
                    # fakeList.append(facename)
                faceDict = {
                    'prob':str(prob),
                    'file':'./media/aligned/'+facename,
                    'frame':x
                }
                list.append(faceDict)
  

        context={"filePathName":filePathName,'fakeList':fakeList,'faces':list, 'frames':frames,'cropped':crop}
        return JsonResponse({"res":context}, safe=False)
    else:
        return HttpResponse("No file uploaded")

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)

def crop_faces(img):
    angle_arr = []
    # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = img
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')
    rects = detector(gray, 0)
    if len(rects) > 0:
        for rect in rects:
            x = rect.left()
            y = rect.top()
            w = rect.right()
            h = rect.bottom()
            shape = predictor(gray, rect)
            print(shape)
            shape = shape_to_normal(shape)
            nose, left_eye, right_eye = get_eyes_nose_dlib(shape)
            center_of_forehead = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)
            center_pred = (int((x + w) / 2), int((y + y) / 2))
            length_line1 = distance(center_of_forehead, nose)
            length_line2 = distance(center_pred, nose)
            length_line3 = distance(center_pred, center_of_forehead)
            cos_a = cosine_formula(length_line1, length_line2, length_line3)
            angle = np.arccos(cos_a)
            rotated_point = rotate_point(nose, center_of_forehead, angle)
            rotated_point = (int(rotated_point[0]), int(rotated_point[1]))
            if is_between(nose, center_of_forehead, center_pred, rotated_point):
                angle = np.degrees(-angle)
            else:
                angle = np.degrees(angle)
            print(angle)
            angle_arr.append(angle)
    return angle_arr

def rotate(frame,angle):
    detector = dlib.get_frontal_face_detector()
    # image= cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    faces = detector(frame, 1)
    cropped_faces = []
    i=0
    if len(faces) > 0:
        rects, scores, idx = detector.run(frame, 0)
        for rect in rects:
            if len(rects) > 0:
                (x, y, w, h) = rect_to_bb(rect)
                roi = frame[(y - 50):(y + int(1.5*h)), (x - 50):(x + int(1.5*w))]
                try:
                    roi_ = cv.resize(roi, (299, 299))
                    img = Image.fromarray(roi_)
                    img = np.array(img.rotate(angle[i]))
                    i+=1
                    cropped_faces.append(img)
                except:
                    pass
    return cropped_faces

def cropped(frame):
    detector = dlib.get_frontal_face_detector()
    # image= cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    faces = detector(frame, 1)
    cropped_faces = []
    i=0
    if len(faces) > 0:
        rects, scores, idx = detector.run(frame, 0)
        for rect in rects:
            if len(rects) > 0:
                (x, y, w, h) = rect_to_bb(rect)
                roi = frame[(y - 50):(y + int(1.5*h)), (x - 50):(x + int(1.5*w))]
                try:
                    roi_ = cv.resize(roi, (299, 299))
                    cropped_faces.append(roi_)
                except:
                    pass
    return cropped_faces

@csrf_exempt 
def predictVideo(request):
    if request.method == 'POST': 
        print(request,"nnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        fileObj = request.FILES['imagePath']
        fs = FileSystemStorage()
        filePathName= fs.save(fileObj.name,fileObj)
        filePathName = fs.url(filePathName)
        print(fileObj)
        print(filePathName)
        frame_pred = {}
        list = []
        frames = []
        fakeList = []
        crop = []
        name = filePathName.split('/')[-1]
        tempName = name[0:-4]
        frame_pred.update({"filename": filePathName})
        BASE_DIR=r'C:\Users\ankit\OneDrive\Desktop\deepfakes\fake-video2.mp4'
        filePathName=BASE_DIR+filePathName
        print(filePathName)
        print(BASE_DIR)
        cap = cv.VideoCapture(BASE_DIR)
        frame_pred.update({"filename": name})
        x = 0
        y = 1
        z = 1
        frameRate = cap.get(5)  
        while(cap.isOpened()):
            print("kkkk")
            frameId = cap.get(1)  
            ret, frame = cap.read()
            if (ret != True):
                break
            if (ret) & (frameId % math.floor(frameRate) == 0):
                angle = crop_faces(frame)
                cropped_faces = cropped(frame)
                rotated_faces = rotate(frame,angle)
                try:
                    frame = cv.resize(frame, (299, 299))
                except:
                    pass
                filename =  tempName + str(int(x)) + ".jpg"
                frames.append('./media/frames/'+filename)
                x+=1
                cv.imwrite('C:/Ankit/proj/git/fyp/client/deepfake/public/media/frames/'+filename, frame)
                print(len(cropped_faces))
                if len(cropped_faces) > 0:
                    for face in cropped_faces:
                        facename = tempName +  str(int(z)) + ".jpg"
                        z+=1
                        face = cv.resize(face, (299, 299))
                        cv.imwrite('C:/Ankit/proj/git/fyp/client/deepfake/public/media/faces/'+facename, face)
                        faceDict = {
                            'file':'./media/faces/'+facename,
                            'frame':x
                        }
                        crop.append(faceDict)

                if len(rotated_faces) > 0:
                    for face in rotated_faces:
                        facename = tempName +  str(int(y)) + ".jpg"
                        y+=1
                        face = cv.resize(face, (299, 299))
                        cv.imwrite('C:/Ankit/proj/git/fyp/client/deepfake/public/media/aligned/'+facename, face)
                        print("face(s) are cropped, sending to prediction")
                        face = face/255
                        face_ = np.expand_dims(face, axis=0)
                        prob = dense.predict_proba(face_)[0][0]
                        if prob>0.5:
                            fakeDict = {
                            'prob':str(prob),
                            'file':'./media/aligned/'+facename,
                            'frame':x
                            }
                            fakeList.append(fakeDict)
                            # fakeList.append(facename)
                        faceDict = {
                            'prob':str(prob),
                            'file':'./media/aligned/'+facename,
                            'frame':x
                        }
                        list.append(faceDict)
            if(x==3):
                cap.release()
        context={"filePathName":filePathName,'fakeList':fakeList,'faces':list, 'frames':frames,'cropped':crop}
        return JsonResponse({"res":context}, safe=False)
        # context={'filePathName':filePathName, 'probability':list,'fakeList':fakeList,'faces':list, 'frames':frames,'cropped':crop}
        # return render(request, 'result.html',context)
    else:
        return HttpResponse("No file uploaded")

def shape_to_normal(shape):
    shape_normal = []
    for i in range(0, 5):
        shape_normal.append((i, (shape.part(i).x, shape.part(i).y)))
    return shape_normal

def get_eyes_nose_dlib(shape):
    nose = shape[4][1]
    left_eye_x = int(shape[3][1][0] + shape[2][1][0]) // 2
    left_eye_y = int(shape[3][1][1] + shape[2][1][1]) // 2
    right_eyes_x = int(shape[1][1][0] + shape[0][1][0]) // 2
    right_eyes_y = int(shape[1][1][1] + shape[0][1][1]) // 2
    return nose, (left_eye_x, left_eye_y), (right_eyes_x, right_eyes_y)

def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def cosine_formula(length_line1, length_line2, length_line3):
    cos_a = -(length_line3 ** 2 - length_line2 ** 2 - length_line1 ** 2) / (2 * length_line2 * length_line1)
    return cos_a

def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy

def is_between(point1, point2, point3, extra_point):
    c1 = (point2[0] - point1[0]) * (extra_point[1] - point1[1]) - (point2[1] - point1[1]) * (extra_point[0] - point1[0])
    c2 = (point3[0] - point2[0]) * (extra_point[1] - point2[1]) - (point3[1] - point2[1]) * (extra_point[0] - point2[0])
    c3 = (point1[0] - point3[0]) * (extra_point[1] - point3[1]) - (point1[1] - point3[1]) * (extra_point[0] - point3[0])
    if (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0):
        return True
    else:
        return False
   