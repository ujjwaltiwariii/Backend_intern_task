from pydantic import BaseModel
from typing import List, Optional


class Address(BaseModel):
    city: str
    country: str

class StudentsIn(BaseModel):
    name:str
    age:int
    address:Address
    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {
    #                 "name": "Ujjwal Tiwari",
    #                 "age": 20,
    #                 "address": {
    #                     "city": "Ghaziabad",
    #                     "country": "India"
    #                 }
                    
    #             }
    #         ]
    #     }
    # }
        


class Student(BaseModel):
    name: str
    age: int

class StudentOut(BaseModel):
    data: Optional[List[Student]]=None

class Detail(BaseModel):
    id:str

class StudentUpdate(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    address: Optional[Address]=None

    class config:
        orm_mode = True
        exclude_unset = True


def studententity_to_dict(data)->dict:
    return {
        'name':data['name'],
        'age':data['age'],
        'address':data['address']
    }

async def studententity(data):
    data=[]
    for student in data:
        data_dict=studententity_to_dict(student)
        print(student)
        data.append(data_dict)
    return data
    # for student in data:
        

