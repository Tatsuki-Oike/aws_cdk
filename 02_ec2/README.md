## 1 環境構築

```sh
cd ./02_ec2
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

## 2 デプロイ

```bash
export KEY_NAME=SampleKey
cdk deploy -c key_name=$KEY_NAME --require-approval never
# cdk destroy -c key_name=$KEY_NAME --force
```