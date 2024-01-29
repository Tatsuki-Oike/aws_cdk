# Node.jsをベースとする公式イメージを使用
FROM amazonlinux:2023

# CLIのインストール
RUN yum update -y && \
    yum install -y aws-cli && \
    yum clean all

# Node.jsおよびPython-pipのインストール
RUN curl -sL https://rpm.nodesource.com/setup_20.x | bash - && \
    yum install -y nodejs && \
    yum install -y python-pip

# aws-cdkのインストール
RUN npm install -g aws-cdk

# コンテナのデフォルトディレクトリを設定
WORKDIR /app

# requirements.txt
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt
