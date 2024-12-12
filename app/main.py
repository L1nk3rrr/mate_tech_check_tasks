from __future__ import annotations
from collections.abc import Iterator
from datetime import datetime
import csv
import os


def load_data(file_path: str) -> list[dict]:
    headers = ['', 'Title', 'Video ID', 'Published At', 'Keyword', 'Likes', 'Comments', 'Views']
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames=headers, delimiter=',')

        # Skip the first line if it contains incorrect header info
        next(reader)

        for row in reader:
            data.append({
                'published_at': datetime.strptime(row['Published At'], '%Y-%m-%d').date(),
                'title': row['Title'],
                'category': row['Keyword'],
                'views': int(row['Views'].rstrip('.0') or 0),
                'likes': int(row['Likes'].rstrip('.0') or 0),
                'comment_count': int(row['Comments'].rstrip('.0') or 0)
            })
    return data


def video_with_highest_views(videos) -> str:
    highest_views = max(videos, key = lambda video: video["views"])
    return highest_views["title"]


# ration = likes / views for 1 video!
# average ratio it's sum of all rations / count of videos
def average_likes_to_views_ratio(videos: list[dict]) -> float:
    views_ratio = 0
    count_videos = 0

    for video in videos:
        if video['views'] > 0:
            views_ratio += video['likes'] / video['views']
            count_videos += 1

    return views_ratio / count_videos


def filter_popular_videos(videos: list[dict]) -> list[dict]:
    return [video for video in videos if video["views"] > 1_000_000 and video["likes"]> 500_000]


def top_videos_by_category(videos: list[dict], categories: list[str]) -> dict[str, list[dict]] | None:
    category_vid = {}
    
    for video in videos:
        if video["category"] in categories:
            if video["category"] not in category_vid:
                category_vid[video["category"]] = []
            category_vid[video["category"]].append(video)
    
    for category in category_vid:
        category_vid[category].sort(key=lambda x: x['views'], reverse=True)
        category_vid[category] = category_vid[category][:3]

    return category_vid

def avg_comments_popular_videos(videos: list[dict]) -> float:
    videos_total = filter_popular_videos(videos)
    comments_total = sum(video["comment_count"] for video in videos_total)
    return comments_total / len(videos_total)


def video_filter_generator(videos) -> Iterator[tuple[str, int]]:
    for video in videos:
        if video["comment_count"] > 450_000:
            yield video["title"], video["views"]


if __name__ == "__main__":
    data = load_data(os.path.join(os.path.dirname(__file__), '..', 'data', 'videos-stats.csv'))

    # Task 1.1 Write a function that returns the video with the highest number of views.
    highest_viewed_video = video_with_highest_views(data)
    print(f"Video with the highest views: {highest_viewed_video}")

    # Task 1.2 Calculate the average likes-to-views ratio across all videos.
    avg_ratio = average_likes_to_views_ratio(data)
    print(f"Average likes-to-views ratio: {avg_ratio:.4f}")

    # Task 1.3 Filter and return a list of videos with views greater than 1,000,000 and likes greater than 500,000.
    popular_videos = filter_popular_videos(data)
    print("Popular videos:", len(popular_videos))

    # Task 1.4 Group videos by category and return the top 3 on each category with views number.
    top_videos = top_videos_by_category(data, categories=['gaming', 'tech', 'crypto'])
    for category, vids in top_videos.items():
        print(f"Category: {category}")
        for video in vids:
            print(f"  Title: {video['title']}, Views: {video['views']}")

    # Task 1.5 Find the average number of comments per video for videos with views greater than 1,000,000 and likes greater than 500,000.
    avg_comments = avg_comments_popular_videos(data)
    print("Average comments for popular videos:", avg_comments)

    # Task 1.6 Write a generator that yields videos with comment count greater than 450,000 (must return title and comment count)
    filtered_videos = video_filter_generator(data)
    for title, views in filtered_videos:
        print(f"{title}: {views}")
