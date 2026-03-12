# Product Analytics Event Generator

Generates 3-5M realistic music streaming events for ~50k users over 6 months, partitioned for S3 data lake.

## Features
- Realistic sessions: login → search → play/like (Poisson dist., tenure-based probs)
- Schema: UUID event_id, user_id, timestamp, metadata (song_id/artist_id)
- Output: JSONL partitioned `raw/events/year=YYYY/month=MM/day=DD/file.jsonl`
- Scale: Tested on 8GB laptop, chunks to avoid OOM[cite:5]

## Quickstart
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python generate_events.py --users 50000 --months 6 --output ./output
python upload_to_s3.py ./output your-s3-bucket
