from envparse import env

env.read_envfile()

SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-u@5e0w_8c49+#oe#+bre(kawayyzi9gu#5%aje6@25(s^8($2s")
DJANGO_DEBUG = env.bool("DJANGO_DEBUG", default=True)

POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD", default="")
POSTGRES_USER = env.str("POSTGRES_USER", default="user")
POSTGRES_DB = env.str("POSTGRES_DB", default="database")
