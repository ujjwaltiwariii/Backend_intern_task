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

class AddressOptional(BaseModel):
    city: Optional[str]=None
    country: Optional[str]=None

class StudentUpdate(BaseModel):
    name: Optional[str]=None
    age: Optional[int]=None
    address: Optional[AddressOptional]=None

    class config:
        orm_mode = True
        exclude_unset = True



def student_data(data)->dict:
    return {
        'name':data['name'],
        'age':data['age'],
        'address':data['address']
    }
def flatten_address(student: StudentUpdate) -> dict:
    data = student.dict(exclude_unset=True)
    if 'address' in data:
        for key, value in data['address'].items():
            data[f'address.{key}'] = value
        del data['address']
    return data

async def cursor_to_dict(cursor):
    result = []
    async for doc in cursor:
        data = {
            'name': doc.get('name', ''),
            'age': doc.get('age', 0),
            'address': doc.get('address', {})
        }
        result.append(data)
    return result