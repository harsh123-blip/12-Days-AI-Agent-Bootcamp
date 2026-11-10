from pydantic import BaseModel, Field
class UserAddress(BaseModel):
    city:str
    pincode:int=Field(gt=100000, lt=999999)
class UserProfile(BaseModel):
    name:str
    age:int = Field(gt = 18)
    address:UserAddress
    skill:list[str]
    
    
    # testing kkarte hai
    
user_data = {"name":"harsh gupta", "age": 19, "address":{"city":"lucknow","pincode":226001}, "skill":["python",'fastapi',"typing"]}
validated_data = UserProfile(**user_data)
print("nested schema validation successfully launch:",validated_data.model_dump()) 
        
