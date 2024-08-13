from fastapi import APIRouter

router = APIRouter()

@router.get("/infos")
def get_infos():
    return ""