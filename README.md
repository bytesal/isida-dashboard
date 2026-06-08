<div align="center">

<img src="https://img.shields.io/badge/iSida-Dashboard-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="iSida Dashboard"/>

# 🌐 iSida Dashboard

**Web control panel for the iSida Discord moderation bot**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com/cloud/atlas)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat-square&logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)

<br/>

> 🔗 **Live Demo**: [isida-dashboard.onrender.com](https://isida-dashboard.onrender.com)
> — Manage your Discord servers from a modern, responsive web interface.

</div>

---

## ✨ Features

| | Feature | Details |
|---|---|---|
| 🔐 | **Discord OAuth2 Login** | Secure login — only admins/owners of servers where iSida is present can access |
| ⚠️ | **Warnings Management** | View all warnings with moderator, reason & timestamp |
| 📋 | **Moderation Logs** | Full audit trail of all actions (kicks, bans, warns, lockdowns, auto‑mod) |
| ✅ | **Verification Settings** | Configure reaction‑role system (channel, role, emoji) from the dashboard |
| 🎫 | **Ticket Transcripts** | View saved support ticket transcripts from `/transcript` |
| 🖥️ | **Server Overview** | See all eligible servers with icons and role badges (Owner / Admin) |
| 📱 | **Responsive Design** | Works seamlessly on desktop, tablet, and mobile |

---

## 🏗️ Architecture

| Component | Technology |
|---|---|
| ⚙️ Backend | FastAPI (Python) |
| 🎨 Frontend | HTML / CSS / JS with Jinja2 templates |
| 🗄️ Database | MongoDB (via Motor async driver) |
| 🔐 Authentication | Discord OAuth2 (session‑based) |
| 🚀 Deployment | Render (recommended) |

---

## 📁 Repository Structure

```
iSida-Dashboard/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # MongoDB connection handler
│   ├── routers/
│   │   ├── auth.py             # OAuth2 login, logout, user info
│   │   ├── guilds.py           # Fetch user's guilds (filtered by admin/owner)
│   │   ├── warnings.py         # GET warnings for a guild
│   │   ├── logs.py             # GET moderation logs for a guild
│   │   ├── verification.py     # GET/POST verification settings
│   │   ├── transcripts.py      # GET transcripts and transcript details
│   │   └── discord.py          # Proxy to Discord API (channels, roles)
│   ├── templates/
│   │   ├── dashboard.html      # Server grid
│   │   ├── warnings.html       # Warnings table
│   │   ├── logs.html           # Mod logs table
│   │   ├── verification.html   # Verification settings form
│   │   └── transcripts.html    # Transcript list + viewer
│   └── static/                 # CSS / images (optional)
├── requirements.txt
├── render.yaml                 # Render.com deployment config
├── runtime.txt                 # Python 3.12
└── .env.example
```

---

## 🔗 API Endpoints

All endpoints are prefixed with `/api`, return JSON, and require a valid session cookie (obtained after login).

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/guilds/` | List servers where user is admin/owner and iSida is present |
| `GET` | `/api/warnings/{guild_id}` | All warnings for the guild |
| `GET` | `/api/logs/{guild_id}` | All moderation logs for the guild |
| `GET` | `/api/verification/{guild_id}` | Current verification settings |
| `POST` | `/api/verification/{guild_id}` | Update verification settings |
| `GET` | `/api/transcripts/{guild_id}` | List all saved transcripts |
| `GET` | `/api/transcripts/detail/{transcript_id}` | Full transcript content |
| `GET` | `/api/discord/guilds/{guild_id}/channels` | List text channels (for settings form) |
| `GET` | `/api/discord/guilds/{guild_id}/roles` | List roles (for settings form) |

---

## 🚀 Deployment (Render)

### 1️⃣ Push to GitHub

Push your code to a GitHub repository.

### 2️⃣ Create a Web Service on Render

Connect your repository, then configure:

```
Build Command:  pip install -r requirements.txt
Start Command:  uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

> Render will auto-detect `render.yaml` if present.

### 3️⃣ Set Environment Variables

| Variable | Description |
|---|---|
| `MONGO_URI` | MongoDB connection string (same as iSida bot) |
| `DISCORD_BOT_TOKEN` | Token of your iSida bot (to fetch guild channels & roles) |
| `CLIENT_ID` | Discord OAuth2 application client ID |
| `CLIENT_SECRET` | Discord OAuth2 application client secret |
| `REDIRECT_URI` | OAuth2 redirect URI — `https://your-dashboard.onrender.com/auth/callback` |
| `SECRET_KEY` | Strong random string for session signing |

### 4️⃣ Discord OAuth2 Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application → **OAuth2 → General**
3. Add `https://your-dashboard.onrender.com/auth/callback` as a **Redirect URI**
4. Copy your **Client ID** and **Client Secret**
5. In the **Bot** section, copy the bot token (must match the bot in your servers)

---

## 💻 Local Development

```bash
# 1. Clone the repository
git clone https://github.com/bytesal/isida-dashboard.git
cd isida-dashboard

# 2. Create virtual environment (Python 3.12)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Fill in all values in .env

# 5. Run the development server
uvicorn app.main:app --reload

# 6. Open in browser
# http://localhost:8000
```

---

## 🧪 Testing the Dashboard

1. 🔐 **Log in** with your Discord account (must be admin/owner of a server with iSida)
2. 🖥️ **Select a server** from the grid
3. ⚠️ **View warnings** — issued warnings appear in a sortable table
4. 📋 **View mod logs** — actions like `/kick`, `/ban` appear after execution
5. ✅ **Configure verification** — pick a channel and role, save, then run `/verify create`
6. 🎫 **View transcripts** — appear after staff runs `/transcript` in a ticket channel

---



## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests.
For major changes, open an issue first to discuss what you'd like to change.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

## 📬 Support

| | Link |
|---|---|
| 🌐 Live Dashboard | [isida-dashboard.onrender.com](https://isida-dashboard.onrender.com) |
| 🐛 Dashboard Issues | [Open an Issue on GitHub](https://github.com/bytesal/isida-dashboard/issues) |
| 💬 Bot & General Help | [Join iSida Support Server](https://discord.gg/AK4qMNdaWp) |

---

<div align="center">

Made by [bytesal](https://github.com/bytesal)

[![GitHub](https://img.shields.io/badge/GitHub-bytesal-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/bytesal/isida-dashboard)
[![Discord](https://img.shields.io/badge/Support-Discord-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/AK4qMNdaWp)

</div>
