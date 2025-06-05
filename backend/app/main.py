from fastapi import FastAPI, HTTPException, Depends, Path, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .models import User, UserCreate, RecipesCreate, UserOut, RecipesOut, Recipes, RecipeImage, RecipeImageOut
from .database import engine, Base, SessionLocal
from typing import List, Optional
from .auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, hash_password, get_current_user, get_current_user_optional
from datetime import timedelta
from fastapi import status
from fastapi.staticfiles import StaticFiles
from pathlib import Path as PathlibPath



app = FastAPI(title="Budget API")


BASE_DIR = PathlibPath(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent  

static_path = PROJECT_ROOT / "app" / "static"

app.mount("/static", StaticFiles(directory=static_path), name="static")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # donde corre tu frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def cargar_datos_de_prueba():
    db = SessionLocal()

    # Eliminar datos existentes
    db.query(Recipes).delete()
    db.query(User).delete()
    db.query(RecipeImage).delete()
    db.commit()

    # Crear usuarios
    users_data = [
        {"username": "alice", "email": "alice@example.com", "password": "alice123"},
        {"username": "bob", "email": "bob@example.com", "password": "bob123"},
        {"username": "charlie", "email": "charlie@example.com", "password": "charlie123"},
        {"username": "diana", "email": "diana@example.com", "password": "diana123"},
        {"username": "edward", "email": "edward@example.com", "password": "edward123"},
        {"username": "fiona", "email": "fiona@example.com", "password": "fiona123"},
        {"username": "george", "email": "george@example.com", "password": "george123"},
        {"username": "hannah", "email": "hannah@example.com", "password": "hannah123"},
        {"username": "ian", "email": "ian@example.com", "password": "ian123"},
        {"username": "julia", "email": "julia@example.com", "password": "julia123"},
    ]

    users = []
    for data in users_data:
        hashed = hash_password(data["password"])
        user = User(username=data["username"], email=data["email"], hashed_password=hashed)
        db.add(user)
        users.append(user)
    db.commit()

    # Crear recetas (asociadas a los usuarios creados)
    recipes_data = [
    {
        "title": "Tarta de espinaca",
        "description": "Tarta rica y saludable, ideal para cualquier comida.",
        "ingredients": "espinaca, huevo, queso",
        "instructions": "Lavar y cocinar la espinaca.\nBatir los huevos y mezclarlos con el queso.\nAgregar la espinaca cocida a la mezcla.\nColocar en una masa y hornear 40 minutos.",
        "category": "Saludable"
    },
    {
        "title": "Galletitas de avena",
        "description": "Perfectas para el desayuno o merienda dulce.",
        "ingredients": "avena, banana, miel",
        "instructions": "Pisar la banana.\nMezclar con avena y miel.\nFormar bolitas.\nHornear 20 minutos.",
        "category": "Desayuno"
    },
    {
        "title": "Sopa de lentejas",
        "description": "Ideal para el invierno, reconfortante y nutritiva.",
        "ingredients": "lentejas, zanahoria, cebolla",
        "instructions": "Cortar la zanahoria y cebolla.\nRehogar en una olla.\nAgregar lentejas y agua.\nHervir 45 minutos.",
        "category": "Salado"
    },
    {
        "title": "Pizza casera",
        "description": "Clásico de domingo, casera y deliciosa.",
        "ingredients": "harina, levadura, tomate, queso",
        "instructions": "Amasar la harina con levadura y agua.\nDejar levar 1 hora.\nEstirar la masa y agregar salsa de tomate.\nAgregar queso.\nHornear 30 minutos.",
        "category": "Salado"
    },
    {
        "title": "Ensalada de quinoa",
        "description": "Fresca y rápida, ideal para un almuerzo ligero.",
        "ingredients": "quinoa, tomate, pepino, limón",
        "instructions": "Hervir la quinoa 15 minutos.\nPicar el tomate y el pepino.\nMezclar todo con jugo de limón.\nServir fría.",
        "category": "Saludable"
    },
    {
        "title": "Brownies",
        "description": "Postre chocolatoso para los más golosos.",
        "ingredients": "chocolate, azúcar, huevos, harina",
        "instructions": "Derretir el chocolate.\nBatir los huevos con azúcar.\nMezclar todo con la harina.\nHornear 25 minutos.",
        "category": "Dulce"
    },
    {
        "title": "Tortilla de papas",
        "description": "Clásico español para cualquier momento.",
        "ingredients": "papa, huevo, cebolla",
        "instructions": "Cortar y freír las papas.\nBatir los huevos.\nMezclar con cebolla y papas.\nCocinar en sartén.",
        "category": "Salado"
    },
    {
        "title": "Wok de verduras",
        "description": "Rápido y sano para una comida ligera.",
        "ingredients": "zanahoria, brócoli, salsa soja",
        "instructions": "Cortar las verduras.\nSaltear en sartén caliente con salsa de soja.\nServir caliente.",
        "category": "Saludable"
    },
    {
        "title": "Empanadas",
        "description": "Ideales para compartir en reuniones.",
        "ingredients": "carne, cebolla, masa",
        "instructions": "Cocinar la carne con cebolla.\nRellenar las tapas de empanadas.\nCerrar y hornear 20 minutos.",
        "category": "Salado"
    },
    {
        "title": "Pan de banana",
        "description": "Aprovechar bananas maduras en un pan dulce.",
        "ingredients": "banana, harina, huevo",
        "instructions": "Pisar las bananas.\nMezclar con huevo y harina.\nColocar en molde.\nHornear 40 minutos.",
        "category": "Dulce"
    },
    {
        "title": "Arroz con leche",
        "description": "Postre tradicional, cremoso y delicioso.",
        "ingredients": "arroz, leche, azúcar, canela",
        "instructions": "Hervir el arroz con leche.\nAgregar azúcar y canela.\nCocinar 40 minutos hasta espesar.",
        "category": "Dulce"
    },
    {
        "title": "Berenjenas al escabeche",
        "description": "Para picadas y entradas frescas.",
        "ingredients": "berenjena, vinagre, ajo",
        "instructions": "Cortar y hervir las berenjenas.\nPreparar mezcla con vinagre y ajo.\nMacerar todo en frasco.",
        "category": "Salado"
    },
    {
        "title": "Fideos con salsa",
        "description": "Rápido y rendidor para cualquier día.",
        "ingredients": "fideos, tomate, ajo",
        "instructions": "Hervir los fideos.\nPreparar salsa con tomate y ajo.\nMezclar todo y servir.",
        "category": "Salado"
    },
    {
        "title": "Milanesas de soja",
        "description": "Opción vegetariana y nutritiva.",
        "ingredients": "soja texturizada, pan rallado",
        "instructions": "Hidratar la soja.\nFormar medallones.\nRebozar y hornear 25 minutos.",
        "category": "Salado"
    },
    {
        "title": "Tarta de zapallitos",
        "description": "Tarta liviana y sabrosa para cualquier momento.",
        "ingredients": "zapallitos, cebolla, huevo",
        "instructions": "Saltear zapallitos y cebolla.\nBatir huevos.\nMezclar todo y volcar en masa.\nHornear 40 minutos.",
        "category": "Salado"
    },
]

    for i, data in enumerate(recipes_data):
        user = users[i % len(users)]
        recipe = Recipes(**data, user_id=user.id)
        db.add(recipe)

    db.commit()

    recipes_image =[
        {"recipe_id": 1, "image_url": "https://images.unsplash.com/photo-1733154507491-df341f482669?q=80&w=2116&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 2, "image_url": "https://images.unsplash.com/photo-1645258751218-1a1ddb1630dc?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 3, "image_url": "https://images.unsplash.com/photo-1552298013-de2af4b94854?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 4, "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 5, "image_url": "https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 6, "image_url": "https://images.unsplash.com/photo-1629856428041-6f9721807b05?q=80&w=1971&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 7, "image_url": "https://images.unsplash.com/photo-1639669794539-952631b44515?q=80&w=2121&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 8, "image_url": "https://plus.unsplash.com/premium_photo-1664478238082-3df93e48c491?q=80&w=2080&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 9, "image_url": "https://images.unsplash.com/photo-1646314230198-e27c375e1a2a?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 10, "image_url": "https://images.unsplash.com/photo-1632931057819-4eefffa8e007?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 11, "image_url": "https://images.unsplash.com/photo-1590055619273-44b5b6ce52e8?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 12, "image_url": "https://images.unsplash.com/photo-1602141901597-dd9e5e5ae5b4?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 13, "image_url": "https://images.unsplash.com/photo-1612929633738-8fe44f7ec841?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 14, "image_url": "https://plus.unsplash.com/premium_photo-1664472757995-3260cd26e477?q=80&w=1961&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"},
        {"recipe_id": 15, "image_url": "https://media.istockphoto.com/id/497616623/es/foto/quiche-de-vegetarianas.webp?a=1&b=1&s=612x612&w=0&k=20&c=u0UvEgrTAvsgBkeBU9OPEcwg0-rNVsb46nzkLsqpkGg="}
    ]
    for data in recipes_image:
        i = 1
        image = RecipeImage(recipe_id=data["recipe_id"], image_url=data["image_url"])
        db.add(image)
        print()
        i += 1
    db.commit()
    db.close()


# Llamar a la función
cargar_datos_de_prueba()

@app.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/recipes/search", response_model=List[RecipesOut])
def search_recipes(q: str, db: Session = Depends(get_db)):
    return db.query(Recipes).filter(
        Recipes.title.ilike(f"%{q}%") | Recipes.ingredients.ilike(f"%{q}%")
    ).all()

@app.get("/recipes/all", response_model=List[RecipesOut])
def get_all_recipes(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    recipes = db.query(Recipes).all()
    if current_user:
        for recipe in recipes:
            recipe.liked_by_current_user = current_user in recipe.liked_by
    return recipes

@app.get("/recipes/{id}", response_model=RecipesOut)
def get_recipe_by_id(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    recipe = db.query(Recipes).filter(Recipes.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    if current_user:
        recipe.liked_by_current_user = current_user in recipe.liked_by
    return recipe

@app.get("/recipes/images", response_model=List[RecipeImageOut])
def get_all_recipes_image(db: Session = Depends(get_db)):
    return db.query(RecipeImage).all()

@app.get("/recipes/", response_model=List[RecipesOut])
def get_recipes_by_category(
    category: Optional[str] = Query(None, description="Filtrar recetas por categoría"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Recipes)
    if category:
        query = query.filter(Recipes.category == category.title())
    recipes = query.all()
    if current_user:
        for recipe in recipes:
            recipe.liked_by_current_user = current_user in recipe.liked_by
    return recipes

@app.get("/users/{id}", response_model=UserOut)
def get_data_user(id: int = Path(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.get("/users/{id}/recipes", response_model=List[RecipesOut])
def get_recipes_user(id: int = Path(...), db: Session = Depends(get_db)):
    return db.query(Recipes).filter(Recipes.user_id == id).all()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id  # Agregamos el ID del usuario en la respuesta
    }

@app.get("/users/me", response_model=UserOut)
def get_user_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    return db.query(User).filter(User.id == current_user.id).first()


@app.post("/users/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/recipes/", response_model=RecipesOut)
async def create_recipe(
    recipe: RecipesCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    try:
        # Crear la receta con los datos validados
        db_recipe = Recipes(
            title=recipe.title,
            description=recipe.description,
            ingredients=recipe.ingredients,
            instructions=recipe.instructions,
            category=recipe.category,
            user_id=current_user.id,
            likes=0  # Inicializar likes en 0
        )
        
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la receta: {str(e)}"
        )

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int = Path(..., gt=0), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = db.query(Recipes).filter(Recipes.id == recipe_id, Recipes.user_id == current_user.id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada o no te pertenece.")
    db.delete(recipe)
    db.commit()
    return {"detail": "Receta eliminada correctamente"}


@app.delete("/users/me", status_code=204)
def delete_current_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return

@app.post("/recipes/{recipe_id}/like")
def like_recipe(recipe_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    recipe = db.query(Recipes).filter(Recipes.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    # Obtener el usuario actual de la misma sesión
    user = db.query(User).filter(User.id == current_user.id).first()

    # Verificar si el usuario ya dio like
    if user in recipe.liked_by:
        # Si ya dio like, lo quitamos
        recipe.liked_by.remove(user)
        recipe.likes -= 1
        message = "Like removido"
    else:
        # Si no ha dado like, lo agregamos
        recipe.liked_by.append(user)
        recipe.likes += 1
        message = "Like agregado"

    db.commit()
    db.refresh(recipe)

    return {"message": message, "likes": recipe.likes, "liked_by_current_user": user in recipe.liked_by}
