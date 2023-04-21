# TODO WIP

import pugsql
from fastapi import FastAPI, HTTPException, Depends
from starlette.responses import RedirectResponse

app = FastAPI()

queries = pugsql.module("path/to/sql/files")
queries.connect("sqlite:///db/database.sqlite3")


@app.get("/{slug}")
async def redirect_to_full_url(slug: str):
    url = queries.get_url(slug=slug)
    if url is None:
        raise HTTPException(status_code=404)
    return RedirectResponse(url)
