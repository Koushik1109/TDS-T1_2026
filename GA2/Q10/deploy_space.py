#!/usr/bin/env python3
"""
Deploy the deployment observability API to Hugging Face Spaces using the Docker SDK.
Creates Space ga2-b0b396 with public visibility, CPU Basic tier, and GA2_TOKEN_5D77 secret.

Usage:
    pip install huggingface_hub
    export HF_TOKEN=your_huggingface_token
    python deploy_space.py
"""
import os
from pathlib import Path

from huggingface_hub import HfApi

SPACE_NAME = "ga2-b0b396"
HARDWARE = "cpu-basic"
SECRET_KEY = "GA2_TOKEN_5D77"
SECRET_VALUE = "ga2-token-5d77-deployment-ready"


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit(
            "HF_TOKEN environment variable is required. "
            "Get your token from https://huggingface.co/settings/tokens"
        )

    api = HfApi(token=token)
    user = api.whoami()
    username = user["name"]
    repo_id = f"{username}/{SPACE_NAME}"

    print(f"Creating Space {repo_id} (public, Docker SDK, {HARDWARE})...")
    try:
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True,
            space_hardware=HARDWARE,
            space_secrets=[{"key": SECRET_KEY, "value": SECRET_VALUE}],
        )
    except TypeError:
        # Older huggingface_hub may not support space_hardware/space_secrets
        api.create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True,
        )
        api.add_space_secret(repo_id=repo_id, key=SECRET_KEY, value=SECRET_VALUE)
        try:
            api.request_space_hardware(repo_id=repo_id, hardware=HARDWARE)
        except Exception:
            pass  # cpu-basic is default
    print("Space created (or already exists).")

    root = Path(__file__).parent
    files_to_upload = [
        "README.md",
        "Dockerfile",
        "requirements.txt",
        "main.py",
        ".dockerignore",
    ]

    print("Uploading files...")
    for fname in files_to_upload:
        path = root / fname
        if path.exists():
            api.upload_file(
                repo_id=repo_id,
                repo_type="space",
                path_in_repo=fname,
                path_or_fileobj=str(path),
            )
            print(f"  Uploaded {fname}")
        else:
            print(f"  WARNING: {fname} not found, skipping")

    # Ensure secret exists (create_repo may have set it; add_space_secret upserts)
    try:
        api.add_space_secret(repo_id=repo_id, key=SECRET_KEY, value=SECRET_VALUE)
        print(f"Secret {SECRET_KEY} configured.")
    except Exception as e:
        print(f"Note: Secret may already exist: {e}")

    url = f"https://huggingface.co/spaces/{repo_id}"
    print(f"\nPublic Space URL: {url}")
    print("Paste this URL in the grader. The Space will build; wait for it to become ready.")


if __name__ == "__main__":
    main()
