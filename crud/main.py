from __future__ import annotations
from fastapi import FastAPI, HTTPException
from dataclasses import dataclass
from sqlalchemy import create_engine
import pandas as pd


app = FastAPI()
engine = create_engine('sqlite:///example.db')


@dataclass
class Book:
    id: int
    title: str
    author: str
    publisher: str

    @classmethod
    def create(cls, data: Book):
        query = f"INSERT INTO book VALUES ({data.id}, '{data.title}', '{data.author}', '{data.publisher}');"
        engine.execute(query)
        return cls.read(id=data.id)

    @classmethod
    def read(cls, id: int):
        query = f'SELECT * FROM book WHERE id = {id};'
        df = pd.read_sql(query, engine)
        records = df.to_dict('records')
        if len(records) == 0:
            # no matches - raise 404 - not found
            raise HTTPException(status_code=404, detail="Product not found")
        elif len(records) < 1:
            # multiple records, raise 500 - internal error - contact administrator
            raise HTTPException(status_code=500, detail=f"Internal Error, id={id} is not unique, contact administrator")
            # result = records
            # result = records[0]
        else:
            # single record
            result = records[0]
        return result

    @classmethod
    def update(cls, data: Book):
        deleted = cls.delete(id=data.id)
        cls.create(data=data)
        return cls.read(id=data.id)

    @classmethod
    def delete(cls, id: int):
        deleted = cls.read(id=id)
        query = f'DELETE FROM book WHERE id = {id};'
        engine.execute(query)
        return deleted

    @classmethod
    def list(cls):
        query = f'SELECT * FROM book;'
        df = pd.read_sql(query, engine)
        result = df.to_dict('records')
        return result


# create
@app.post("/book")
def create(book: Book):
    return Book.create(data=book)


# read
@app.get("/book/{id}")
def read(id: int):
    return Book.read(id)


# update
@app.put("/book/{id}")
def update(id: int, book: Book):
    return Book.update(book)


#delete
@app.delete("/book/{id}")
def delete(id: int):
    return Book.delete(id=id)


# list
@app.get("/list")
def list():
    return Book.list()
