## 1 コンテナ起動

```sh
cd ./04_s3
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

## 3 S3に画像アップロード

```sh
export BUCKET_URL=s3://[bucket-name]
aws s3 cp cat.jpg $BUCKET_URL
aws s3 rm $BUCKET_URL --recursive
```
