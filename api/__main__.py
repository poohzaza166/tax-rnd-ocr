# from fastapi import FastAPI, File, UploadFile
# from pydantic import BaseModel
# from typing import List
# import sqlite3
# import json
#
# app = FastAPI()
#
# conn = sqlite3.connect('data.db')
# c = conn.cursor()
#
#
# class Item(BaseModel):
#     status: int
#     data: dict
#     api_key: str
#
#
# @app.get('/items/', response_model=List[Item])
# def get_items():
#     c.execute('SELECT * FROM items')
#     items = c.fetchall()
#     return [Item(**item) for item in items]
#
#
# @app.post('/items/', response_model=Item)
# def create_item(item: Item):
#     c.execute('INSERT INTO items VALUES (:id, :name, :description, :price)', item.dict())
#     conn.commit()
#     return item
#
#
# @app.post('/upload/')
# async def upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     save_path = f'uploads/{file.filename}'
#     with open(save_path, 'wb') as f:
#         f.write(contents)
#     return {'filename': file.filename}
#
#
# @app.get('/info')
# def get_info():
#     return json.dumps({'date': '2023-09-19'})

from .chatbot import Chatbot
from plugins.greetings_plugin import GreetingsPlugin

bot = Chatbot()

bot.process("Hello world!")
# Prints "Hello there!"
bot.process("joke")

bot.process("This text won't match")
# No output