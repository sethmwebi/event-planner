from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from database.connection import Database
from models.user import User, UserSignIn

user_router = APIRouter(tags=["User"])
user_database = Database(User)
hash_password = HashPassword()

users = {}


@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided already exists",
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {"message": "User created successfully"}


@user_router.post("/signin")
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist.",
        )
    if user_exist.password == user.password:
        return {"message": "User signed in successfully."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid details passed."
    )
