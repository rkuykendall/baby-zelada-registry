# Comment this out before you start using the site so you don't run it by accident
 source venv/bin/activate
 rm -rv registry/migrations/*
 touch registry/migrations/__init__.py
 heroku pg:reset --app simplici7y --confirm baby-zelada-registry
 ./scripts/migrate
