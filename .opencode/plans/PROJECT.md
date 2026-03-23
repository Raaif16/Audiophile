# Audiophile Headphones Ecommerce

## What This Is

A full-featured ecommerce platform for headphone enthusiasts (audiophiles) featuring a curated product catalog, user-generated reviews with verified purchase badges, wishlist functionality, and an admin panel for product and order management. Built with React frontend, FastAPI backend, and MongoDB.

## Core Value

Users can discover, research, and save headphones through authentic community reviews while browsing a curated catalog tailored for audiophile enthusiasts.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Product catalog with categories (over-ear, in-ear, open-back, etc.), filtering, and search
- [ ] User authentication with email/password (signup, login, logout, password reset)
- [ ] Product reviews with star ratings, written reviews, and photo uploads
- [ ] Verified purchase badge system for reviews
- [ ] User wishlist functionality
- [ ] Admin panel for product management (add/edit/delete products)
- [ ] Admin panel for order management (view orders, update status)
- [ ] Admin panel for review moderation
- [ ] Local file storage for product images
- [ ] Minimal/modern UI design

### Out of Scope

- **Payment processing** — Deferred to v2; focus on catalog and community features first
- **Social login** — Email/password sufficient for v1
- **Email service integration** — Skip for v1; can add transactional emails later
- **Cloud storage** — Using local file storage for product images
- **Mobile app** — Web-first approach
- **Real-time chat** — Not core to audiophile research experience

## Context

Building for personal use and learning. Target audience is headphone enthusiasts who value detailed specifications and authentic reviews. Community-driven approach means reviews and ratings are central to the experience.

## Constraints

- **Tech Stack**: React (frontend), FastAPI + MongoDB (backend), separate folder structure required
- **Storage**: Local filesystem for product images (not cloud)
- **Authentication**: Email/password only (no OAuth)
- **Email**: No email service integration in v1
- **Design**: Minimal/modern aesthetic preferred
- **Timeline**: Personal project — no hard deadline

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Separate BE/FE folders | Clear separation of concerns, enables independent deployment | — Pending |
| Local image storage | Simpler setup for v1, no cloud dependencies | — Pending |
| Skip payments in v1 | Focus on core catalog and community features first | — Pending |
| MongoDB for database | Flexible schema for product variations and reviews | — Pending |
| FastAPI for backend | Modern Python framework with great async support and auto-generated docs | — Pending |

---
*Last updated: 2025-03-23 after initialization*
