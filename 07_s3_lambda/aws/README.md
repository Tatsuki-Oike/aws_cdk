## 1 コンテナ起動

```sh
cd ./07_s3_lambda/aws
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

## 2 デプロイ

```bash
cdk deploy --require-approval never
```

* .envにAPI GatewayのURLを記述
* frontendのbuild

```bash
export BUCKET_URL=s3://[bucket-name]
aws s3 sync dist $BUCKET_URL --delete
```

## 3 後処理

```bash
rm -r dist/*
aws s3 sync dist $BUCKET_URL --delete
cdk destroy --force
```
