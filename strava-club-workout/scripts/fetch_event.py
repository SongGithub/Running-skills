#!/usr/bin/env python3
"""Fetch Strava club events and display upcoming workouts.

Usage:
  python3 fetch_event.py mrc          — Show MRC upcoming events
  python3 fetch_event.py dct          — Show DCT upcoming events  
  python3 fetch_event.py mrc detail   — Show full event descriptions
"""
import json, ssl, sys, os
from urllib.request import Request, urlopen
from urllib.parse import urlencode

try:
    import certifi
    _ssl_ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _ssl_ctx = ssl.create_default_context()

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLUBS = {'mrc': 882047, 'dct': 1259829}

def strava_token():
    config = json.loads(open(os.path.join(WORKSPACE, 'strava_config.json')).read())
    data = urlencode({
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'grant_type': 'refresh_token',
        'refresh_token': config['refresh_token'],
    }).encode()
    req = Request('https://www.strava.com/api/v3/oauth/token', data)
    with urlopen(req, context=_ssl_ctx) as resp:
        result = json.loads(resp.read())
    config['refresh_token'] = result['refresh_token']
    with open(os.path.join(WORKSPACE, 'strava_config.json'), 'w') as f:
        json.dump(config, f, indent=2)
    return result['access_token']

def strava_get(path):
    token = strava_token()
    req = Request(f'https://www.strava.com/api/v3{path}',
                  headers={'Authorization': f'Bearer {token}'})
    with urlopen(req, context=_ssl_ctx) as resp:
        return json.loads(resp.read())

import time
def cmd_list(club_key, show_detail=False):
    cid = CLUBS.get(club_key.lower())
    if not cid:
        print(f'Unknown club: {club_key}. Options: {list(CLUBS.keys())}')
        return
    events = strava_get(f'/clubs/{cid}/group_events')
    print(f'Events for {club_key.upper()} (ID: {cid}):')
    for e in events:
        upcomm = e.get('upcoming_occurrences', [])
        if not upcomm:
            continue
        title = e.get('title', '?')
        print(f'\n📌 {title}')
        for occ in upcomm:
            print(f'   🗓️ {occ}')
        if show_detail:
            time.sleep(0.2)
            try:
                detail = strava_get(f'/clubs/{cid}/group_events/{e["id"]}')
                desc = detail.get('description', '')[:500]
                if desc:
                    print(f'   📝 {desc[:200]}...' if len(desc)>200 else f'   📝 {desc}')
            except:
                pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1].lower()
    show_detail = len(sys.argv) > 2 and sys.argv[2].lower() == 'detail'
    cmd_list(cmd, show_detail)
