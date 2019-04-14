from image_cutout import split_img
from DeepHash import HashPic


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


def add_word_img_hash_to_cluster(cluster, img_hash):
    cluster.add(img_hash)


def get_word_img_hash_cluster_id(cluster, img_hash):
    return cluster.get(img_hash)


def set_item_img_hash_cluster(redis_client, img_hash, word_img_cluster_id):
    try:
        redis_client.hash_add(img_hash, word_img_cluster_id)
        return True
    except:
        return False


def add_item_img_hash_to_faiss(faiss_client, item_img_hash):
    faiss_client.add(item_img_hash)


def init_cluster(imgs):
    cluster = None
    for m_img in imgs:
        word_img, _ = split_img(m_img)
        word_img_hash = get_word_img_hash(word_img)
        add_word_img_hash_to_cluster(cluster, word_img_hash)
    return cluster


def train(imgs, cluster, redis_client, faiss_client):
    for m_img in imgs:
        m_word_img, item_imgs = split_img(m_img)
        m_cluster_id = get_word_img_hash_cluster_id(cluster, get_word_img_hash(m_word_img))
        for m_item_img in item_imgs:
            m_item_img_hash = get_item_img_hash(m_item_img)
            set_item_img_hash_cluster(redis_client, m_item_img_hash, m_cluster_id)
            add_item_img_hash_to_faiss(faiss_client, m_item_img_hash)
