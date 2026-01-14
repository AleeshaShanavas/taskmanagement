# Task Management Application

A Django-based task management system with role-based access control (SuperAdmin, Admin, User), JWT authentication for users, and a custom HTML admin panel for Admins and SuperAdmins.

## ✨ Features

### 🔐 Authentication
- **JWT Login** for regular users (`UserType.USER`) via `/api/auth/login/`
- **Session-based login** for Admin/SuperAdmin (custom admin panel)

### 👥 Roles & Permissions
| Role | Capabilities |
|------|-------------|
| **SuperAdmin** | Create/edit/delete users, assign users to admins, view all tasks & reports |
| **Admin** | Assign tasks to their users, view/manage their tasks, view completion reports |
| **User** | View assigned tasks, mark as completed with report & worked hours |

### 📡 API Endpoints (User-Facing)
- `POST /api/auth/login/` – Get JWT token (users only)
- `GET /api/tasks/` – List own tasks
- `PUT /api/tasks/{id}/` – Update task status (must submit report + hours when completed)
- `GET /api/tasks/{id}/report/` – View report (Admin/SuperAdmin only)

### 🖥️ Admin Panel (HTML Templates)
- Custom dashboard at `/api/auth/panel/login/`
- User management (SuperAdmin only)
- Task assignment (Admin only)
- Report viewing
- Secure logout

## 🛠️ Tech Stack
- Python 3.9+
- Django 4.2+
- Django REST Framework
- SimpleJWT
- SQLite (default)

## 🚀 Quick Start

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd taskmanagement