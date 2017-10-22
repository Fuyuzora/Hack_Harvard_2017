from face_detection import face_detection as face
from handwriting_to_text import handwriting_to_text as handwriting
import os
import json

# img_list is a list of urls
def photo_analyse (img_list):
    img_path_list = []
    filtered_img_list = []
    for img in img_list:
        detect = face(img)
        if detect is not '[]':
            img_path_list.append(str(img))
            filtered_img_list.append(img)
    analyzed_imgs = []
    text = []
    for i in range(len(filtered_img_list)):
        filtered_img_list[i] = handwriting(filtered_img_list[i])
        lines = json.loads(filtered_img_list[i])['recognitionResult']['lines']
        text.append('')
        for line in lines:
            text[i] += line['text'] + '\n'
    for i in range(len(text)):
        if text[i] not in text[i+1:]:
            analyzed_imgs.append(img_path_list[i])
    print(analyzed_imgs)
    return analyzed_imgs

test_img_list = ["http://joshldavis.com/img/handwriting/dijkstras.png", \
                 "https://media.npr.org/assets/img/2016/04/17/handwritten-note_wide-941ca37f3638dca912c8b9efda05ee9fefbf3147.jpg?s=1400",\
                 "http://joshldavis.com/img/handwriting/dijkstras.png"]
photo_analyse(test_img_list)
