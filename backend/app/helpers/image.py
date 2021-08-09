from PIL import Image
import requests
from io import BytesIO
import cv2


def read_from_url(url: str):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def read_from_path(path: str):
    image= cv2.imread(path)
    return image
