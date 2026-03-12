import argparse
import boto3
from pathlib import Path
from tqdm import tqdm  # pip install tqdm
from dotenv import load_dotenv
import os

# Load AWS credentials from .env
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


def upload_to_s3(local_dir: Path, bucket: str, prefix: str = ""):
    """Upload all .jsonl files preserving folder structure."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    jsonl_files = list(local_dir.rglob("*.jsonl"))
    total_size_gb = sum(f.stat().st_size for f in jsonl_files) / (1024**3)
    print(f"Found {len(jsonl_files)} files totaling {total_size_gb:.2f} GB")

    for local_path in tqdm(jsonl_files, desc="Uploading"):
        # Keep folder structure relative to local_dir.parent
        rel_path = local_path.relative_to(local_dir.parent)
        s3_key = f"{prefix}{rel_path}" if prefix else str(rel_path)
        s3.upload_file(str(local_path), bucket, s3_key)
        print(f"✓ {s3_key}")

    print(f"Upload complete to s3://{bucket}/{prefix}!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload .jsonl files to S3")
    parser.add_argument("local_path", type=Path, help="Path to local folder containing .jsonl files")
    parser.add_argument("bucket", help="Existing S3 bucket name")
    parser.add_argument("--prefix", default="", help="Optional prefix/folder inside S3 bucket")
    args = parser.parse_args()

    # Only upload, assume bucket already exists
    upload_to_s3(args.local_path, args.bucket, args.prefix)