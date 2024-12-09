import pytest
from datetime import datetime
import os
from app.main import (
    load_data,
    video_with_highest_views,
    average_likes_to_views_ratio,
    filter_popular_videos,
    avg_comments_popular_videos,
    video_filter_generator,
    top_videos_by_category
)


TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'videos-stats.csv')

@pytest.fixture
def test_data():
    return load_data(TEST_DATA_PATH)

def test_load_data(test_data):
    assert isinstance(test_data, list)
    assert len(test_data) > 0

def test_video_with_highest_views(test_data):
    result = video_with_highest_views(test_data)
    assert result == "El Chombo - Dame Tu Cosita feat. Cutty Ranks (Official Video) [Ultra Music]"

def test_average_likes_to_views_ratio(test_data):
    result = average_likes_to_views_ratio(test_data)
    assert result == pytest.approx(0.08502870)

def test_filter_popular_videos(test_data):
    result = filter_popular_videos(test_data)
    assert len(result) == 99

def test_avg_comments_popular_videos(test_data):
    result = avg_comments_popular_videos(test_data)
    assert result == pytest.approx(7808.4732)

def test_top_videos_by_category(test_data):
    categories = ['gaming', 'tech', 'crypto']

    result = top_videos_by_category(test_data, categories)
    expected_gaming_videos = [
        {'category': 'gaming', 'comment_count': 14706, 'likes': 238193, 'published_at': datetime(2020, 11, 14).date(),
         'title': 'PlayStation 5 Review: Next Gen Gaming!', 'views': 7132206},
        {'category': 'gaming', 'comment_count': 15609, 'likes': 298406, 'published_at': datetime(2022, 8, 24).date(),
         'title': 'I OPENED MY OWN ARCADE SHOP', 'views': 3773387},
        {'category': 'gaming', 'comment_count': 6315, 'likes': 71905, 'published_at': datetime(2022, 5, 6).date(),
         'title': 'The Story of Super Mario World | Gaming Historian', 'views': 2381931}
    ]
    assert result['gaming'] == expected_gaming_videos

def test_video_filter_generator(test_data):
    result = list(video_filter_generator(test_data))
    assert len(result) == 3