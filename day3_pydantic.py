from  pydantic import BaseModel,Field,ValidationError #yeh jo haai ek important tempate hai pehle hamne jo hi gasemodel karka apne class ki smart banayenge then ham field ka istemal karke specifiv security lagane ke liye use karenge names par and numbers par validation error  hame error se bachata hai 
class AIUserResponse(BaseModel):
    name :str#  hamne ph se bol diya hai ki namme string me hi hogi
    
    
    age : int=Field(gt=18)# interger 18 se greater hona chahiye
    
    skills:list[str] #isme ek list honi chahiyye
try:
    print("test1: sahi data jach rahe hai....")
    good_data = {"name":"harsh gupta","age":19,"skills":["python","fastapi","asyncgroq"]
                 
    }
    
    validated_user = AIUserResponse(**good_data)
    print("data bilkul perfect hai")
    print(validated_user.model_dump()) # akhi ye kya hai model_dump().
    
except ValidationError as e:
    print("error aya:",e )   
    
    
print("\n-----------------------")


try:
    print("test2 : galat data bhejkar pahre dar ko check kar rahe hai") 
    bad_data =  { 'name':'Rahul' ,
                 'age':15,'skills':'python'
    }
    validated_user = AIUserResponse(**bad_data)
    
except ValidationError as e :
    print("pydantic gatekepper ne data ki pakad liya hai...........")
    print(e)
    