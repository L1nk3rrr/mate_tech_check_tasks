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
    res_data = sorted(videos, key=lambda x: x["views"], reverse=True)
    return res_data[0]['title']


def average_likes_to_views_ratio(videos: list[dict]) -> float:
    total_sum = 0
    counter = 0
    for el in videos:
        if el.get('views') != 0:
            total_sum += el.get('likes') / el.get('views')
            counter += 1
    return total_sum / counter


def filter_popular_videos(videos: list[dict]) -> list[dict]:
    res = []
    for el in videos:
        if el['views'] > 1_000_000 and el['likes'] > 500_000:
            res.append(el)
    return res
    ### також можна зробити красиво:
    #return [el for el in videos if el['views'] > 1_000_000 and el['likes'] > 500_000]


def top_videos_by_category(videos: list[dict], categories: list[str]) -> dict[str, list[dict]] | None:
    resulted_cat = {}
    for cat in categories:
        category = [el for el in videos if el["category"] == cat]
        resulted_cat[cat] = sorted(category, key=lambda x: x["views"], reverse=True)[:3]
    return resulted_cat


def avg_comments_popular_videos(videos: list[dict]) -> float:
    popular = filter_popular_videos(videos)
    return sum([video["comment_count"] for video in popular]) / len(popular)


def video_filter_generator(videos) -> Iterator[tuple[str, int]]:
    for el in videos:
        if el['comment_count'] > 450_000:
            yield el["title"], el["views"]
    ### інший варіант створення генератора через вираз, але нащо тоді для цього окрема функція...
    #return ((el["title"], el["views"]) for el in videos if el['comment_count'] > 450_000)


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

    # Task 1.6 Write a generator that yields with comments count greater than 450,000
    filtered_videos = video_filter_generator(data)
    for title, views in filtered_videos:
        print(f"{title}: {views}")
