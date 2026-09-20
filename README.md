# Catalog Store

Digital catalog with WhatsApp ordering, for small businesses.
A customer browses the products and is redirected to a pre-filled
WhatsApp conversation - no cart, no online payment.

## Tech stack

- **Backend**: Django 5.2 (LTS) + Django REST Framework, PostgreSQL in production (SQLite locally)
- **Frontend**: Vue 3 + Vite + Vue Router
- **Photos**: Cloudinary
- **Hosting**: Render (backend), Netlify (frontend), Neon (PostgreSQL database)

## Project structure
```
CatalogStore/
├── backend/
│ ├── config/ # Django settings (settings, root urls)
│ ├── catalog/ # Main App
│ │ ├── models.py # Store, Category, Product, ProductImage, ProductInquiry
│ │ ├── serializers.py # JSON serialization for the API
│ │ ├── views.py # Endpoint logic
│ │ ├── urls.py # API routes
│ │ ├── admin.py # Admin interface
│ │ └── management/commands/seed_catalog.py
│ ├── requirements.txt
│ └── manage.py
└── frontend/
  ├── src/
  │ ├── components/ # ProductCard, CategoryFilter, StoreHeader, FloatingWhatsAppButton
  │ ├── views/ # HomeView, ProductDetailView
  │ ├── lib/ # api.js (API calls), whatsapp.js, colors.js
  │ ├── router/ # Vue Router config
  │ ├── App.vue
  │ └── style.css
  └── .env # VITE_API_URL, VITE_STORE_SLUG
```
## Running the project locally

### Backend

```bash
cd backend
conda create -n catalogue-boutique python=3.12
conda activate catalogue-boutique
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create a `backend/.env` file with:

```bash
SECRET_KEY=               # Django secret key (min. 50 characters)
DEBUG=True                # False in production
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=             # Empty = SQLite locally, PostgreSQL in production

CLOUDINARY_CLOUD_NAME=    # From dashboard.cloudinary.com
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Create a `frontend/.env` file with:

```bash
VITE_API_URL=http://127.0.0.1:8000/api
VITE_STORE_SLUG=the-store-slug
```

## API endpoints

All routes are prefixed with `/api/`.

| Method | Route | Description |
|---|---|---|
| GET | `/stores/` | List of active stores |
| GET | `/stores/<slug>/` | Store details (name, tagline, address, WhatsApp, currency, colors, logo) |
| GET | `/stores/<slug>/categories/` | A store's categories |
| GET | `/stores/<slug>/products/` | A store's available products (paginated, 20/page) |
| | `?category=<slug>` | Filter by category |
| | `?search=<text>` | Search by name/description (accent-insensitive) |
| GET | `/stores/<slug>/products/<id>/` | Product detail page (all photos) |
| POST | `/stores/<slug>/products/<id>/track-click/` | Logs a click on "Ask/Order" (stats) |

## Running tests

```bash
cd backend
python manage.py test catalog
```

## Features

- Catalog filterable by category, with search (accent-insensitive)
- Product detail page with photo gallery
- Fixed price or "price on request"
- Per-store currency and colors (`Store` model)
- WhatsApp inquiry tracking per product (admin)
- Pagination ("Load more")

## Deployment

| Component | Service | Notes |
|---|---|---|
| Frontend | [Netlify](https://netlify.com) | Build: `npm run build` - `frontend/dist` folder |
| Backend | [Render](https://render.com) | Free tier |
| Database | [Neon](https://neon.tech) | Free PostgreSQL, no expiry |
| Photos | [Cloudinary](https://cloudinary.com) | 25 free credits/month |

Environment variables to set on Render:

```bash
SECRET_KEY=...
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-site-name.netlify.app
DATABASE_URL=... (provided by Neon)
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

Render build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput --upload-unhashed-files && python manage.py migrate
```

Environment variables to set on Netlify:

```bash
VITE_API_URL=https://your-service-name.onrender.com/api
VITE_STORE_SLUG=the-store-slug
```