from fastapi import APIRouter

router = APIRouter()


@router.post('admin/signup')
def adminAccountCreate():
    pass
