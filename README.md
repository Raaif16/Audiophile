# Audiophile Headphones Ecommerce

A curated platform for headphone enthusiasts to discover, research, and save headphones through authentic community reviews.

## Tech Stack

- **Frontend:** React + Vite + TypeScript
- **Backend:** FastAPI + Python + MongoDB
- **Storage:** Local filesystem for images

## Project Structure

```
.
├── backend/          # FastAPI backend
│   ├── app/         # Application code
│   │   ├── models/  # MongoDB/Beanie models
│   │   ├── routers/ # API route handlers
│   │   ├── services/# Business logic
│   │   └── schemas/ # Pydantic schemas
│   └── tests/       # Backend tests
├── frontend/        # React frontend (Vite)
└── README.md
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

### Frontend

(Coming in Plan 06 - Vite setup)

## Environment Variables

See `backend/.env.example` for required environment variables.

## Features

- Email/password authentication (JWT-based)
- Product catalog with detailed specifications
- Community reviews and ratings
- Wishlist functionality
- Product comparison
- Admin dashboard (Phase 5)
