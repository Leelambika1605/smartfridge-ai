from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.models.refrigerator import Refrigerator
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate, AuthResponse
from app.schemas.refrigerator import RefrigeratorCreate, RefrigeratorResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user account, creates their default virtual refrigerator,
    and returns their profile and JWT access token.
    """
    existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # Create new user
    new_user = User(
        email=user_in.email.lower(),
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Automatically provision user's default virtual refrigerator
    default_fridge = Refrigerator(
        name=f"{new_user.full_name or 'Home'}'s Smart Fridge",
        model="Virtual SmartFridge AI v1",
        location="Kitchen",
        target_temperature_celsius=3.5,
        current_temperature_celsius=3.5,
        user_id=new_user.id
    )
    db.add(default_fridge)
    db.commit()
    db.refresh(new_user)

    # Issue JWT token
    access_token = create_access_token(subject=new_user.id)

    return {
        "user": new_user,
        "token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=AuthResponse)
def login_user(login_in: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates user credentials and returns user profile and JWT access token.
    """
    user = db.query(User).filter(User.email == login_in.email.lower()).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated."
        )

    access_token = create_access_token(subject=user.id)

    return {
        "user": user,
        "token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Retrieves the profile and virtual refrigerators of the currently authenticated user."""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_current_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Updates profile attributes (name, password) for the authenticated user."""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.password is not None:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/refrigerators", response_model=List[RefrigeratorResponse])
def get_user_refrigerators(current_user: User = Depends(get_current_user)):
    """Returns all virtual refrigerators owned by the current user."""
    return current_user.refrigerators


@router.post("/refrigerators", response_model=RefrigeratorResponse, status_code=status.HTTP_201_CREATED)
def create_virtual_refrigerator(
    fridge_in: RefrigeratorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates an additional virtual refrigerator for the current user."""
    new_fridge = Refrigerator(
        name=fridge_in.name,
        model=fridge_in.model or "Virtual SmartFridge AI v1",
        location=fridge_in.location or "Kitchen",
        target_temperature_celsius=fridge_in.target_temperature_celsius,
        current_temperature_celsius=fridge_in.current_temperature_celsius or 3.5,
        user_id=current_user.id
    )
    db.add(new_fridge)
    db.commit()
    db.refresh(new_fridge)
    return new_fridge
