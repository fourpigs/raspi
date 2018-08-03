import os
from echokit import EchoKit
import boto3
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr

app = EchoKit("amzn1.ask.skill.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
handler = app.handler

@app.launch
def on_launch(request, session):
    return app.response("部屋の温湿度を調べるには、つづけて温湿度を訪ねてください")

@app.intent("RASPI_ASK")
def on_intent(request, session):
    data = get_data()
    return app.response("部屋の温度は、{}度、湿度は{}%です".format(data['temp'],data['humi']))

def get_data():
    db = boto3.resource('dynamodb')
    table = db.Table('temphumi')
    data = table.get_item( Key = {'am2320' : 1 } )['Item']
    return data
