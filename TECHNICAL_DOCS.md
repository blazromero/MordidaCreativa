# Documentación Técnica

## Arquitectura del Sistema

### Backend (FastAPI)

#### Estructura de Archivos
- `main.py`: Endpoints y lógica principal de la API
- `models.py`: Modelos SQLAlchemy y Pydantic
- `database.py`: Configuración de la base de datos
- `auth.py`: Lógica de autenticación y JWT

#### Sistema de Autenticación
```python
# Configuración JWT
SECRET_KEY = "xuhac-tifet-nyfob-busob-gopam-beden-meraz-mebul-vaxax"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Flujo de autenticación
1. Usuario envía credenciales
2. Backend verifica y genera JWT
3. Frontend almacena token
4. Token se usa en cabeceras Authorization
```

#### Modelos de Base de Datos

##### Relaciones
```python
# Tabla de asociación para likes
recipe_likes = Table(
    'recipe_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id'))
)

# Relaciones en User
recipes: relationship("Recipes", back_populates="user")
liked_recipes: relationship("Recipes", secondary=recipe_likes)

# Relaciones en Recipes
user: relationship("User", back_populates="recipes")
liked_by: relationship("User", secondary=recipe_likes)
images: relationship("RecipeImage", back_populates="recipe")
```

#### Validaciones
```python
class RecipesCreate(BaseModel):
    title: str
    description: constr(max_length=140)
    ingredients: str
    instructions: constr(max_length=1400)
    category: Optional[str]
    
    @validator('title')
    def validate_title(cls, value):
        if len(value) < 3:
            raise ValueError('Título muy corto')
        return value.title()
```

### Frontend (React)

#### Componentes Principales

##### RecipeDetailCard
```javascript
// Estados
const [likes, setLikes] = useState(recipe.likes || 0);
const [likedByCurrentUser, setLikedByCurrentUser] = useState(recipe.liked_by_current_user);

// Manejo de likes
const handleLike = async () => {
    const token = localStorage.getItem('token');
    const res = await fetch(`/recipes/${recipe.id}/like`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    setLikes(data.likes);
    setLikedByCurrentUser(data.liked_by_current_user);
};
```

#### Gestión de Estado
- Token JWT almacenado en localStorage
- Estados locales para UI
- Props para pasar datos entre componentes

#### Rutas
```javascript
<Routes>
    <Route path="/" element={<Home />} />
    <Route path="/recetas/:id" element={<RecipeDetail />} />
    <Route path="/perfil/:id" element={<Perfil />} />
    <Route path="/crear" element={<CreateRecipe />} />
</Routes>
```

## Flujos de Datos

### Crear Receta
1. Usuario completa formulario
2. Frontend valida datos
3. Envía POST a /recipes/
4. Backend valida con Pydantic
5. Crea registro en base de datos
6. Devuelve receta creada

### Sistema de Likes
1. Usuario hace clic en like
2. Frontend envía POST con token
3. Backend verifica autenticación
4. Actualiza relaciones en base de datos
5. Actualiza contador de likes
6. Devuelve nuevo estado
7. Frontend actualiza UI

## Seguridad

### JWT
```python
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
```

### Protección de Rutas
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
```

## Base de Datos

### Esquema
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    email VARCHAR UNIQUE,
    hashed_password VARCHAR,
    profile_image VARCHAR
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(40),
    description VARCHAR(140),
    ingredients VARCHAR(50),
    instructions TEXT,
    user_id INTEGER REFERENCES users,
    category VARCHAR(50),
    likes INTEGER DEFAULT 0
);

CREATE TABLE recipe_likes (
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes,
    PRIMARY KEY (user_id, recipe_id)
);
```

## Manejo de Errores

### Backend
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

### Frontend
```javascript
try {
    const response = await fetch(url);
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail);
    }
} catch (error) {
    console.error('Error:', error.message);
}
```

## Optimizaciones

### Backend
- Paginación en listados
- Caché de consultas frecuentes
- Índices en campos de búsqueda

### Frontend
- Lazy loading de imágenes
- Memorización de componentes
- Estados locales para UI

## Pruebas

### Backend
```python
def test_create_recipe():
    response = client.post(
        "/recipes/",
        json={
            "title": "Test Recipe",
            "description": "Test Description",
            "ingredients": "Test Ingredients",
            "instructions": "Test Instructions"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### Frontend
```javascript
test('renders recipe card', () => {
    render(<RecipeCard recipe={mockRecipe} />);
    expect(screen.getByText(mockRecipe.title)).toBeInTheDocument();
});
```

## Despliegue

### Backend
```bash
# Producción
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend
```bash
# Build
npm run build
# Servir con nginx
```

## Mantenimiento

### Tareas Periódicas
- Backup de base de datos
- Limpieza de archivos temporales
- Monitoreo de errores
- Actualización de dependencias

### Logs
- Errores de aplicación
- Accesos de usuarios
- Rendimiento del sistema
- Uso de recursos 