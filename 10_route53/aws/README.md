## 1 コンテナ起動

```sh
cd ./10_route53/aws
docker run -it --rm --name aws-container \
    -v ~/.aws:/root/.aws \
    -v ~/.ssh:/root/.ssh \
    -v "$(pwd)"/src:/app \
    aws-image /bin/bash
```

## 2 デプロイ

* .envにAPI GatewayのURLを記述
* frontendのbuild

```bash
export US_ACM_ARN=arn:aws:acm:XXXXXX
export ACM_ARN=arn:aws:acm:XXXXX
export HOSTED_ZONE_ID=XXXXX
export DOMAIN_NAME=XXXXX.com
cdk deploy --require-approval never \
    -c us_acm_arn=$US_ACM_ARN \
    -c acm_arn=$ACM_ARN \
    -c hosted_zone_id=$HOSTED_ZONE_ID \
    -c domain_name=$DOMAIN_NAME
```

```bash
export BUCKET_URL="s3://www.dslabsample.com"
aws s3 rm $BUCKET_URL --recursive
cdk destroy --force \
    -c us_acm_arn=$US_ACM_ARN \
    -c acm_arn=$ACM_ARN \
    -c hosted_zone_id=$HOSTED_ZONE_ID \
    -c domain_name=$DOMAIN_NAME
```
