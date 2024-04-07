from app.db.session import get_client

from fastapi import APIRouter, Depends, HTTPException,responses,Query
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.db.models import StudentsIn,Detail,StudentOut,student_data,cursor_to_dict
from app.db.models import studententity
from fastapi import Path
router = APIRouter()



@router.post("/students",response_model=Detail,status_code=201,
             responses={201: {"description": "A JSON response sending back the ID of the newly created student record."}})
async def create_student(student: StudentsIn,client=Depends(get_client)):
    """
    API to create a student in the system. All fields are mandatory and required while creating the student in the system.


    """
    try:
        db=client.get_database('LMS')
        collection=db.get_collection('Students')
        student=await collection.insert_one(jsonable_encoder(student))
        print(type(student.inserted_id))

        return {'id':str(student.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Unable to create student: {e}")
    




@router.get("/students",
            responses={200: {"description": "sample response"}},
            
           
            response_model=StudentOut)   
async def list_students(
    country:str=Query(default=None,description="To apply filter of country. If not given or empty, this filter should be applied."),
    age:int=Query(default=None,description="Only records which have age greater than equal to the provided age should be present in the result. If not given or empty, this filter should be applied."),
    client=Depends(get_client)):
    """
    An API to find a list of students. You can apply filters on this API by passing the query parameters as listed below.
    """
    try:
        if country and age:
            db = client.get_database('LMS')
            collection = db.get_collection('Students')
            student = collection.find({'address.country': country, 'age': {'$gte': age}})
            students = await cursor_to_dict(student)
            return {'data': students}
        if country:
            db=client.get_database('LMS')
            collection=db.get_collection('Students')
            student=collection.find({'address.country':country})
            students=await cursor_to_dict(student)
            
            return {'data':students}
        if age:
            db=client.get_database('LMS')
            collection=db.get_collection('Students')
            student=collection.find({'age':{'$gte':age}})
            students=await cursor_to_dict(student)
            return {'data':students}
        
        db=client.get_database('LMS')
        collection=db.get_collection('Students')
        student=collection.find()
        students=await cursor_to_dict(student)  
        
        return {'data':students}

    
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Unable to fetch student: {e}")
    








@router.get("/students/{id}",
            responses={200: {"description": "sample response"},
                        404: {"description": "Student not found","content": {"application/json": {"example": {"detail": "Unable to fetch Student: Student not found"}}}}
                       
                       
                       },
            response_model=StudentsIn)
async def fetch_student(id:str=Path(description="The ID of the student previously created."),client:AsyncIOMotorClient=Depends(get_client)):
    """
    An API to get a student. You can get a student by passing the student id in the request URL.
    """
    try:
        db=client.get_database('LMS')
        collection=db.get_collection('Students')
        student = await collection.find_one({'_id': ObjectId(id)})
    
        if student:
            return student_data(student)
        
        else:
            raise HTTPException(status_code=404,detail="Student not found")

        
    except Exception as e:
        sc=500
        if isinstance(e,HTTPException):
            sc=e.status_code
            detail=e.detail

        raise HTTPException(status_code=sc,detail=f"Unable to fetch Student: {detail}")




from app.db.models import StudentUpdate 

@router.patch("/students/{id}",responses={204: {"description": "No Content","content": {"application/json": {"example": {}}}}},status_code=204)
async def update_student(id:str,student: StudentUpdate,client:AsyncIOMotorClient=Depends(get_client)):
    """
    API to update the student's properties based on information provided. Not mandatory that all information would be sent in PATCH, only what fields are sent should be updated in the Database.
    """
    try:
        collection = client.get_database('LMS').get_collection('Students')
        update_result = await collection.update_one({'_id': ObjectId(id)}, {'$set': student.model_dump(exclude_unset=True)})

        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {}
    except Exception as e:
        sc=500
        if isinstance(e,HTTPException):
            sc=e.status_code
            detail=e.detail
        raise HTTPException(status_code=sc,detail=f"Unable to update student: {detail}")








@router.delete("/students/{id}",responses={200: {"description": "sample response","content": {"application/json": {"example": {}}}}},status_code=200,)
async def delete_student(id:str,client=Depends(get_client)):
    """
    An API to delete a student. You can delete a student by passing the student id in the request URL.
    """
    try:
        db=client.get_database('LMS')
        collection=db.get_collection('Students')
        student=collection.delete_one({'_id':ObjectId(id)})
        # print(student.)
        if not student:
            raise HTTPException(status_code=404,detail="Student not found")
        
        
        return {"message":"Student deleted successfully"}
    except Exception as e:
        sc=500
        if isinstance(e,HTTPException):
            sc=e.status_code
            detail=e.detail
        raise HTTPException(status_code=sc,detail=f"Unable to delete student: {detail}")

    
    