from tesserocr import PyTessBaseAPI
import tesserocr
import cv2
import fastapi

app = fastapi()

img_rgb = cv2.imread("test.png")
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)


images = ['sample.jpg']

# tesserocr.PyTessBaseAPI("/home/pooh/Downloads/tessdata-4.1.0", lang="tha")

# print(tesserocr.image_to_text(img_gray))

with PyTessBaseAPI(path="/home/pooh/Downloads/tessdata-4.1.0", lang="tha") as api:
    # for img in images:
    # api.SetImageFile("test.png")
    api.SetImage(img_gray)
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())
