from image_cutout import split_img
from DeepHash import HashPic
from sklearn.cluster import DBSCAN
from sklearn.metrics import hamming_loss


def get_word_img_hash(img):
    pass


def get_item_img_hash(hash_module: HashPic.HashPic, img):
    """
    实现物品图片的哈希化
    :param hash_module: 用于hash化的对象
    :param img:     需要进行化细化的图片
    :return:    返回的hash值
    """
    return hash_module.hash(img)


def set_item_img_hash_cluster(redis_client, img_hash, word_img_cluster_id):
    try:
        redis_client.hash_add(img_hash, word_img_cluster_id)
        return True
    except:
        return False


def add_item_img_hash_to_faiss(faiss_client, item_img_hash):
    faiss_client.add(item_img_hash)


def init_cluster(word_imgs):
    cluster = DBSCAN(min_samples=50, metric=hamming_loss)
    all_imgs_hash = [get_word_img_hash(m_word_img) for m_word_img in word_imgs]
    labels = cluster.fit_predict(all_imgs_hash)
    return cluster, labels


def train(imgs, item_img_hash_module: HashPic, redis_client, faiss_client):
    """
    将文本图像与物品图像进行对应
    NOTE：只支持固定训练，无法进行增量训练
    :param imgs:    训练的图像
    :param item_img_hash_module:   物品图片hash化模块
    :param redis_client:    redis的client实例
    :param faiss_client:    faiss的client实例
    :return:    训练好的文本图像hash值的聚类
    """
    all_word_imgs = []
    all_item_imgs = []
    for m_img in imgs:
        m_word_img, item_imgs = split_img(m_img)
        all_word_imgs.append(m_word_img)
        all_item_imgs.append(item_imgs)
    cluster_instance, cluster_ids = init_cluster(all_word_imgs)
    for m_cluster_id, m_item_imgs in zip(cluster_ids, all_item_imgs):
        for m_item_img in m_item_imgs:
            m_item_img_hash = get_item_img_hash(item_img_hash_module, m_item_img)
            set_item_img_hash_cluster(redis_client, m_item_img_hash, m_cluster_id)
            add_item_img_hash_to_faiss(faiss_client, m_item_img_hash)
    return cluster_instance
