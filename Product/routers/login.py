from fastapi import APIRouter, Depends, status, HTTPException
from Product.database import engine, SessionLocal, get_database
from ..import schemas,database,models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

SECRET_KEY = "f5654643c6956bcd0ccca872cda68178f1231ba711eafcdd1af9d3f71b1d0761"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post('/login',response_model = None)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_database)):
    user = db.query(models.Login).filter(models.Login.username == request.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Username not found/ user is invalid')
    if not  pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail='Invalid Password')
    # Generate JWT Token
    access_token = generate_token(data= {'sub':user.username})
    return {"access_token": access_token, "token_type":"bearer"}

@router.post("/users/", response_model=schemas.Login)
def create_user(user: schemas.LoginCreate, db: Session = Depends(get_database)):
    db_user = db.query(models.Login).filter(models.Login.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    db_user = models.Login(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid auth credentials",
        headers = {'WWW-Authenticate':'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms =[ALGORITHM])
        username:str =  payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
