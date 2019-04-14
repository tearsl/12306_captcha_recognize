import os

import torch
from PIL import Image

from torch.autograd import Variable
import numpy as np
from torchvision import transforms

from DeepHash.net import AlexNetPlusLatent


class HashPic:
    def __init__(self, model_file, bits, use_cuda=False):
        self.net = AlexNetPlusLatent(bits)
        self.bits = bits
        self.net.load_state_dict(torch.load(model_file))
        self.use_cuda = use_cuda
        if self.use_cuda:
            self.net = self.net.cuda()
        self.net = self.net.eval()
        self.transform = transforms.Compose(
            [transforms.Resize(227),
             transforms.ToTensor(),
             transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010))])

    def _binary(self, _hash_res):
        return np.round(_hash_res, 0).astype(np.int)

    def _hex(self, _hash_bin_res):
        def __hex(__hash_bin):
            return hex(int(np.sum(np.logspace(base=2, start=3, stop=0, num=4) * __hash_bin)))[2:]

        return "".join([__hex(_hash_bin_res[i * 4:(i + 1) * 4]) for i in range(self.bits // 4)])

    def hash(self, img):
        assert any([isinstance(img, _) for _ in [Image.Image]]), '类型不支持'
        img = self.transform(img).unsqueeze(0)
        with torch.no_grad():
            if self.use_cuda:
                img = Variable(img.cuda())
                res = self.net(img)[0].cpu().numpy().squeeze()
            else:
                res = self.net(Variable(img))[0].numpy().squeeze()
        return self._binary(res)

    def hash_hex(self, img):
        return self._hex(self.hash(img))


if __name__ == '__main__':
    t = HashPic(os.path.join('.', 'AlexNetPlusLatent_89.21.pth'), 128)
    t_img_1 = Image.open('/12306_pics/pics_test_cut/00a11e4e-2f37-11e9-91b9-b4b686ea7832_6.jpg')
    t_img_2 = Image.open('/12306_pics/pics_test_cut/00a11e4e-2f37-11e9-91b9-b4b686ea7832_7.jpg')
    print(t.hash(t_img_1))
    print(t.hash(t_img_2))
