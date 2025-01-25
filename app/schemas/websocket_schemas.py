from pydantic import BaseModel



class WSout(BaseModel):
    username: str
    message: str
    created_at: str

