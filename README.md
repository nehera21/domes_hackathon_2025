# Domes Hackathon 2025 - Fullstack ML Project Template

A modern fullstack application template for ML hackathon projects, featuring a React TypeScript frontend, FastAPI Python backend, and PostgreSQL database.

## 🏗️ Tech Stack

### Frontend
- **React** with **TypeScript**
- **Vite** for fast development and building
- **React Router** for client-side routing
- **Axios** for API communication
- Modern, responsive CSS

### Backend
- **FastAPI** for high-performance async API
- **Python 3.11+**
- **asyncpg** for async PostgreSQL operations
- **Pydantic** for data validation and settings management
- **uvicorn** as ASGI server
- **uv** for fast Python package management

### Database
- **PostgreSQL** (connection setup, ready to use)

## 📁 Project Structure

```
domes_hackathon_2025/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── settings.py          # Configuration management
│   ├── databridge.py        # Database connection layer
│   ├── models/              # Domain and request/response models
│   │   ├── user.py
│   │   └── project.py
│   ├── services/            # Business logic layer
│   │   ├── user_service.py
│   │   └── project_service.py
│   ├── routers/             # API route handlers
│   │   ├── users.py
│   │   └── projects.py
│   ├── pyproject.toml       # Python dependencies (uv)
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx         # Application entry point
│   │   ├── App.tsx          # Main app with routing
│   │   ├── models/          # TypeScript type definitions
│   │   │   ├── user.ts
│   │   │   └── project.ts
│   │   ├── services/        # API client
│   │   │   └── api.ts
│   │   ├── components/      # React components
│   │   │   ├── UserList.tsx
│   │   │   └── ProjectList.tsx
│   │   └── pages/           # Page components
│   │       ├── HomePage.tsx
│   │       ├── UsersPage.tsx
│   │       └── ProjectsPage.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example         # Environment variables template
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **npm**
- **PostgreSQL** (optional for now - mock data is used)
- **uv** - Fast Python package manager ([installation instructions](https://github.com/astral-sh/uv))

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Install dependencies using uv:
```bash
uv sync
```

4. Run the backend server:
```bash
uv run python -m backend.main
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Install dependencies:
```bash
npm install
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📊 API Endpoints

### Users
- `GET /api/v1/users` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `POST /api/v1/users` - Create a new user
- `PUT /api/v1/users/{id}` - Update a user
- `DELETE /api/v1/users/{id}` - Delete a user

### Projects
- `GET /api/v1/projects` - Get all projects
- `GET /api/v1/projects?owner_id={id}` - Get projects by owner
- `GET /api/v1/projects/{id}` - Get project by ID
- `POST /api/v1/projects` - Create a new project
- `PUT /api/v1/projects/{id}` - Update a project
- `DELETE /api/v1/projects/{id}` - Delete a project

## 🗄️ Database Setup (Optional)

The template currently uses mock data, but the database connection is ready to use.

### Setting up PostgreSQL

1. Install PostgreSQL if you haven't already

2. Create the database:
```bash
createdb hackathon_db
```

3. Update the `.env` file in the backend directory with your database credentials

4. Uncomment the database queries in the service files (`backend/services/*.py`)

### Creating Tables

Example SQL schema for users and projects:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Development

### Backend Development

The backend uses FastAPI's automatic reload in debug mode. Any changes to Python files will automatically restart the server.

### Frontend Development

Vite provides hot module replacement (HMR), so changes will be reflected instantly in the browser.

### Code Quality

Backend:
```bash
cd backend
uv run black .        # Format code
uv run ruff check .   # Lint code
```

Frontend:
```bash
cd frontend
npm run lint          # Lint TypeScript/React code
```

## 📦 Building for Production

### Backend

```bash
cd backend
uv build
```

### Frontend

```bash
cd frontend
npm run build
```

The production build will be in the `frontend/dist` directory.

## 🤝 Contributing

This is a hackathon template - feel free to modify and extend it for your specific needs!

### Adding New Features

1. **New Domain/Entity:**
   - Create model in `backend/models/`
   - Create service in `backend/services/`
   - Create router in `backend/routers/`
   - Register router in `backend/main.py`
   - Create TypeScript types in `frontend/src/models/`
   - Add API methods in `frontend/src/services/api.ts`
   - Create components/pages as needed

2. **Database Schema Changes:**
   - Update SQL schema
   - Modify models and services accordingly

## 📝 License

MIT License - feel free to use this template for your hackathon projects!

## 🎯 Next Steps

- [ ] Connect to actual PostgreSQL database
- [ ] Add authentication/authorization
- [ ] Implement ML model integration
- [ ] Add data visualization components
- [ ] Set up Docker for easy deployment
- [ ] Add tests (pytest for backend, Vitest for frontend)
- [ ] Set up CI/CD pipeline

---

Happy hacking! 🚀