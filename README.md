# Novapex WhatsApp Bot

This is a small Flask webhook for the Novapex WhatsApp Cloud API flow.

## Bot flow

Hi / Hello / Hey / START -> Main menu

1 -> Novapex Information
2 -> Website Development
3 -> More Details
0 -> Main menu

## Important secrets

Never put your Meta access token in source code, screenshots, GitHub, or chat.
Set `WHATSAPP_TOKEN`, `PHONE_NUMBER_ID`, and `VERIFY_TOKEN` as environment variables on the hosting service.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The webhook route is:

`/webhook`

For Meta, the Callback URL must be your public HTTPS URL ending in `/webhook`.

Example:

`https://YOUR-DOMAIN.example/webhook`

The Verify Token in Meta must exactly match your `VERIFY_TOKEN` environment variable.

## Deployment

Deploy this project to any service that supports a Python Flask/Gunicorn web service and provides a public HTTPS URL.

After deployment, test:

`https://YOUR-DOMAIN.example/`

It should show:

`Novapex WhatsApp Bot is running.`

Then configure the Meta Webhook with:

- Callback URL: `https://YOUR-DOMAIN.example/webhook`
- Verify Token: the same value as `VERIFY_TOKEN`

Subscribe the WhatsApp `messages` webhook field after verification.

## Graph API version

`GRAPH_API_VERSION` is configurable so the app can be updated when Meta requires a newer Graph API version. Use the version shown/recommended by your current Meta WhatsApp Cloud API setup.
