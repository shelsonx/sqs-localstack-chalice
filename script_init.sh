#!/bin/bash

awslocal s3api create-bucket --bucket website &&
awslocal s3 cp chalicelib/static/index.html s3://website &&
awslocal sqs create-queue --queue-name passwords 