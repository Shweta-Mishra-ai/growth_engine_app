import csv
import io
import json
import os
from datetime import datetime

DEFAULT_SCHEDULE_FILE = "scheduled_posts.json"


def load_scheduled_posts(file_path: str = DEFAULT_SCHEDULE_FILE) -> list[dict]:
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def save_scheduled_post(
    platform: str,
    content: str,
    date,
    time,
    file_path: str = DEFAULT_SCHEDULE_FILE,
) -> dict:
    posts = load_scheduled_posts(file_path)
    new_id = (max([p.get("id", 0) for p in posts], default=0) + 1)
    new_post = {
        "id": new_id,
        "platform": platform,
        "content": content[:160] + ("..." if len(content) > 160 else ""),
        "full_content": content,
        "date": str(date),
        "time": str(time),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "Scheduled",
    }
    posts.append(new_post)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving scheduled post: {e}")
    return new_post


def delete_scheduled_post(post_id: int, file_path: str = DEFAULT_SCHEDULE_FILE) -> bool:
    posts = load_scheduled_posts(file_path)
    filtered = [p for p in posts if p.get("id") != post_id]
    if len(filtered) != len(posts):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(filtered, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    return False


def clear_scheduled_posts(file_path: str = DEFAULT_SCHEDULE_FILE) -> bool:
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False


def export_scheduled_posts_csv(posts: list[dict]) -> str:
    output = io.StringIO()
    fieldnames = ["id", "platform", "date", "time", "status", "created_at", "full_content"]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for p in posts:
        writer.writerow(p)
    return output.getvalue()


def export_scheduled_posts_json(posts: list[dict]) -> str:
    return json.dumps(posts, indent=4, ensure_ascii=False)
