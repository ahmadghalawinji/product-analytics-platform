import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import uuid
import random
import numpy as np
from faker import Faker
import boto3  # Optional for S3 upload
from typing import List, Dict

fake = Faker()
NUM_SONGS = 100000
NUM_ARTISTS = 10000
SONG_TO_ARTIST = {i: random.randint(1, NUM_ARTISTS) for i in range(1, NUM_SONGS + 1)}

def generate_catalogs():
    """Pre-generate song/artist IDs."""
    return list(range(1, NUM_SONGS + 1)), list(range(1, NUM_ARTISTS + 1))

def pick_event_weights(user_tenure_days: int) -> List[float]:
    """Realistic probabilities: new users explore, old engage deeply.[web:14]"""
    if user_tenure_days < 7:
        return [0.3, 0.2, 0.25, 0.05, 0.05, 0.03, 0.12]  # signup,login,search,play,like,playlist,upgrade
    else:
        return [0.05, 0.1, 0.15, 0.4, 0.15, 0.1, 0.05]

EVENTS = ["signup", "login", "search_songs", "play_song", "like_song", "create_playlist", "upgrade_premium"]

def generate_event(user_id: int, session_id: str, ts: datetime, event_name: str, country: str, device: str = None,
                   metadata: Dict = None) -> Dict:
    """Generate single event JSON."""
    if device is None:
        device = random.choice(["mobile", "web", "tablet"])
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "event_name": event_name,
        "event_timestamp": ts.isoformat(),
        "session_id": session_id,
        "device_type": device,
        "country": country,
        "metadata": metadata or {}
    }

def generate_session(user_id: int, start_ts: datetime, country: str, tenure_days: int, avg_events: int = 10) -> List[Dict]:
    """Logical sequence: must login first, then search/play/etc."""
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    events = []
    ts = start_ts
    num_events = max(3, np.random.poisson(avg_events))  # Poisson for realism
    weights = pick_event_weights(tenure_days)
    
    # Force login as first event for realism
    first_event = generate_event(user_id, session_id, ts, "login", country)
    events.append(first_event)
    ts += timedelta(minutes=random.uniform(1, 5))
    num_events -= 1  # Already added login
    
    for _ in range(num_events):
        event_idx = np.random.choice(len(EVENTS), p=weights)
        event_name = EVENTS[event_idx]
        metadata = {}
        if event_name == "play_song":
            song_id = random.randint(1, NUM_SONGS)
            metadata = {"song_id": song_id, "artist_id": SONG_TO_ARTIST[song_id]}
        elif event_name == "like_song":
            metadata = {"song_id": random.randint(1, NUM_SONGS)}
        elif event_name == "create_playlist":
            metadata = {"playlist_id": random.randint(1, 10000)}
        elif event_name == "search_songs":
            metadata = {"query": fake.word() + " " + fake.word()}
        elif event_name == "upgrade_premium":
            metadata = {"plan": "premium_monthly"}
        
        event = generate_event(user_id, session_id, ts, event_name, country, metadata=metadata)
        events.append(event)
        ts += timedelta(minutes=random.uniform(1, 30))  # Intra-session gaps
    
    return events


def main(args):
    songs, artists = generate_catalogs()
    start_date = datetime(2025, 9, 1)  # 6 months back from Mar 2026
    end_date = datetime(2026, 3, 1)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    all_users = []
    for u in range(1, args.users + 1):
        signup_date = start_date + timedelta(days=random.uniform(0, (end_date - start_date).days))
        all_users.append({"user_id": u, "signup_date": signup_date.date(), "country": fake.country()})
    
    daily_files = {}
    for user in all_users:
        tenure_days = (start_date.date() - user["signup_date"]).days if user["signup_date"] < start_date.date() else 0
        num_sessions = max(1, int(np.random.gamma(5, 0.5))) if tenure_days > 30 else random.randint(1, 3)
        
        for _ in range(num_sessions):
            day_offset = random.randint(0, (end_date - start_date).days)
            session_start = start_date + timedelta(days=day_offset, hours=random.randint(8, 23), minutes=random.randint(0, 59))
            session_events = generate_session(user["user_id"], session_start, user["country"], tenure_days)
            
            for event in session_events:
                event_date = datetime.fromisoformat(event["event_timestamp"]).date()
                date_str = event_date.strftime("%Y/%m/%d")
                if date_str not in daily_files:
                    daily_files[date_str] = []
                daily_files[date_str].append(event)
    
    total_events = 0
    for date_str, events in daily_files.items():
        year, month, day = date_str.split('/')
        path = output_dir / f"raw/events/year={year}/month={month}/day={day}/events_{uuid.uuid4().hex[:8]}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
        total_events += len(events)
        print(f"Wrote {len(events):,} events to {path}")
    
    print(f"Generated {total_events:,} total events for {args.users} users over ~{args.months} months.[web:12]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=50000)
    parser.add_argument("--months", type=int, default=6)
    parser.add_argument("--output", default="./data")
    # parser.add_argument("--s3-bucket", default=None)  # Add for upload
    args = parser.parse_args()
    main(args)
