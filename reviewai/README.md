# ReplyFast AI — $5,000/month SaaS Business

AI-powered review response management for local businesses.

## Business Model

| Plan     | Price   | Businesses | AI Responses/month |
|----------|---------|------------|--------------------|
| Free     | $0      | 1          | 10                 |
| Starter  | $49/mo  | 3          | 100                |
| Growth   | $99/mo  | 10         | Unlimited          |
| Agency   | $249/mo | Unlimited  | Unlimited          |

**Path to $5,000/month MRR:** 60 Growth customers × $99 = $5,940 ✓

**Cost structure at 100 customers:**
- Hosting (Railway/Render): ~$25/month
- Claude API (~100 reviews × avg 10 responses × $0.002): ~$2/month
- Domain + email: ~$20/month
- **Total: ~$50/month → 99%+ margin**

## Quick Start

```bash
cd reviewai

# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Fill in ANTHROPIC_API_KEY and Stripe keys

# 3. Run
python run.py
```

Open http://localhost:5001

## Features

- **Landing page** — conversion-optimised marketing page
- **Auth** — secure register/login with hashed passwords
- **Business management** — add multiple locations with category, address, contact
- **Review inbox** — add reviews from any platform (Google, Yelp, Facebook, TripAdvisor)
- **AI response generation** — one-click Claude-powered personalised responses
- **Brand voice** — train the AI on your specific tone and style
- **Response analytics** — response rate, avg rating, sentiment tracking
- **Stripe billing** — subscription management with webhooks
- **Customer portal** — self-serve plan changes and cancellations

## Deployment (Production)

### Railway (recommended — $5/month)
```bash
railway login
railway init
railway add postgresql
railway up
```

Set environment variables in Railway dashboard.

### Render
1. Create a new Web Service → connect your GitHub repo
2. Build command: `pip install -r reviewai/requirements.txt`
3. Start command: `python reviewai/run.py`
4. Add a PostgreSQL database
5. Set `DATABASE_URL` environment variable

### Environment Variables Required
- `SECRET_KEY` — random secret for session signing
- `ANTHROPIC_API_KEY` — from console.anthropic.com
- `STRIPE_SECRET_KEY` — from dashboard.stripe.com
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_STARTER` / `STRIPE_PRICE_GROWTH` / `STRIPE_PRICE_AGENCY`
- `DATABASE_URL` — PostgreSQL connection string

## Stripe Setup

1. Create 3 products in Stripe dashboard:
   - **Starter** — $49/month recurring
   - **Growth** — $99/month recurring
   - **Agency** — $249/month recurring
2. Copy the Price IDs into your `.env`
3. Set up webhook endpoint: `https://yourdomain.com/billing/webhook`
   - Events to listen for: `customer.subscription.updated`, `customer.subscription.deleted`

## Go-to-Market Strategy

**Target customers:** Local businesses with 10+ Google reviews — restaurants, salons, gyms, dental offices, hotels, auto shops.

**Acquisition channels:**
1. **Cold email** — scrape local businesses with poor response rates via Google Maps
2. **Local Facebook groups** — "I built a tool that responds to Google reviews in 1 click"
3. **Google Ads** — "AI review management tool" ($3-8 CPC, high intent)
4. **Agency partnerships** — offer 30% recurring commission to marketing agencies

**Pricing psychology:**
- Free plan = low barrier to sign up and experience value
- Growth at $99/mo is the anchor — most perceived value
- Annual plans (2 months free) improve cashflow and reduce churn

## Tech Stack

- **Backend:** Flask + SQLAlchemy + Flask-Login
- **Database:** SQLite (dev) → PostgreSQL (prod)
- **AI:** Anthropic Claude API (claude-opus-4-6)
- **Payments:** Stripe Subscriptions + Customer Portal
- **Frontend:** Tailwind CSS (CDN) + vanilla JS
- **Deploy:** Railway, Render, or any Python host
