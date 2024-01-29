## 1 コンテナ環境作成

```sh
cd 01_env
docker build -t aws-image .
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

```bash
aws --version
cdk --version
```

## 2 AWSでシークレットキー作成

* コンソールでシークレットキー作成

aws_access_key_id: XXXXXXXXX <br>
aws_secret_access_key: XXXXXXXXX <br>
region: ap-northeast-1 <br>
output format: json

```bash
aws configure
cat ~/.aws/credentials
cat ~/.aws/config
```

## 3 SSHキー作成

```bash
export KEY_NAME=SampleKey
aws ec2 create-key-pair --key-name ${KEY_NAME} --query 'KeyMaterial' --output text > ${KEY_NAME}.pem
```

```bash
mv SampleKey.pem ~/.ssh/
chmod 400 ~/.ssh/SampleKey.pem 
```

## 4 デプロイと消去

```bash
cdk bootstrap -c key_name=$KEY_NAME # 最初の一度だけ
cdk deploy -c key_name=$KEY_NAME --require-approval never
cdk destroy -c key_name=$KEY_NAME --force
```