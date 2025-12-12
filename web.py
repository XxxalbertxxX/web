from flask import Flask, redirect, request
import requests

app = Flask(__name__)

CLIENT_ID = "1449168996917317644"
CLIENT_SECRET = "cvm8wFw3JxGRCQ9D2nnX7EKHF-093ecW"
BOT_TOKEN = "MTQ0OTE2ODk5NjkxNzMxNzY0NA.G3TdHU.IOp3B3xURQ3Dti2lkFpEpkTC6-I3gHwXAhld6c"

REDIRECT_URI = "http://localhost:5000/callback"

GUILD_ID = 1448470539705516177
ROLE_ID = 1448473245434249318

DISCORD_API = "https://discord.com/api"

@app.route("/verify")
def verify():
    return redirect(
        f"{DISCORD_API}/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify guilds.join"
    )

@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(f"{DISCORD_API}/oauth2/token", data=data, headers=headers)
    token = r.json()["access_token"]

    user = requests.get(
        f"{DISCORD_API}/users/@me",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    user_id = user["id"]

    # AÑADIR ROL
    requests.put(
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}/roles/{ROLE_ID}",
        headers={
            "Authorization": f"Bot {BOT_TOKEN}"
        }
    )

    return "✅ Verificación completada, ya puedes volver a Discord"