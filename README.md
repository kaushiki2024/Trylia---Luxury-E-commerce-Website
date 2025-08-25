# Trylia---Luxury-E-commerce-Website

A premium, modern e-commerce website for luxury products, built with **Next.js**, **TypeScript**, and **Tailwind CSS**.  
Focused on **elegance**, **performance**, and **seamless shopping experience**.

---

## 🚧 Project Status
**Currently under development** – features and UI will be added progressively.  
Follow the repo for updates.

---

## ✨ Planned Features
- 🛒 **Shopping Cart** with persistent state
- 💳 **Secure Checkout** with payment gateway integration
- 🔍 **Advanced Product Filters & Search**
- 🖼️ **High-Resolution Product Gallery**
- 🌐 **Multi-Currency Support**
- 📱 **Fully Responsive Design**
- ⚡ **Optimized with Next.js App Router**

---

## 🛠️ Tech Stack
- **Framework**: [Next.js 14+](https://nextjs.org/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **State Management**: React Context API
- **Data**: JSON + API-ready backend integration

---

## 📂 Project Structure
*(Work in progress — will expand as features are added)*

---

## Backend API (FastAPI + PostgreSQL)

This repo includes a FastAPI backend for "Trylia: Your Virtual Dressing Room".

### Prerequisites
- Python 3.11+
- PostgreSQL 14+

### Setup
1. Copy environment template:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your DB credentials and JWT secret.
3. Install dependencies:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Create the database (example):
   ```bash
   createdb trylia
   ```
5. Run migrations:
   ```bash
   PYTHONPATH=. alembic upgrade head
   ```
6. Start the server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### API Summary
- Auth: `POST /auth/signup`, `POST /auth/login`
- Users: `GET /users/me`
- Photos: `POST /photos`, `GET /photos`
- Outfits: `POST /outfits`, `GET /outfits`, `GET /outfits/{id}`, `PATCH /outfits/{id}`, `DELETE /outfits/{id}`
- Sessions: `POST /sessions`, `GET /sessions`
- Recommendations: `POST /recommendations`, `GET /recommendations`
- 3D Models: `POST /outfits/{id}/upload-3d` (multipart file), `GET /outfits/{id}/3d-model`

### 3D Model Notes
- Accepted formats: `glb`, `gltf`, `fbx`.
- Files are stored under `static/3d/` by default and served at `/static/3d/...`.
- To use a CDN or object storage, set `MEDIA_BASE_URL` in `.env`; returned `file_url` will use that base.
- CORS is enabled by default for frontend access.

