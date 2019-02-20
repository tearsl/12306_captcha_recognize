import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable


class L2Norm(nn.Module):
    def __init__(self):
        super(L2Norm, self).__init__()
        self.eps = 1e-10

    def forward(self, x):
        norm = torch.sqrt(torch.sum(x * x, dim=1) + self.eps)
        x = x / norm.unsqueeze(-1).expand_as(x)
        return x


class L1Norm(nn.Module):
    def __init__(self):
        super(L1Norm, self).__init__()
        self.eps = 1e-10

    def forward(self, x):
        norm = torch.sum(torch.abs(x), dim=1) + self.eps
        x = x / norm.expand_as(x)
        return x


class HardNet(nn.Module):
    """HardNet model definition
    """

    def __init__(self):
        super(HardNet, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32, affine=False),
            nn.ReLU(),
            nn.Conv2d(32, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32, affine=False),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(64, affine=False),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64, affine=False),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(128, affine=False),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(128, affine=False),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Conv2d(128, 128, kernel_size=8, bias=False),
            nn.BatchNorm2d(128, affine=False),

        )
        # self.features.apply(weights_init)

    def input_norm(self, x):
        flat = x.view(x.size(0), -1)
        mp = torch.mean(flat, dim=1)
        sp = torch.std(flat, dim=1) + 1e-7
        return (x - mp.detach().unsqueeze(-1).unsqueeze(-1).unsqueeze(-1).expand_as(x)) / sp.detach().unsqueeze(
            -1).unsqueeze(-1).unsqueeze(1).expand_as(x)

    def forward(self, input):
        x_features = self.features(self.input_norm(input))
        x = x_features.view(x_features.size(0), -1)
        return L2Norm()(x)


class HardNetExtractor:
    def __init__(self,model_path='./HardNet++.pth'):
        model_weights = model_path
        self.model = HardNet()
        checkpoint = torch.load(model_weights, 'cpu')
        self.model.load_state_dict(checkpoint['state_dict'])
        self.model.eval()
        self.model = self.model.cpu()

    def extract(self, patches: list, batch_size=128) -> np.array:
        """
        对所有特征点所包含的ROI进行特征提取

        :param patches:     所有ROI区域
        :return:    len(patches)*128
        """
        assert all(map(lambda x: isinstance(x, np.ndarray), patches)), 'ROI区域需要全部为numpy矩阵'
        assert all(map(lambda x: len(x.shape) == 2, patches)), 'ROI区域必须全部是灰度图像'
        assert all(map(lambda x: x.shape == (32,32), patches)), 'ROI区域为32*32'
        prepared_patches = np.zeros((len(patches), 1, 32, 32))
        for m_ind, m_patch in enumerate(patches):
            prepared_patches[m_ind, 0, :, :] = m_patch / 255. if m_patch.max() > 1 else 1.
        prepared_patches -= 0.443728476019
        prepared_patches /= 0.20197947209
        to_return = np.zeros((len(patches), 128))
        for i in range(0, len(patches), batch_size):
            data_a = prepared_patches[i: i + batch_size, :, :, :].astype(np.float32)
            data_a = torch.from_numpy(data_a)
            data_a = Variable(data_a)
            # compute output
            with torch.no_grad():
                out_a = self.model(data_a)
            to_return[i: i + batch_size, :] = out_a.data.cpu().numpy().reshape(-1, 128)
        assert len(patches) == to_return.shape[0], '输出结果数有误'
        return to_return
