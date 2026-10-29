# django-taobao


## Required deployment configuration

Supply `DJANGO_SECRET_KEY`, `DJANGO_DB_USER`, and `DJANGO_DB_PASSWORD` in
the application process environment. Missing or blank values stop startup.
`DJANGO_DB_HOST`, `DJANGO_DB_PORT`, and `DJANGO_DB_NAME` have local-development
defaults documented in `.env.example`; set them for your own database.

Email requires `SMTP_HOST`, `SMTP_USER`, and `SMTP_PASSWORD`; `SMTP_PORT`
defaults to 465 (SMTP over TLS). `SMTP_FROM` optionally overrides the sender
address. WeChat notifications require `SERVERCHAN_SEND_KEY` when used. Missing
required mail or notification configuration raises a configuration error before
any network request. SMTP debug logging is disabled to avoid credential leakage.

The app does not automatically load `.env` files. Use a secret manager or protected
process configuration. Never commit real values or private keys. Treat formerly
committed values as exposed and replace them through the relevant provider;
changing Git history does not invalidate them. This patch does not rotate any
credential or change a deployed service. Set a fresh Django secret before deploying
and account for invalidated sessions and signed tokens.

This is a legacy Django project; these configuration changes are not a production
hardening review or a framework upgrade. Review deployment settings separately.
Run offline configuration checks with:
`python -m unittest discover -s tests -p 'test_*.py'`.
