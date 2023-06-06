from chalice import Chalice, Response
import boto3
import json
from trycourier import Courier
import os
import re

ENDPOINT_URL_SEND ='http://host.docker.internal:4566'
ENDPOINT_URL_RECEIVE = "http://host.docker.internal:4566/_aws/sqs/messages"
QUEUE_URL = "http://queue.localhost.localstack.cloud:4566/000000000000"
QUEUE_NAME = 'passwords'
BUCKET_NAME = 'website'
PAGE = 'index.html'
MESSAGE_SUCCESS = "Parabéns! Senha cadastrada com sucesso!"
MESSAGE_ERROR = "Error! Senha não passou nas politicas requeridas."


app = Chalice(app_name='queueSQS')
app.debug = True

def send_mail(email, body):
    client = Courier(auth_token=os.environ.get("KEY_COURIER"))

    resp = client.send_message(
        message={
            "to": {
            "email": email
            },
            "content": {
            "title": "System KWS, analysis result!",
            "body": body
            },
        }
    )

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password) or \
       not re.search(r'[a-z]', password) or \
       not re.search(r'\d', password) or \
       not re.search(r'[\W_]', password):
        return False
    return True

def send_message(data):
	try:
		sqs = boto3.client('sqs', endpoint_url=ENDPOINT_URL_SEND)
		sqs.send_message(
			QueueUrl=f'{QUEUE_URL}/{QUEUE_NAME}',
			MessageBody=json.dumps(data)
		)
	except Exception as e:
		return (str(e))

@app.route('/cadastro', methods=['POST'], cors=True)
def receive_data():
	try:
		paraments = app.current_request.json_body
		return send_message(paraments)
	except Exception as e:
		return (str(e))

@app.route('/', methods=['GET'])
def index():
    s3 = boto3.client('s3', endpoint_url=ENDPOINT_URL_SEND)
    response = s3.get_object(Bucket=BUCKET_NAME, Key=PAGE)
    page = response['Body'].read().decode('utf-8')
    return Response(
		body=page, 
		headers={'Content-Type': 'text/html'},
		status_code=200)

@app.on_sqs_message(queue=QUEUE_NAME)
def on_event(event):
	try:
		for record in event:
			data = json.loads(record.body)
			if (validate_password(data['password'])):
				send_mail(data['email'], f'{MESSAGE_SUCCESS} {data["password"]}')
			else:
				send_mail(data['email'], f'{MESSAGE_ERROR} {data["password"]}')
	except:
		pass