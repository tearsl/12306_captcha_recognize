# 12306验证码识别

## 项目介绍
另辟蹊径识别12306网页登录验证码。

## 项目依赖
首先获取爬虫代理，框架和方法引用自 [proxy_pool](https://github.com/novioleo/proxy_pool)，
为了进行对图片进行Hash化，这里使用的DeepHash，
为了方便Hash值的检索，这里使用[faiss](https://github.com/facebookresearch/faiss)

## 思路

整个项目是基于假设：当采集样本足够多的时候，同一个文本对应的物品的频率最高的几个一定是跟这个文本相关的。

1. 训练Item图片的DeepHash
2. 训练经过TPS变换的文本图片的DeepHash
3. 建立Item的Hash与文本图片Hash的聚类的关系

## 优势
传统的12306的识别方案是直接对文本的识别，然后再对图像进行分类，然后将分类的结果与OCR的结果进行比对，这样带来的后果就是文本哪存在一定的错误率，图像分类存在一定的错误率，两个错误率相乘，就会效果很差。

而且我们无法保证12306以后的数据库是否会更新，为了保证整个项目变为一个无监督的增量项目，所以采用搜索的形式。

项目如果需要增量，则需要周期性的利用爬虫进行爬取最新的12306的数据。

## 环境
虽然整个项目用的是pytorch作为深度学习框架，但是为了保证环境一致性，整个项目依然会放到docker中。
关于如何安装NVIDIA-Docker，烦请参考[nvidia-docker install.sh](https://github.com/novioleo/DL_Dockerfiles/blob/master/ubuntu_docker_install.sh)


## how to run
```bash
git clone --recurse-submodules https://github.com/tearsl/12306_captcha_recognize
cd 12306_captcha_recognize/Docker
# 如果没有docker-compose需要预先安装docker-compose
# pip install docker-compose
# 第一次运行需要添加--build
docker-compose up # --build
```
启动代理ip池之后，运行crawler，为了避免使用多进程，减少代码复杂程度，想要增加爬虫的并发数直接运行多个即可。

将图片保存到本地之后，运行`python image_cutout.py /path/to/pics/folder`，会在图片所在的文件夹同级目录新建一个文件夹，
以及生成一个映射文件。装载切图后的结果。

进入DeepHash中，运行`train.py`，调整数据集，训练自己的DeepHash的模型。

## Contributors
[Novio](https://github.com/novioleo)  
