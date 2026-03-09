

## Plan: Add AWS App Runner Deployment Files for Django Backend

### What We'll Create

Four files to make the Django backend deployable on AWS App Runner:

1. **`Dockerfile`** — Multi-stage build with Python 3.11, installs dependencies, runs Gunicorn on port 8000
2. **`requirements.txt`** — All Python dependencies (Django, DRF, psycopg2, gunicorn, msal, ckeditor, Pillow, requests)
3. **`.dockerignore`** — Excludes frontend files (`node_modules`, `dist`, `src/`, etc.) and unnecessary files from the image
4. **`apprunner.yaml`** — App Runner service config specifying build/run commands, port 8000, health check on `/api/blogs/`, and environment variable placeholders

### Technical Details

- **Gunicorn** as the WSGI server (3 workers, binding to `0.0.0.0:8000`)
- **`collectstatic`** runs at build time
- **Health check** hits `/api/blogs/` (a public GET endpoint)
- **Environment variables** (DB credentials, Azure keys, `SECRET_KEY`) will be configured in the App Runner console — not hardcoded
- The Dockerfile will modify `settings.py` behavior to read from `os.environ` when `secrets.json` is absent (it already falls back to an empty dict)
- **`DJANGO_SETTINGS_MODULE`** set in Dockerfile
- Static/media files: `collectstatic` included; for production media uploads you'd use S3 (noted in comments)

### What You'll Need to Configure in App Runner Console

Environment variables: `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, `AZURE_SENDER_UPN`, `DEFAULT_FROM_EMAIL`, `NOTIFY_CONTACT_RECIPIENTS`

