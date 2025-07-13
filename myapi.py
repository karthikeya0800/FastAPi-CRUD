from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1:{
        "name":"john",
        "age":"17",
        "year": "year 12"
    }
}

class Student(BaseModel):
    name:str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name:Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
def index():
    return {"name":"First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id:int = Path(..., description="The ID of the student you want to view",gt=0,lt=50)):
    return students[student_id]


#All the variables present in api endpoint are path paramenters remaining are query parameters.
#Example 'student_id is path paramenter, test and name are query parameters
#pythin dont allow optional inputs before mandatory inputs in a function. Hence, *
@app.get("/get-by-name/{student_id}")
def get_student(*,name:Optional[str] = None, test:int,student_id:int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data":"Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id:int, student : Student):
    if student_id in students:
        return {"Error":"Student exists"}
    
    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error":"Student does not exist"}
    
    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
            students[student_id].year = student.year
    
    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return {"Error":"Student does not exist"}
    
    del students[student_id]
    return {"Message":"Student deleted successfully"}