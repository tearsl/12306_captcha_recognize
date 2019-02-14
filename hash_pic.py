import numpy as np
from PIL import Image


class PQTable:
    def __init__(self):
        pass

    def fit(self, hash_list: list):
        pass

    def find(self, hash_str: str, threshold: float, metric: str):
        pass

    def dump(self):
        pass


def compute_feature_vector(pic: Image, feature_category: str):
    # 由于图片较小，这里直接特征点就是整张图片，也就是特征向量是用来反映整个图片的特征
    # 选择特定类型的函数用来描述当前图片的特征
    # TODO:
    # 利用ORB进行特征点检测，并使用对应特征提取算法，将提取的特征向量使用VLAD，最终得到一个固定长度的特征向量
    to_return = np.zeros([128])
    if feature_category == 'HOG':
        pass
    elif feature_category == 'ORB':
        from skimage.feature import ORB
        orb = ORB()
        to_return = orb.detect_and_extract(np.array(pic))
    else:
        raise Exception("没有适配%s这个特征类型")

    return to_return


def word_pic_tps(pic: Image):
    # 对文字图像进行tps
    return pic


def hash_word_pic(pic_folder):
    # 对图像进行stn-tps形变
    all_pics = []
    all_feature_vector = []
    for m_pic in all_pics:
        transformed_word_pic = word_pic_tps(m_pic)
        # 计算图像的surf特征
        all_feature_vector.append(compute_feature_vector(transformed_word_pic, 'surf'))
    # 配置LSH
    # word_pic_lsh = LSH()
    # word_pic_lsh.fit(all_feature_vector)

    # for m_feature_vector in all_feature_vector:
    #     # 输出每张图的hash字符串到文件
    #     yield word_pic_lsh.transform(m_feature_vector)
    # word_pic_lsh.dump(os.path.join('.','word_pic_lsh.pkl'))


def hash_item_pic():
    # 计算整张图的hog特征
    # 配置LSH
    # 输出每张图的hash字符串到文件
    pass


def load_to_pqtable():
    # 加载当前所有数据加载至pqtable中，并保存为文件
    pass


if __name__ == '__main__':
    pic_path = "./0000ac08-2eb9-11e9-91b2-b4b686ea7832_1.jpg"
    pic = Image.open(pic_path)
    np.set_printoptions(threshold=np.inf)
    print(compute_feature_vector(pic, 'ORB'))
