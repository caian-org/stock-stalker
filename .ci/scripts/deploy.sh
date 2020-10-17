#!/usr/bin/env bash

set -ex

python3 -m aws s3 cp "$ARTIFACT" "s3://${AWS_S3_BUCKET}/${ARTIFACT}"

python3 -m aws lambda update-function-code \
   --function-name "$AWS_LAMBDA_NAME" \
   --s3-bucket "$AWS_S3_BUCKET" \
   --s3-key "$ARTIFACT"
