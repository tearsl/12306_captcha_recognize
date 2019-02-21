import pickle

from sklearn.cluster import KMeans
import numpy as np


class VLAD:
    def __init__(self, exist_visual_dict: str = None, k=8):
        if exist_visual_dict is not None:
            with open(exist_visual_dict, 'rb') as to_read_model:
                self.visual_dict = pickle.load(to_read_model)
        else:
            self.visual_dict = None
        self._k = k
        pass

    def train(self, dataset, dump_location: str):
        self.visual_dict = KMeans(n_clusters=self._k, init='k-means++', tol=0.0001, verbose=1).fit(dataset)
        with open(dump_location, 'wb') as to_write_model:
            pickle.dump(self.visual_dict, to_write_model)

    def aggregate(self, feature_vectors) -> np.ndarray:
        assert self.visual_dict is not None, '字典未训练或者加载'

        predicted_labels = self.visual_dict.predict(feature_vectors)
        centers = self.visual_dict.cluster_centers_
        k = self._k
        m, d = feature_vectors.shape
        V = np.zeros([k, d])
        for i in range(k):
            if np.sum(predicted_labels == i) > 0:
                V[i] = np.sum(feature_vectors[predicted_labels == i, :] - centers[i], axis=0)
        V = V.flatten()
        V = np.sign(V) * np.sqrt(np.abs(V))
        V = V / np.sqrt(np.dot(V, V))
        return V
