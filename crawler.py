# 爬取12306的验证码
import sys
from io import BytesIO
from time import sleep

import requests
from termcolor import colored
import json
import base64
import os
from uuid import uuid1
from PIL import Image
import datetime

from urllib3.exceptions import InsecureRequestWarning
import urllib3
# 关闭ssl警告
urllib3.disable_warnings(InsecureRequestWarning)

url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64'

proxy_pool_host_ip = 'localhost'
proxy_pool_host_port = 5010


def get_proxy_ip():
    try:
        ip_and_port = requests.get(
            "http://{ip}:{port}/get".format_map({'ip': proxy_pool_host_ip, 'port': proxy_pool_host_port})).text
        if ip_and_port == 'no proxy!':
            return None,None
        return ip_and_port.strip().split(':')
    except Exception as e:
        print(e)
        return None,None


def validation_proxy(ip, port, test_url='https://www.12306.cn/index/images/logo.jpg'):
    proxy = {
        "http": "http://%s:%s" % (ip, port),
        "https": "https://%s:%s" % (ip, port),
    }
    try:
        if requests.get(test_url, proxies=proxy, verify=False, timeout=5).status_code == 200:
            return True
        return False
    except:
        return False


def delete_proxy(ip, port):
    try:
        requests.get(
            "http://{ip}:{port}/delete?proxy={proxy_ip}:{proxy_port}".format_map(
                {'ip': proxy_pool_host_ip,
                 'port': proxy_pool_host_port,
                 'proxy_ip': ip,
                 'proxy_port': port,
                 }))
        pass
    except Exception as e:
        print(e)


def get_pic(proxy_ip, proxy_port):
    try:
        req = requests.get(url, proxies={'https': 'https://%s:%s' % (proxy_ip, proxy_port)}, verify=False, timeout=5)
        if req.status_code == 200:
            try:
                json_res = json.loads(req.text)
                return json_res['image']
            except Exception as e:
                print(e)
                return False
    except Exception as te:
        print(te)
        delete_proxy(proxy_ip, proxy_port)
        return False


def sink_pic(image_base64_str, target_folder):
    os.makedirs(target_folder, exist_ok=True)
    try:
        target_path = os.path.join(target_folder, str(uuid1()) + '.jpg')
        im = Image.open(BytesIO(base64.b64decode(image_base64_str)))
        im.save(target_path)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    success_counter = 0
    while True:
        cur_hour = datetime.datetime.now().hour
        if cur_hour >= 23 or cur_hour < 6:
            sleep(3600)
            continue
        proxy_ip, proxy_port = get_proxy_ip()
        if proxy_ip is None and proxy_port is None:
            print("当前没有可用的代理ip了，睡60秒")
            sleep(60)
            continue
        if validation_proxy(proxy_ip, proxy_port):
            print("Test Success:", colored('%s:%s' % (proxy_ip, proxy_port), 'green'))
            pic = get_pic(proxy_ip, proxy_port)
            pic_size = sys.getsizeof(pic)
            if isinstance(pic, str) and pic_size > 3000:
                sink_pic(pic.encode('utf-8'), os.path.join('.', 'pics'))
                success_counter += 1
                print(success_counter)
        else:
            print("Test Fail:", colored('%s:%s' % (proxy_ip, proxy_port), 'red'))
            delete_proxy(proxy_ip, proxy_port)
