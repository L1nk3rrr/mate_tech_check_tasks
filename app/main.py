from typing import Iterator
import datetime

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

data = load_data(os.path.join(os.path.dirname(__file__), '..', 'data', 'videos-stats.csv'))

def video_with_highest_views(videos: list[dict]) -> str:
    # Task 1.1 Write a function that returns the video with the highest number of views.
    max_views = -1
    max_viewed_video_title = ""

    for video in videos:
        if video['views'] > max_views:
            max_views = video['views']
            max_viewed_video_title = video['title']

    return f"Video with the highest views: {max_viewed_video_title}"


# ration = likes / views for 1 video!
# average ratio it's sum of all rations / count of videos
def average_likes_to_views_ratio(videos: list[dict]) -> float:
    # Task 1.2 Calculate the average likes-to-views ratio across all videos.

    total_ratio = 0.0
    video_count = 0

    for video in videos:
        if video['views'] > 0:
            total_ratio += video['likes'] / video['views']
            video_count += 1

    return total_ratio / video_count


def filter_popular_videos(videos: list[dict]) -> list[dict]:
    # Task 1.3 Filter and return a list of videos with views greater than 1,000,000 and likes greater than 500,000.

    popular_videos = []

    for video in videos:
        if video['views'] > 1_000_000 and video['likes'] > 500_000:
            popular_videos.append(video)

    return popular_videos


def top_videos_by_category(videos: list[dict], categories: list[str]) -> dict[str, list[dict]] | None:
    # Task 1.4 Group videos by category and return the top 3 on each category with views number.
    category_groups = {category: [] for category in categories}

    for video in videos:
        category = video.get('category', '').lower()
        if category in category_groups:
            category_groups[category].append(video)

    for category in category_groups:
        category_groups[category].sort(key=video['views'], reverse=True)
        category_groups[category] = category_groups[category][:3]

    return category_groups

def avg_comments_popular_videos(videos: list[dict]) -> float:

    popular_videos = []
    for video in videos:
        if video['views'] > 1_000_000 and video['likes'] > 500_000:
            popular_videos.append(video)

    total_comments = 0
    for video in popular_videos:
        total_comments += video['comment_count']

    return total_comments / len(popular_videos) if popular_videos else 0.0


def video_filter_generator(videos: list[dict]) -> Iterator[tuple[str, int]]:
    # Task 1.6 Write a generator that yields videos with comment count greater than 450,000 (must return title and views)
    for video in videos:
        if video['comment_count'] > 450_000:
            yield video['title'], video['views']


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
