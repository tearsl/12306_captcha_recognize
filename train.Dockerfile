from pytorch/pytorch:0.4.1-cuda9-cudnn7-runtime
WORKDIR /project
# 配置国内源
run pip install pip -U
run pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
add requirements.txt .
run pip install -r requirements.txt
# 如果没有，那么就需要单独去下
# run curl --create-dirs -o /root/.torch/models/alexnet-owt-4df8aa71.pth https://download.pytorch.org/models/alexnet-owt-4df8aa71.pth
run mkdir -p /root/.torch/models
copy alexnet-owt-4df8aa71.pth /root/.torch/models/
