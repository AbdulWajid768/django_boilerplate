<div align="center">

<!-- animated header -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:020617,35:00d4aa,70:0891b2,100:7c3aed&height=200&section=header&text=Django%20Boilerplate&fontSize=44&fontColor=ffffff&animation=twinkling&desc=REST%20API%20spine%20%7C%20DRF%20%7C%20JWT%20%7C%20OAuth&descSize=16&descAlignY=72&descAlign=62"/>

<!-- typing tagline -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=18&duration=2800&pause=900&color=00D4AA&center=true&vCenter=true&multiline=true&repeat=true&width=620&height=90&lines=Boot+multi-app+backends+in+minutes;Flat-app+DRF+%2B+JWT+%2B+Google+OAuth;SQLite+dev+%E2%86%92+Postgres+prod;Slot+booking+%2B+lifecycle+ready" alt="Typing animation"/>
</a>

<br/>

### ⟡ Live telemetry ⟡

[![GitHub stars](https://img.shields.io/github/stars/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=starship&logoColor=white&labelColor=0f172a&color=00d4aa)](https://github.com/AbdulWajid768/django_boilerplate/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=git&logoColor=white&labelColor=0f172a&color=0891b2)](https://github.com/AbdulWajid768/django_boilerplate/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=eye&logoColor=white&labelColor=0f172a&color=7c3aed)](https://github.com/AbdulWajid768/django_boilerplate/watchers)
[![Open issues](https://img.shields.io/github/issues/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=githubissues&logoColor=white&labelColor=0f172a&color=f472b6)](https://github.com/AbdulWajid768/django_boilerplate/issues)

[![Last commit](https://img.shields.io/github/last-commit/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=git&logoColor=white&labelColor=0f172a&color=00d4aa)](https://github.com/AbdulWajid768/django_boilerplate/commits/main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=pulse&logoColor=white&labelColor=0f172a&color=0891b2)](https://github.com/AbdulWajid768/django_boilerplate/graphs/commit-activity)
[![Repo size](https://img.shields.io/github/repo-size/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=database&logoColor=white&labelColor=0f172a&color=7c3aed)](https://github.com/AbdulWajid768/django_boilerplate)
[![Code size](https://img.shields.io/github/languages/code-size/AbdulWajid768/django_boilerplate?style=for-the-badge&logo=codeigniter&logoColor=white&labelColor=0f172a&color=e879f9)](https://github.com/AbdulWajid768/django_boilerplate)

[![Python](https://img.shields.io/badge/Python-3.11+-00d4aa?style=for-the-badge&logo=python&logoColor=0f172a)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-a30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)

<br/>

<img src="https://github-readme-stats.vercel.app/api/pin/?username=AbdulWajid768&repo=django_boilerplate&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=00d4aa&icon_color=7c3aed&text_color=c9d1d9&border_radius=12" width="48%"/>
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=AbdulWajid768&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=00d4aa&text_color=c9d1d9&layout=compact&border_radius=12" width="48%"/>

<br/><br/>

[⚡ Quick start](#-quick-start) · [🛰 Architecture](#-architecture) · [📡 API](#-api-surface) · [🚀 Deploy](#-deploy)

<img src="https://capsule-render.vercel.app/api?type=rect&color=gradient&customColorList=0,1,2,3&height=2&section=footer" width="100%"/>

</div>

---

## ◈ Transmission

> **Mission:** Deploy a **production-shaped** Django REST backend without rewiring fundamentals every sprint.

`django_boilerplate` is a **flat-app DRF chassis**—email users, Google `id_token` verification, service catalogs, slot scheduling, appointment state machines, and CMS singletons. **SQLite + console email** boot locally; flip env vars for Postgres, SMTP, and hardened prod.

```text
     ┌─────────────┐     JWT / OAuth      ┌──────────────┐
     │  Client SPA │ ◄──────────────────► │  /api/v1/*   │
     └─────────────┘                      │  Django+DRF  │
                                          └──────┬───────┘
                                                 │
                    ┌────────────────────────────┼────────────────────────────┐
                    ▼                            ▼                            ▼
              accounts/                    appointments/                 site_content/
              services/                      slots/                      signals → mail
```

---

## ◈ Stack matrix

| Layer | Module | Role |
| --- | --- | --- |
| Core | Django 5.1 + DRF | HTTP + serialization |
| Identity | Simple JWT + `google-auth` | Bearer sessions |
| Persistence | SQLite ↔ PostgreSQL | Dev/prod parity |
| Assets | Pillow + WhiteNoise | Media + static |
| Edge | CORS headers | SPA coupling |

---

## ◈ Architecture

```text
core/           settings · WSGI/ASGI · /api/v1 router
common/         mixins · singletons · email · validators
accounts/       User + Client · Google auth endpoints
services/       Service catalog
slots/          AvailableSlot + recurring-slot admin
appointments/   Booking lifecycle · signals · templates
site_content/   PaymentInstruction · SiteSettings · Contact
```

Each app owns `api/v1/`—scale by **adding apps**, not inflating a god-module.

---

## ◈ Quick start

```bash
git clone https://github.com/AbdulWajid768/django_boilerplate.git
cd django_boilerplate

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.sample .env

python manage.py migrate
python manage.py loaddata services/fixtures/initial_services.json \
                        site_content/fixtures/initial_site.json
python manage.py createsuperuser
python manage.py runserver
```

| Endpoint | URL |
| --- | --- |
| Admin | `http://127.0.0.1:8000/admin/` |
| API | `http://127.0.0.1:8000/api/v1/` |

---

## ◈ API surface

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/services/` | — | Service catalog |
| GET | `/slots/?date=&type=` | — | Bookable slots |
| GET | `/slots/available-dates/` | — | Dates with availability |
| GET | `/payment-instructions/` | — | Payment singleton |
| GET | `/site-settings/` | — | Site copy & stats |
| POST | `/appointments/` | — | Create booking |
| POST | `/contact/` | — | Contact form |
| POST | `/auth/google/` | — | Google → JWT |
| POST | `/auth/refresh/` | — | Refresh token |
| GET/PATCH | `/clients/me/` | Bearer | Profile |
| GET | `/appointments/mine/` | Bearer | Own bookings |
| POST | `/appointments/mine/<ref>/cancel/` | Bearer | Cancel pending |

---

## ◈ Booking lifecycle

```mermaid
%%{init: {'theme':'dark', 'themeVariables': { 'primaryColor':'#00d4aa','primaryTextColor':'#020617','lineColor':'#7c3aed'}}}%%
stateDiagram-v2
    [*] --> PENDING: create
    PENDING --> CONFIRMED: admin confirm
    PENDING --> DECLINED: admin decline
    PENDING --> CANCELLED: client cancel
    CONFIRMED --> [*]
    CANCELLED --> [*]
```

`select_for_update()` on slot rows prevents double-booking under load.

---

## ◈ Deploy

1. `ENVIRONMENT=prod`, `DEBUG=false`, strong secrets, real DB + SMTP + `GOOGLE_CLIENT_ID`.
2. `python manage.py collectstatic --noinput`
3. **Gunicorn** → `core.wsgi:application` behind your proxy.
4. Persistent `media/` volume (or object storage later).

---

<div align="center">

### ⟡ Pulse over time ⟡

<a href="https://star-history.com/#AbdulWajid768/django_boilerplate&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=AbdulWajid768/django_boilerplate&type=Date&theme=dark"/>
    <img alt="Star history chart" src="https://api.star-history.com/svg?repos=AbdulWajid768/django_boilerplate&type=Date"/>
  </picture>
</a>

<br/>

<a href="https://github.com/AbdulWajid768">
  <img src="assets/github-activity-graph.svg" alt="Contribution activity graph" width="100%"/>
</a>

<sub>Auto-refreshed daily via GitHub Actions (replaces paused Vercel activity-graph API).</sub>

<br/>

**[Abdul Wajid](https://github.com/AbdulWajid768)** · Software Engineer · Lahore, PK

[![GitHub](https://img.shields.io/badge/@AbdulWajid768-181717?style=flat&logo=github)](https://github.com/AbdulWajid768)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/abdul-wajid-amin/)

<br/>

<img src="https://komarev.com/ghpvc/?username=AbdulWajid768-django_boilerplate&label=NEURAL%20VIEWS&color=00d4aa&style=for-the-badge" alt="views"/>

<sub>Forge the backend · Ship the next timeline.</sub>

</div>
