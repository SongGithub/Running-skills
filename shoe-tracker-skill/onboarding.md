# Shoe Tracker Skill — Onboarding Guide

Follow these steps to set up the shoe tracker in your AI agent.

## 1. Garmin Connect Setup

You need a Garmin Connect account with running data.

### Token-based auth
The Garmin `garminconnect` library stores session tokens in a JSON file.

```python
from garminconnect import Garmin
from pathlib import Path

g = Garmin("your.email@example.com")
# First time: full login with MFA
g.login()
# Save tokens
Path.home().joinpath(".config/garmin/tokens.json").write_text(g.client.dumps())
# Subsequent sessions:
g.client.loads(Path.home().joinpath(".config/garmin/tokens.json").read_text())

# REQUIRED: Load display name
prof = g.client.connectapi("/userprofile-service/socialProfile")
g.display_name = prof.get("displayName")
```

**MFA note:** Garmin sends 6-digit codes to your email. Your AI agent may need access to fetch these.

## 2. Strava API Setup

Create a Strava API app at https://www.strava.com/settings/api

Save these in `strava_config.json`:
```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "refresh_token": "YOUR_INITIAL_REFRESH_TOKEN",
  "access_token": null,
  "expires_at": 0
}
```

To get the initial `refresh_token`, complete the OAuth authorization code flow (one-time setup):
1. Visit: `https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=read,activity:read_all`
2. Authorize, copy the `code` from the redirect URL
3. Exchange it:
   ```bash
   curl -X POST https://www.strava.com/api/v3/oauth/token \
     -d client_id=YOUR_CLIENT_ID \
     -d client_secret=YOUR_CLIENT_SECRET \
     -d code=THE_CODE_FROM_URL \
     -d grant_type=authorization_code
   ```
4. Save `refresh_token` from the response into `strava_config.json`

## 3. Initialize the Database

Run the schema to create tables:
```bash
sqlite3 runs.db < schema/schema.sql
```

## 4. Onboard Your Shoes

Copy `reference/SHOE_TEMPLATE.md` to `reference/SHOE_TRACKING.md`.

For each shoe you own:
- Insert a row in the `shoes` table
- Take a photo of the shoe from the side (showing logos/colors clearly)
- Describe its visual features in `SHOE_TRACKING.md`

Example:
```sql
INSERT INTO shoes (brand, model, color, notes)
VALUES ('Adidas', 'Adizero EVO SL', '黑/白条纹', 'Garmin UUID: xyz');
```

## 5. Test

Upload a Strava run with a shoe photo. Ask your agent: "记一下这双鞋的公里数"

If the agent is set up correctly, it should:
1. Find the photo
2. Identify the shoe
3. Record the km
4. Bind it on Garmin Gear

## File Locations

The skill expects these files in the workspace root directory:
- `runs.db` — database
- `strava_config.json` — Strava API config
- `~/.config/garmin/tokens.json` — Garmin tokens
- `references/SHOE_TRACKING.md` — shoe visual guide
