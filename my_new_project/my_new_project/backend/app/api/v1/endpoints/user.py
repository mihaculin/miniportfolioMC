from fastapi import APIRouter
from app.schemas.user import UserInfoResponse

router = APIRouter()

_USER_INFO = UserInfoResponse(
    name="Mihaela Constantin",
    email="mihaela@example.com",
    role="Full Stack Developer",
    skills=["Python", "FastAPI", "React", "TypeScript", "PostgreSQL", "Docker"],
    location="Romania",
    bio="Passionate full stack developer with experience building modern web applications.",
)


@router.get("/user/info", response_model=UserInfoResponse, summary="Get User Info")
def get_user_info() -> UserInfoResponse:
    return _USER_INFO
