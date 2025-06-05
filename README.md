# Aplicación de Recetas

Esta es una aplicación web fullstack para compartir y gestionar recetas de cocina. Permite a los usuarios crear, ver y dar like a recetas, así como gestionar sus propias recetas.

## Estructura del Proyecto

```
BudgetAPI/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py          # Endpoints de la API
│       ├── models.py        # Modelos de la base de datos
│       ├── database.py      # Configuración de la base de datos
│       ├── auth.py         # Autenticación y seguridad
│       └── static/         # Archivos estáticos
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/     # Componentes React
│       ├── pages/         # Páginas de la aplicación
│       └── App.js         # Componente principal
└── README.md
```

## Características Principales

### Sistema de Autenticación
- Registro de usuarios
- Inicio de sesión con JWT
- Protección de rutas privadas
- Gestión de sesiones

### Gestión de Recetas
- Crear nuevas recetas
- Ver listado de recetas
- Filtrar por categorías
- Ver detalles de recetas
- Eliminar recetas propias

### Sistema de Likes
- Dar/quitar likes a recetas
- Contador de likes por receta
- Estado visual de likes
- Persistencia de likes

### Perfiles de Usuario
- Ver perfil propio
- Ver perfiles de otros usuarios
- Ver recetas por usuario

## Tecnologías Utilizadas

### Backend
- FastAPI (Framework Python)
- SQLAlchemy (ORM)
- PostgreSQL (Base de datos)
- JWT (Autenticación)
- Pydantic (Validación de datos)

### Frontend
- React
- React Router
- Fetch API
- CSS moderno

## API Endpoints

### Autenticación
- `POST /login` - Iniciar sesión
- `POST /users/` - Registrar nuevo usuario
- `GET /users/me` - Obtener datos del usuario actual
- `DELETE /users/me` - Eliminar cuenta

### Recetas
- `GET /recipes/all` - Obtener todas las recetas
- `GET /recipes/{id}` - Obtener una receta específica
- `POST /recipes/` - Crear nueva receta
- `DELETE /recipes/{recipe_id}` - Eliminar receta
- `GET /recipes/search` - Buscar recetas
- `GET /recipes/` - Filtrar recetas por categoría

### Likes
- `POST /recipes/{recipe_id}/like` - Dar/quitar like a una receta

### Usuarios
- `GET /users/{id}` - Obtener datos de un usuario
- `GET /users/{id}/recipes` - Obtener recetas de un usuario

## Modelos de Datos

### Usuario (User)
```python
class User:
    id: int
    username: str
    email: str
    hashed_password: str
    profile_image: str
    recipes: List[Recipe]
    liked_recipes: List[Recipe]
```

### Receta (Recipe)
```python
class Recipe:
    id: int
    title: str
    description: str
    ingredients: str
    instructions: str
    user_id: int
    category: str
    likes: int
    images: List[RecipeImage]
    liked_by: List[User]
```

## Funcionalidades por Implementar
- Sistema de comentarios
- Categorías personalizadas
- Búsqueda avanzada
- Sistema de seguimiento entre usuarios
- Compartir recetas en redes sociales

## Configuración del Proyecto

### Backend
1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
SECRET_KEY=tu_clave_secreta
DATABASE_URL=postgresql://user:password@localhost/db_name
```

4. Iniciar servidor:
```bash
uvicorn app.main:app --reload
```

### Frontend
1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Iniciar servidor de desarrollo:
```bash
npm start
```

## Seguridad
- Autenticación mediante JWT
- Contraseñas hasheadas con bcrypt
- Protección CORS configurada
- Validación de datos con Pydantic
- Manejo seguro de sesiones

## Contribuir
1. Fork el repositorio
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

## Vista previa

![Pantalla principal](docs/Home.png)
![Formulario](docs/formulario.png)
![Perfil](docs/perfil.png)
![Registro](docs/Registro.png)

## 🎥 Demo en video

[![Demo de la app](https://img.youtube.com/vi/4495vgXfo84/0.jpg)](https://youtu.be/4495vgXfo84)

## Licencia
Este proyecto está bajo la Licencia MIT. 