import praw
import pandas as pd

def initialize_reddit_client(client_id, client_secret, user_agent):
    """
    Initializes and returns a Reddit client.
    
    Args:
        client_id (str): Your Reddit API client ID.
        client_secret (str): Your Reddit API client secret.
        user_agent (str): A unique user agent string.
        
    Returns:
        praw.Reddit: An authenticated Reddit instance.
    """
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        print("Reddit client initialized successfully.")
        return reddit
    except Exception as e:
        print(f"Error initializing Reddit client: {e}")
        return None

def get_subreddit_comments(reddit, subreddit_name, limit=100):
    """
    Fetches comments from a specified subreddit.
    
    Args:
        reddit (praw.Reddit): An authenticated Reddit instance.
        subreddit_name (str): The name of the subreddit to scrape.
        limit (int): The maximum number of comments to fetch.
        
    Returns:
        pd.DataFrame: A DataFrame containing the comments.
    """
    if not reddit:
        print("Reddit client is not initialized.")
        return pd.DataFrame()
        
    try:
        subreddit = reddit.subreddit(subreddit_name)
        comments_data = []
        print(f"Fetching comments from r/{subreddit_name}...")
        for comment in subreddit.comments(limit=limit):
            comments_data.append({
                'id': comment.id,
                'body': comment.body,
                'created_utc': comment.created_utc,
                'subreddit': subreddit_name
            })
        
        df = pd.DataFrame(comments_data)
        print(f"Successfully fetched {len(df)} comments.")
        return df
    except Exception as e:
        print(f"Error fetching comments from r/{subreddit_name}: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    # --- Replace with your credentials ---
    CLIENT_ID = "YOUR_CLIENT_ID"
    CLIENT_SECRET = "YOUR_CLIENT_SECRET"
    USER_AGENT = "Aspect-Pulse v1.0 by u/your_username"
    # ------------------------------------

    reddit_client = initialize_reddit_client(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    
    if reddit_client:
        # Example: Fetch comments from r/apple
        apple_comments_df = get_subreddit_comments(reddit_client, 'apple', limit=200)
        
        if not apple_comments_df.empty:
            print("\n--- Sample of fetched comments ---")
            print(apple_comments_df.head())
            
            # Save to CSV
            output_path = '../data/reddit_comments_apple.csv'
            apple_comments_df.to_csv(output_path, index=False)
            print(f"\nComments saved to {output_path}")

        # Example: Fetch comments from r/samsung
        samsung_comments_df = get_subreddit_comments(reddit_client, 'samsung', limit=200)

        if not samsung_comments_df.empty:
            print("\n--- Sample of fetched comments ---")
            print(samsung_comments_df.head())

            # Save to CSV
            output_path = '../data/reddit_comments_samsung.csv'
            samsung_comments_df.to_csv(output_path, index=False)
            print(f"\nComments saved to {output_path}")
