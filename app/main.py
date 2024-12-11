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


def video_with_highest_views(videos: list[dict]) -> str:
    return max(videos, key=lambda video: video['views'])['title']
#  знайшов лекший варіант + основна проблема що треба писати з маленької перегляди та тайтл)))))))

# ration = likes / views for 1 video!
# average ratio it's sum of all rations / count of videos
def average_likes_to_views_ratio(videos: list[dict]) -> float:
    total = 0
    total_vid = 0
    for video in videos:
        if video['views'] > 0:
            total += video['likes'] / video['views']
            total_vid += 1
    return total / total_vid if total_vid > 0 else 0
#  тут я на тех-чеку не зрозумів самого завдання тут треба знайти сер співідношення для відео ДЕ Є ПЕРЕГЛЯДИ

def filter_popular_videos(videos: list[dict]) -> list[dict]:
    result = []
    for video in videos:
        if video['views'] > 1000_000 and video['likes'] >= 500_000:
            result.append(video)
    return result
#  тут основна проблема була як і в першому Views i Likes з маленької)

def top_videos_by_category(videos: list[dict], categories: list[str]) -> dict[str, list[dict]] | None:
    sort_by_category = {}
    for video in videos:
        if video['category'] in categories:
            if video['category'] not in sort_by_category:
                sort_by_category[video['category']] = []
            sort_by_category[video['category']].append(video)
    #  спочатку групуєм відоси по категоріям

    top_videos_by_category = {}
    for category, category_videos  in sort_by_category.items():
        sorted_videos = sorted(category_videos, key=lambda x: x['views'], reverse=True)
        top_videos_by_category[category] = sorted_videos[:3]
    return top_videos_by_category
    #  потім сортуєм у кожній категорії та вибераєм перші три (це найбільші)
    #  тому, що ключ за сортуванням: key=lambda x: x['views']

def avg_comments_popular_videos(videos: list[dict]) -> float:
    cool_video = [video for video in videos if video['views'] >= 1000_000 and video['likes'] >= 500_000]
    sum_comments = sum(video['comment_count'] for video in cool_video)
    avg_comments = sum_comments / len(cool_video)
    return avg_comments

def video_filter_generator(videos: list[dict]) -> Iterator[tuple[str, int]]:
    for vi in videos:
        if vi['comment_count'] > 450_000:
            yield vi['title'], vi['comment_count']


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

    # Task 1.6 Write a generator that yields videos with comment count greater than 450,000 (must return title and views)
    filtered_videos = video_filter_generator(data)
    for title, views in filtered_videos:
        print(f"{title}: {views}")
