# 12306验证码识别

## 项目介绍
识别12306网页登录验证码

## 项目依赖
首先获取爬虫代理，框架和方法引用自https://github.com/novioleo/proxy_pool

## 思路

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

将图片保存到本地之后，运行denoise.py
## Contributors
[Novio](https://github.com/novioleo)  
