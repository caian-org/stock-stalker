#!/usr/bin/env bash

set -ex
export PATH="$PATH:$HOME/.local/bin"

# ------------------------------------------------
printf "\n----- UPLOADING TO S3...\n\n"
aws s3 cp "$ARTIFACT" "s3://${AWS_S3_BUCKET}/${ARTIFACT}"

# ------------------------------------------------
printf "\n----- UPDATING FUNCTION CODE...\n"
aws lambda update-function-code \
   --function-name "$AWS_LAMBDA_NAME" \
   --s3-bucket "$AWS_S3_BUCKET" \
   --s3-key "$ARTIFACT"

# ------------------------------------------------
printf "\n----- DONE!\n"
