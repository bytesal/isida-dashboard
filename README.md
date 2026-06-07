# iSida Dashboard

Web dashboard for iSida Discord bot – view warnings, mod logs, and server configurations.

## Setup

1. Create a Discord Application at https://discord.com/developers/applications
2. Add OAuth2 redirect: `https://your-dashboard.onrender.com/auth/callback`
3. Copy `.env.example` to `.env` and fill values
4. Deploy on Render using `render.yaml` or manual web service.

## Environment Variables

- `MONGO_URI` – Your MongoDB connection string
- `CLIENT_ID` – Discord OAuth2 client ID
- `CLIENT_SECRET` – Discord OAuth2 client secret
- `REDIRECT_URI` – Full callback URL
- `ADMIN_USER_IDS` – Comma-separated Discord user IDs allowed to access

## Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
