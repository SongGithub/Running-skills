#!/usr/bin/env python3
"""Shoe tracker — fetch Strava photo, identify shoe, record distance, bind Garmin gear.

Usage:
  python3 track_shoe.py latest    — Show recent Strava activities with photos
  python3 track_shoe.py track N   — Track shoe for activity N (Strava ID)
"""
import json, sys, ssl, os
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from pathlib import Path

try:
    import certifi
    _ssl_ctx = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _ssl_ctx = ssl.create_default_context()

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _strava_token():
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

def _strava_get(path):
    token = _strava_token()
    url = f'https://www.strava.com/api/v3/{path}'
    req = Request(url, headers={'Authorization': f'Bearer {token}'})
    with urlopen(req, context=_ssl_ctx) as resp:
        return json.loads(resp.read())

def cmd_latest():
    """Show recent activities, highlight those with photos."""
    acts = _strava_get('athlete/activities?per_page=10')
    print('Recent Strava activities:')
    print(f'{"Date":12s} {"ID":14s} {"Dist":6s} {"Photo":5s}  Name')
    print('-' * 60)
    for a in acts:
        dt = a['start_date'][:10]
        aid = a['id']
        dist = a['distance'] / 1000
        photos = a.get('total_photo_count', 0)
        name = a.get('name', '')
        has_photo = '📸' if photos > 0 else ''
        print(f'{dt:12s} {aid:14d} {dist:.1f}km {has_photo:5s}  {name}')
        if photos > 0:
            detail = _strava_get(f'activities/{aid}')
            photos_data = detail.get('photos', {})
            primary = photos_data.get('primary', {}) if isinstance(photos_data, dict) else {}
            urls = primary.get('urls', {})
            if urls:
                img_url = urls.get('600', list(urls.values())[0])
                print(f'  📷 {img_url}')

def cmd_track(strava_id):
    """Track shoe for a specific Strava activity."""
    detail = _strava_get(f'activities/{strava_id}')
    dist_km = detail['distance'] / 1000
    name = detail.get('name', '')
    dt = detail.get('start_date', '')[:10]

    photos_data = detail.get('photos', {})
    primary = photos_data.get('primary', {}) if isinstance(photos_data, dict) else {}
    urls = primary.get('urls', {})
    img_url = urls.get('600', list(urls.values())[0] if urls else None)

    print(f'Activity: {name} ({dt})')
    print(f'Distance: {dist_km:.1f} km')
    print(f'Photo URL: {img_url}')
    print()
    print('Pass the photo URL to the AI agent\'s vision tool to identify the shoe.')
    print('Then record with: sqlite3 runs.db \"INSERT INTO run_shoes ...\"')
    print('And bind Garmin gear: g.add_gear_to_activity(gear_uuid, garmin_activity_id)')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: track_shoe.py [latest|track <strava_id>]')
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'latest':
        cmd_latest()
    elif cmd == 'track' and len(sys.argv) > 2:
        cmd_track(sys.argv[2])
    else:
        print(f'Unknown command: {cmd}')
