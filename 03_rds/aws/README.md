## 1 コンテナ起動

```sh
cd ./03_rds/aws
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

## 2 デプロイ

```bash
export KEY_NAME=SampleKey
export USERNAME=admin
export PASSWORD=your_password
export DATABASE_NAME=your_database
cdk deploy -c key_name=$KEY_NAME \
    -c username=$USERNAME \
    -c password=$PASSWORD \
    -c database_name=$DATABASE_NAME \
    --require-approval never

cdk destroy -c key_name=$KEY_NAME \
    -c username=$USERNAME \
    -c password=$PASSWORD \
    -c database_name=$DATABASE_NAME \
    --force
```
