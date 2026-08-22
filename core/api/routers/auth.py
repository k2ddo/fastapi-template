from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...schemas.user import TokenSchema
from ..dependencies import SessionDep
from ..security import authenticate_user, create_access_token

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token', response_model=TokenSchema)
async def issue_token(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> TokenSchema:
    user = await authenticate_user(session, form.username, form.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return TokenSchema(access_token=create_access_token(user.id))
