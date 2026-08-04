# Student Store

A simple e-commerce web app built with Django, Tailwind CSS, and SQLite (PostgreSQL on Render). Manage products and orders from the Django admin panel — no code changes needed to add inventory.

## Project structure

```
store/                  # Django project settings & root URLs
shop/                   # E-commerce app (models, views, templates)
  models.py             # Product, Order, OrderItem
  views.py              # Homepage, cart, checkout, etc.
  cart.py               # Session-based cart helpers
  admin.py              # Admin panel configuration
  templates/shop/       # HTML templates (Tailwind via CDN)
  management/commands/  # seed_products command
manage.py               # Django CLI entry point
requirements.txt        # Python dependencies
```

---

## Run locally

### 1. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables (optional for local dev)

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
```

Defaults work out of the box for local development. Edit `.env` if you want a custom `SECRET_KEY`.

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password. You'll use this to log in at `/admin`.

### 6. Seed sample products

```bash
python manage.py seed_products
```

This adds 10 sample products so the store isn't empty.

### 7. Start the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

- **Storefront:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

---

## Deploy to Render

### Prerequisites

- A [Render](https://render.com) account (free tier works)
- Your project pushed to a GitHub repository

### Step 1 — Create a PostgreSQL database

1. In the Render dashboard, click **New +** → **PostgreSQL**.
2. Choose the **Free** plan, pick a name (e.g. `student-store-db`), and create it.
3. Once created, copy the **Internal Database URL** (starts with `postgres://`).

### Step 2 — Create a Web Service

1. Click **New +** → **Web Service**.
2. Connect your GitHub repo containing this project.
3. Configure the service:

| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| **Start Command** | `gunicorn store.wsgi:application` |

### Step 3 — Set environment variables

In the Web Service **Environment** tab, add:

| Key | Value |
|---|---|
| `SECRET_KEY` | A long random string (generate one at https://djecrety.ir/) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | Your Render hostname, e.g. `student-store-ebot.onrender.com` |
| `DATABASE_URL` | Paste the Internal Database URL from Step 1 |
| `RESEND_API_KEY` | Your Resend API key for HTTPS email delivery |
| `DEFAULT_FROM_EMAIL` | Optional sender email (defaults to `onboarding@resend.dev`) |

Required Render environment variables for this project are:

- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `SECRET_KEY`
- `DEBUG`
- `RESEND_API_KEY`

> Render auto-links the database if you create the Web Service from the database page. In that case `DATABASE_URL` is set automatically.

### Step 4 — Deploy

Click **Create Web Service**. Render will build and deploy automatically.

After the first deploy:

1. Open the **Shell** tab in your Render service.
2. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
3. Seed products:
   ```bash
   python manage.py seed_products
   ```

Your store is live at `https://your-app-name.onrender.com`.

---

## Managing the store

Use the Django admin at `/admin` to:

- **Add / edit / delete products** (name, description, price, image URL, stock)
- **View orders** placed by customers
- **Mark orders as paid** with the `is_paid` checkbox

No code changes are needed to manage inventory.
