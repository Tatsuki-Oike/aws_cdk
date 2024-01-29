## 1 環境構築

```sh
cd ./05_alb
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

## 2 デプロイ

```bash
cdk deploy --require-approval never
# cdk destroy --force
```
