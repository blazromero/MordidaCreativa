from sqlalchemy import Column, Integer, String, ForeignKey, Float, text, Table
from sqlalchemy.orm import relationship, Mapped
from .database import Base
from pydantic import BaseModel, constr
from typing import Optional, List
from pydantic import validator

# Tabla de asociación para likes
recipe_likes = Table(
    'recipe_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile_image = Column(
        String,
        server_default=text("'http://localhost:8000/static/img_defecto.avif'"),
        nullable=False
    )

    recipes: Mapped[list["Recipes"]] = relationship("Recipes", back_populates="user")
    liked_recipes = relationship("Recipes", secondary=recipe_likes, back_populates="liked_by")


class Recipes(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(40), index=True)
    description = Column(String(15))
    ingredients = Column(String(50))
    instructions = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String(50), nullable=True)
    likes = Column(Integer, default=0)


    images: Mapped[list["RecipeImage"]] = relationship("RecipeImage", back_populates="recipe", cascade="all, delete")
    user: Mapped["User"] = relationship("User", back_populates="recipes")
    liked_by = relationship("User", secondary=recipe_likes, back_populates="liked_recipes")

    

class RecipeImage(Base):
    __tablename__ = "recipe_images"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    image_url = Column(String)

    recipe: Mapped["Recipes"] = relationship("Recipes", back_populates="images")


# ESQUEMAS DE VALIDACIÓN CON PYDANTIC

class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # El usuario envía la contraseña sin encriptar

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    profile_image: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    profile_image: Optional[str]

class RecipesCreate(BaseModel):
    title: str
    description: constr(max_length=140)
    ingredients: str
    instructions: constr(max_length=1400)
    category: Optional[str] = None
    
    @validator('title')
    def validate_title(cls, value):
        value = value.strip()
        if len(value) < 3:
            raise ValueError('El título debe tener al menos 3 caracteres')
        if len(value) > 40:  # Según la restricción en el modelo SQL
            raise ValueError('El título no puede exceder los 40 caracteres')
        return value.title()

    @validator('ingredients')
    def validate_ingredients(cls, value):
        if not value.strip():
            raise ValueError('La lista de ingredientes no puede estar vacía')
        if len(value) > 50:  # Según la restricción en el modelo SQL
            raise ValueError('La lista de ingredientes no puede exceder los 50 caracteres')
        return value.strip()

    @validator('category')
    def validate_category(cls, value):
        if value is None:
            return value
        valid_categories = ['Desayuno', 'Almuerzo', 'Cena', 'Postre', 'Snack']
        if value not in valid_categories:
            raise ValueError(f'Categoría debe ser una de: {", ".join(valid_categories)}')
        return value

class RecipeImageOut(BaseModel):
    id: int
    image_url: str

    class Config:
        orm_mode = True

class UserPublic(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class RecipesOut(BaseModel):
    id: int
    title: str
    description: str
    ingredients: str
    instructions: str
    user_id: int
    category: Optional[str]  # <--- Agregado
    images: list[RecipeImageOut] = []
    user: UserPublic
    likes: int
    liked_by_current_user: Optional[bool] = False

    class Config:
        orm_mode = True


