import tweepy
import os
import sys
import tempfile
from pdf2image import convert_from_path



def pdf_to_png(source,destino):

    print(f"Converting {source}to {destino}")
    convert_from_path(pdf_path=source,
    dpi=100,
    output_folder=destino,
    fmt="png",
    output_file="fax.png",
    single_file=True)


def init_api():

    consumer_key = os.getenv('FAX2TWEET_CONSUMER_KEY')
    consumer_secret = os.getenv('FAX2TWEET_CONSUMER_SECRET')
    access_token = os.getenv('FAX2TWEET_ACCESS_TOKEN')
    access_token_secret= os.getenv('FAX2TWEET_ACCESS_TOKEN_SECRET')

    if consumer_key is None or consumer_secret is None or access_token is None or access_token_secret is None:
        print("Twitter creds were incorrect, exiting")
        print_usage()

    print("Initializing API")
    twitter_auth_keys = {
        "consumer_key"        : consumer_key,
        "consumer_secret"     : consumer_secret,
        "access_token"        : access_token,
        "access_token_secret" : access_token_secret
    }

    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)

    return api


def send_tweet(api, txt, img_path):

    print(f"Generating media object from {img_path}")
    media = api.media_upload(img_path)

    print(f"Setting Tweet text to \"{txt}\"")
    tweet = txt

    print(f"Posting Tweet")
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])


def print_usage():
    print("Gets the first page of a PDF and tweets it")
    print("")
    print("Twitter API Credentials are supplied as env vars:")
    print("FAX2TWEET_CONSUMER_KEY")
    print("FAX2TWEET_CONSUMER_SECRET")
    print("FAX2TWEET_ACCESS_TOKEN")
    print("FAX2TWEET_ACCESS_TOKEN_SECRET")
    print("")
    print("Usage:")
    print("'fax2tweet.py [PATH TO PDF] [TEXT TO TWEET]")
    print("")
    print("")
    sys.exit()

def main():

    if len(sys.argv) < 2:
        print("pdf_path and tweet_text arguments are required")
        print_usage()

    pdf_path = sys.argv[1]
    tweet_text = sys.argv[2]

    if pdf_path is None or tweet_text is None:
        print("pdf_path or tweet_text was None")
        print_usage()

    print(f"Starting fax2tweet")

    api = init_api()

    with tempfile.TemporaryDirectory() as path:

        pdf_to_png(pdf_path, f"{path}")

        send_tweet(api, tweet_text, f"{path}/fax.png")


if __name__ == "__main__":
    main()
