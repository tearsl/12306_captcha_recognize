import random

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from tqdm import tqdm
import uuid
import os
import shutil
import cv2
import numpy as np


def generate_random_points(img_h, img_w, size=10, seed=927):
    np.random.seed(seed)
    return np.hstack((np.random.randint(0, img_w, (size,1)), np.random.randint(0, img_h, (size,1))))


def random_deform_points(img_h, img_w, points_size, seed=927, radius=5):
    origin_points = generate_random_points(img_h, img_w, size=points_size, seed=seed)
    deformed_points = [None] * points_size
    rand = random.Random()
    rand.seed(seed)
    for m_ind, (m_x, m_y) in enumerate(origin_points):
        while True:
            det_x = rand.randint(-radius, radius + 1)
            det_y = rand.randint(-radius, radius + 1)
            if 0 <= det_x + m_x < img_w and 0 <= det_y + m_y < img_h:
                break
        deformed_points[m_ind] = (det_x + m_x, det_y + m_y)
    return origin_points, np.array(deformed_points)


def tps_warp(source, target, img):
    tps = cv2.createThinPlateSplineShapeTransformer()
    source = source[np.newaxis,:,:]
    target = target[np.newaxis,:,:]

    matches = list()
    for i in range(0, len(source[0])):
        matches.append(cv2.DMatch(i, i, 0))

    tps.estimateTransformation(target, source, matches)
    new_img = tps.warpImage(img)
    return new_img


def generate_word_item_pics(folder_path, dictionary_path, generate_size):
    all_words = []
    with open(dictionary_path, encoding='utf-8', mode='r') as to_read:
        for m_line in to_read:
            all_words.append(m_line.strip())
    img_w, img_h = 80, 30
    font_size = 20
    font = ImageFont.truetype('../TengXiangMingSongJian-W1-2.ttf', size=font_size)
    os.makedirs(folder_path, exist_ok=True)
    for i in tqdm(range(generate_size)):
        img = Image.new('RGB', (img_w, img_h), 'black')
        img_draw = ImageDraw(img)
        choiced_word = random.choice(all_words)
        img_draw.text((0, 0), np.unicode(choiced_word), fill='white', font=font)
        origin_points, deform_points = random_deform_points(img_h, img_w, points_size=random.randint(5, 10), radius=2)
        warped_img = 255-tps_warp(origin_points, deform_points, np.array(img))
        cv2.imwrite(os.path.join(folder_path, f'{i}_{choiced_word}.jpg'), warped_img)


if __name__ == '__main__':
    generate_word_item_pics('generate_text_img', '../text_dictionary.txt', 20000)
