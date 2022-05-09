# kanop-test

To run the app in a shell:

```
FLASK_APP=kanop.py \
SECRET_KEY=*** \
SECURITY_PASSWORD_SALT=*** \
EMAIL=*** \
PASSWORD=*** \
flask run
```

To run the app in a docker container:

```
docker run \
--env FLASK_APP=kanop.py \
--env SECRET_KEY=*** \
--env SECURITY_PASSWORD_SALT=*** \
--env EMAIL=*** \
--env PASSWORD=*** \
-p 5000:5000 \
kanop
```

To generate a salt, use `secrets.SystemRandom().getrandbits(128)`.

To generate a secret key, use `secrets.token_urlsafe()`.
