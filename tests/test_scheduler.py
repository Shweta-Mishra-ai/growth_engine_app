"""
tests/test_scheduler.py — Tests for scheduler service (load, save, delete, clear, export).
"""
import os
import pytest
from services.scheduler_service import (
    load_scheduled_posts, save_scheduled_post,
    delete_scheduled_post, clear_scheduled_posts,
    export_scheduled_posts_csv, export_scheduled_posts_json,
)


@pytest.fixture
def tmp_schedule_file(tmp_path):
    return str(tmp_path / "test_scheduled_posts.json")


def test_load_empty_schedule(tmp_schedule_file):
    posts = load_scheduled_posts(tmp_schedule_file)
    assert posts == []


def test_save_scheduled_post(tmp_schedule_file):
    new_post = save_scheduled_post(
        platform="LinkedIn",
        content="Testing post scheduling functionality",
        date="2026-10-10",
        time="09:00",
        file_path=tmp_schedule_file,
    )
    assert new_post["id"] == 1
    assert new_post["platform"] == "LinkedIn"
    assert new_post["status"] == "Scheduled"

    loaded = load_scheduled_posts(tmp_schedule_file)
    assert len(loaded) == 1
    assert loaded[0]["content"].startswith("Testing post")


def test_delete_scheduled_post(tmp_schedule_file):
    p1 = save_scheduled_post("Twitter/X", "Tweet 1", "2026-10-11", "10:00", tmp_schedule_file)
    p2 = save_scheduled_post("LinkedIn", "Post 2", "2026-10-12", "11:00", tmp_schedule_file)

    deleted = delete_scheduled_post(p1["id"], tmp_schedule_file)
    assert deleted is True

    loaded = load_scheduled_posts(tmp_schedule_file)
    assert len(loaded) == 1
    assert loaded[0]["id"] == p2["id"]


def test_clear_scheduled_posts(tmp_schedule_file):
    save_scheduled_post("Instagram", "Caption 1", "2026-10-13", "12:00", tmp_schedule_file)
    clear_scheduled_posts(tmp_schedule_file)
    assert load_scheduled_posts(tmp_schedule_file) == []


def test_export_schedule_csv_and_json(tmp_schedule_file):
    posts = [
        {"id": 1, "platform": "LinkedIn", "date": "2026-10-15", "time": "14:00", "status": "Scheduled", "full_content": "Post content"},
    ]
    csv_str = export_scheduled_posts_csv(posts)
    assert "platform" in csv_str
    assert "LinkedIn" in csv_str

    json_str = export_scheduled_posts_json(posts)
    assert "LinkedIn" in json_str
