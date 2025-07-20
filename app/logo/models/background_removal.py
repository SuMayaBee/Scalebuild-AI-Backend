from pydantic import BaseModel

class RemoveBgRequest(BaseModel):
    image_url: str

class RemoveBgResponse(BaseModel):
    new_image_url: str
