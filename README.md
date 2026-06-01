# mariashoaib.com — Backend (Django + DRF)

REST API + admin for Maria Shoaib's nutrition practice site. Pairs with the Next.js
frontend in `ms_fe/`.

## Stack

- Django 5.1 + Django REST Framework
- `djangorestframework-simplejwt` for JWT issuance
- `google-auth` for Google id_token verification (no allauth / dj-rest-auth)
- PostgreSQL in production, SQLite fallback for local dev
- WhiteNoise for static, Pillow for media
- Email notifications via Django's SMTP backend (post_save signals)

## Layout (flat apps alongside `core/`)

```
core/                project, settings, root URL + api_urls
common/              shared mixins (TimeStampMixin, UUIDPKMixin), SingletonModel, email helper, validators
accounts/            User (email-based) + Client profile + Google OAuth view
services/            Service catalog
slots/               AvailableSlot + recurring-slot admin form
appointments/        Appointment lifecycle + post_save email notification
site_content/        PaymentInstruction (singleton), SiteSettings (singleton), ContactMessage + signal
```

## Local setup

```bash
cd ms_be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.sample .env             # then fill in
python manage.py migrate
python manage.py loaddata services/fixtures/initial_services.json site_content/fixtures/initial_site.json
python manage.py createsuperuser
python manage.py runserver
```

The `.env.sample` defaults the project to SQLite + console email so it boots with
zero infra. Set `USE_SQLITE=false` and fill `DB_*` to switch to Postgres.

## Public API surface (under `/api/v1/`)

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/services/` | – | Active service catalog (sorted by `display_order`) |
| GET | `/slots/?date=YYYY-MM-DD&type=ONLINE\|INPERSON` | – | Bookable slots on a date |
| GET | `/slots/available-dates/?month=YYYY-MM&type=…` | – | Dates with at least one slot |
| GET | `/payment-instructions/` | – | Singleton bank-transfer payload |
| GET | `/site-settings/` | – | Singleton stats + About copy |
| POST | `/appointments/` | – | Create booking (anonymous OK) |
| POST | `/contact/` | – | Public contact form |
| POST | `/auth/google/` | – | Verify Google id_token, return JWT pair |
| POST | `/auth/refresh/` | – | Refresh JWT access token |
| GET | `/clients/me/` | Bearer | Logged-in client profile |
| PATCH | `/clients/me/` | Bearer | Update phone |
| GET | `/appointments/mine/?status=…` | Bearer | List own bookings |
| GET | `/appointments/mine/<booking_reference>/` | Bearer | Booking detail |
| POST | `/appointments/mine/<booking_reference>/cancel/` | Bearer | Cancel a `PENDING` booking |

## Booking lifecycle

```
              ┌─── client cancel (only when PENDING) ───┐
              │                                          ▼
created ─▶ PENDING ───admin confirm───▶ CONFIRMED       CANCELLED
              │                                          ▲
              └───admin decline───▶ DECLINED ────────────┘
```

`Appointment.save()` automatically releases the slot when the appointment
transitions into `CANCELLED`. The booking POST uses `select_for_update()` on the
slot row to prevent double-booking races.

## Email notifications

Both `Appointment` creation and `ContactMessage` creation fire `post_save` signals
that send a multipart (HTML + text) email to `settings.NOTIFICATION_EMAIL`
(`contact@mariashoaib.com` by default). Templates live in:

- `appointments/templates/emails/new_appointment.{html,txt}`
- `site_content/templates/emails/new_contact_message.{html,txt}`

The helper in `common/email.py` swallows SMTP failures (logs them) so a flaky
email host can never break a booking POST.

In dev the default email backend is `console` — emails print to `runserver`
stdout. For prod set:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=…
EMAIL_HOST_PASSWORD=…
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=no-reply@mariashoaib.com
NOTIFICATION_EMAIL=contact@mariashoaib.com
```

## Admin highlights

- **Services**: ordered list, inline `is_active` + `display_order` editing,
  slug prepopulated from name.
- **AvailableSlot**: date hierarchy, bulk enable/disable, plus a custom
  **"Add recurring slots"** intermediate form (date range × weekdays × interval).
- **Appointment**: list view with WhatsApp deep-link per row, bulk
  "Mark as Confirmed / Declined" actions, fieldsets separating client / booking
  / admin notes.
- **PaymentInstruction & SiteSettings**: singletons (add disabled once a row
  exists, deletion disabled), with a profile-photo preview on SiteSettings.
- **ContactMessage**: read-only fields, `is_read` toggle and bulk
  "Mark as read" action.

## Deploying

1. Set `ENVIRONMENT=prod`, `DEBUG=false`, a strong `SECRET_KEY`, real
   `ALLOWED_HOSTS`, real DB, real SMTP, and `GOOGLE_CLIENT_ID` matching the
   frontend.
2. `python manage.py collectstatic --noinput`
3. Run via `gunicorn core.wsgi:application` behind nginx / Railway / Render.
4. Make sure the `media/` volume is persistent (or swap WhiteNoise media for
   S3/R2 in a future iteration).

Prod-only security hardening (HSTS, secure cookies, SSL redirect) kicks in
automatically when `ENVIRONMENT=prod` and `DEBUG=false`.
