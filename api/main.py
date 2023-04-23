import pandas as pd
from sqlalchemy import create_engine
from fastapi import FastAPI, HTTPException

app = FastAPI()
connection_string = 'sqlite:///example.db'
engine = create_engine(connection_string)


# get all products
@app.get("/products")
async def read_item():
    query = f'SELECT * FROM products'
    df = pd.read_sql(query, engine)
    result = df.to_dict('records')
    return result


# get product by id
@app.get("/products/{product_id}")
async def read_item(product_id: int):
    query = f'SELECT * FROM products WHERE product_id = {product_id}'
    df = pd.read_sql(query, engine)
    records = df.to_dict('records')
    if len(records) == 0:
        # no matches - raise 404 - not found
        raise HTTPException(status_code=404, detail="Product not found")
    elif len(records) < 1:
        # multiple records, raise 500 - internal error - contact administrator
        raise HTTPException(status_code=500, detail=f"Internal Error - product_id={product_id} is not unique, contact administrator")
    else:
        # single record
        result = records[0]

    return result

