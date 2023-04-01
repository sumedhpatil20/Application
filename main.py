from typing import  Any

from fastapi import Depends,Body, FastAPI, Path, Query
from pydantic import BaseModel, Field

import json
import mysql.connector

app = FastAPI()




@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_db():
   db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="test1234",
    database='student'
    )

   try:
      yield db
   finally:
      db.close()

class Student(BaseModel):
    name: str = Field(
        title="The name of student"
    )
    id: int  = Field(
        title="The roll number of student"
    )
    standard: int = Field(gt=0, description="The grade of student")


@app.put("/items/update/{item_id}")
def update_item(item_id: int, item: Any,db: Any= Depends(get_db)):
    print(item.name)
    cur = db.cursor()
    str1 = f""" update student set id = {item.id}, name = '{item.name}', standard = {item.standard} where id = {item_id}"""
    cur.execute(str1)
    reslt = (cur.fetchall())
    cur.execute("commit;")
    jsonstr = json.dumps(reslt)
    return jsonstr

@app.post("/items/add/")
def add_student(item: Any, db: Any= Depends(get_db)):

    cur = db.cursor()

    str1 = f""" insert into student  (select {item.id} as id, '{item.name}' as name,{item.standard} as standard)"""
    cur.execute(str1)
    print(cur.fetchall())
    cur.execute("commit;")

    str1 = f"""select * from student where id = {item.id}"""
    cur.execute(str1)
    jsonstr = json.dumps(cur.fetchall())

    return jsonstr

@app.get("/items/{item_id}")
def get_student(item_id: int,db: Any= Depends(get_db)):
    cur = db.cursor()

    str1 = f"""select * from student where id = {item_id}"""
    cur.execute(str1)

    jsonstr = json.dumps(cur.fetchall())
    return jsonstr

@app.get("/items/")
def get_student():
    str1 = f"""select * from student"""

    mydb = mysql.connector.connect(
    host="mysql",
    user="root",
    password="test1234",
    database='student'
    )

    cursorObject = mydb.cursor()
    cursorObject.autocommit =True

    cursorObject.execute(str1)
    jsonstr = json.dumps(cursorObject.fetchall())
    return jsonstr

@app.delete("/items/delete/{item_id}")
def delete_student(item_id: int,db: Any= Depends(get_db)):
    cur = db.cursor()

    str1 = f"""delete from student where id = {item_id}"""
    cur.execute(str1)
    reslt = cur.fetchall()

    cur.execute("commit;")
    jsonstr = json.dumps(reslt)
    return jsonstr