from pytorch/pytorch:1.0.1-cuda10.0-cudnn7-runtime
WORKDIR /project
# 配置国内源
pip install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
add requirements.txt ./
pip install -r requirements.txt
