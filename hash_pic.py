import os

import numpy as np
from PIL import Image


class LSH:
    def __init__(self):
        pass

    def fit(self, feature_vectors: list):
        pass

    def transform(self, feature_vector: np.array):
        pass

    def dump(self,dump_path):
        pass


class PQTable:
    def __init__(self):
        pass

    def fit(self, hash_list: list):
        pass

    def find(self, hash_str: str, threshold: float, metric: str):
        pass

    def dump(self):
        pass


def compute_feature_vector(pic, feature_category: str):
    # 选择特定类型的函数用来描述当前图片的特征
    return np.zeros([128])


def word_pic_tps(pic:Image):
    # 对文字图像进行tps
    return pic


def hash_word_pic(pic_folder):
    # 对图像进行stn-tps形变
    all_pics = []
    all_feature_vector = []
    for m_pic in all_pics:
        transformed_word_pic = word_pic_tps(m_pic)
        # 计算图像的surf特征
        all_feature_vector.append(compute_feature_vector(transformed_word_pic,'surf'))
    # 配置LSH
    word_pic_lsh = LSH()
    word_pic_lsh.fit(all_feature_vector)

    for m_feature_vector in all_feature_vector:
        # 输出每张图的hash字符串到文件
        yield word_pic_lsh.transform(m_feature_vector)
    word_pic_lsh.dump(os.path.join('.','word_pic_lsh.pkl'))


def hash_item_pic():
    # 计算整张图的hog特征
    # 配置LSH
    # 输出每张图的hash字符串到文件
    pass


def load_to_pqtable():
    # 加载当前所有数据加载至pqtable中，并保存为文件
    pass
