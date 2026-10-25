#!/usr/bin/env python3
"""Garmin setup helper — login and save tokens.

Usage:
  python3 garmin_setup.py
"""
import json, sys, os, getpass
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_garmin():
    """Interactive Garmin login flow."""
    print("=== Garmin Connect Setup ===")
    print()
    
    email = input("Garmin email: ").strip()
    password = getpass.getpass("Garmin password: ").strip()
    
    try:
        from garminconnect import Garmin
        
        def mfa_callback():
            print("\nGarmin sent a 6-digit code to your email.")
            return input("Enter MFA code: ").strip()
        
        g = Garmin(email, password, prompt_mfa=mfa_callback)
        g.login()
        
        tokens_path = Path.home().joinpath('.config/garmin/tokens.json')
        tokens_path.parent.mkdir(parents=True, exist_ok=True)
        tokens_path.write_text(g.client.dumps())
        
        print(f"\n✅ Tokens saved to {tokens_path}")
        print("Your AI agent can now access Garmin data.")
        
    except ImportError:
        print("❌ garminconnect library not installed.")
        print("Install: pip install garminconnect")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_garmin()
