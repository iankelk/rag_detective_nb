#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="rag-detective-api-service"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../../../secrets/
export PERSISTENT_DIR=$(pwd)/../../../persistent-folder/
<<<<<<< HEAD
export GCS_BUCKET_NAME="ac215_scraper_bucket"
=======
# export GCS_BUCKET_NAME="mushroom-app-models"
>>>>>>> 3b132bfe43a2715fef5c920d56008a73d4dffdb0

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .
# M1/2 chip macs use this line
#docker build -t $IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .

# Run the container
docker run --rm --name "$IMAGE_NAME" -ti \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$PERSISTENT_DIR":/persistent \
-p 9000:9000 \
-e DEV=1 \
<<<<<<< HEAD
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
$IMAGE_NAME
=======
$IMAGE_NAME

# -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
# -e GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
>>>>>>> 3b132bfe43a2715fef5c920d56008a73d4dffdb0
