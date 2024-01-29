## 1 環境構築

```sh
cd ./09_route53
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

## 2 デプロイ

```bash
export ACM_ARN=arn:aws:acm:XXX
export HOSTED_ZONE_ID=XXX
export DOMAIN_NAME=XXX.com
cdk deploy --require-approval never\
    -c acm_arn=$ACM_ARN \
    -c hosted_zone_id=$HOSTED_ZONE_ID \
    -c domain_name=$DOMAIN_NAME
    
cdk destroy --force \
    -c acm_arn=$ACM_ARN \
    -c hosted_zone_id=$HOSTED_ZONE_ID \
    -c domain_name=$DOMAIN_NAME
```
