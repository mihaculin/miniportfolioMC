from pydantic import BaseModel, EmailStr


class UserInfoResponse(BaseModel):
    name: str
    email: str
    role: str
    skills: list[str]
    location: str
    bio: str
