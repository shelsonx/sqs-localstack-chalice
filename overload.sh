#!/bin/bash

for i in {1..50}; do
    echo $i
    awslocal --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/passwords --message-body "Mensagem $i"
done