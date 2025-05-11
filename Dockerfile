# 使用官方的 Ubuntu 镜像作为基础镜像
FROM ubuntu:latest

ARG AKSK

# 避免在安装过程中出现交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 确保 /app 目录存在
RUN mkdir -p /app

# 工作目录
WORKDIR /app

# 复制当前目录下的文件和文件夹到工作目录
COPY . /app
RUN AKSK=$(cat /run/secrets/mysecret) && sed -i '$d' config.yaml && echo "aksk: \"Bearer $AKSK\"" >> config.yaml

# 确保 /app 目录有足够的权限
RUN chmod -R 755 /app

# 更新系统软件包列表并安装必要的软件包
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# 设置 Python3 为默认的 Python 版本
RUN ln -s /usr/bin/python3 /usr/bin/python

# 设置 Pip3 为默认的 Pip 版本
RUN rm -rf /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip

# Create a virtual environment
RUN cd /app && python3 -m venv /app/venv

# Activate the virtual environment and install any needed packages specified in requirements.txt
RUN cd /app && /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install -r /app/requirements.txt

# Make port 5111 available to the world outside this container
EXPOSE 5111

# Use the Python interpreter from the virtual environment to run the application
CMD ["/app/venv/bin/python", "/app/app.py"]
    
