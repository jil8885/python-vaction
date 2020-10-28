import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import requests, json


# client_id = os.environ['client_id']
# client_secret = os.environ['client_secret']

def convert():
    file_list = []
    for root, dirs, files in os.walk('lunchparty'):
        for fname in files:
            full_fname = os.path.join(root, fname)

            file_list.append(full_fname)

    for file in file_list:
        basewidth = 960
        img = Image.open(file)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save('resized/' + file.split('/')[1].split('.')[0] + '.png')


def open_img():
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    file_list = []
    for root, dirs, files in os.walk('resized'):
        for fname in files:
            full_fname = os.path.join(root, fname)

            file_list.append(full_fname)
    url = 'https://openapi.naver.com/v1/vision/face'
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    for file in file_list:
        print(file)
        files = {'image': open(file, 'rb')}
        response = requests.post(url, files=files, headers=headers)
        rescode = response.status_code
        if rescode == 200:
            detect_result = json.loads(response.text)['faces']
            img = mpimg.imread(file)
            imgplot = plt.imshow(img)
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(img)
            for each in detect_result['faces']:
                x, y, w, h = each['roi'].values()
                gender, gen_confidence = each['gender'].values()
                emotion, emotion_confidence = each['emotion'].values()
                age, age_confidence = each['age'].values()
                rect_face = patches.Rectangle((x, y), w, h, linewidth=5, edgecolor='r', facecolor='none')
                ax.add_patch(rect_face)
                annotation = age
                plt.figtext(0.15, 0.17, annotation, wrap=True, fontsize=17, color='white')
                plt.show()

open_img()
