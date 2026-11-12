# Django_Movie_Recommender_Ai
Personalized movie recommendation engine built with Django (content-based, Jaccard similarity on genres).

## Run locally
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py load_movies
python manage.py make_recommendations
python manage.py runserver
```

## Config (environment variables)
| Variable | Default | Notes |
|---|---|---|
| `DJANGO_SECRET_KEY` | dev-only key | **Set this** for any deployment |
| `DJANGO_DEBUG` | `1` | Set `0` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated |
