import json
import hydra
import shutil
import tweepy
import random
import logging
import requests
from omegaconf import DictConfig
from opensea import OpenseaAPI


@hydra.main(config_path="../configs", config_name="base_config")
def find_buyers(cfg: DictConfig) -> None:
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)
 
    api_key = cfg.twitter.api_key
    api_secret = cfg.twitter.api_secret
    access_token = cfg.twitter.access_token
    access_token_secret = cfg.twitter.access_token_secret

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    logger.info('twitter client authenticated')

    search_results = api.search_tweets(
        q="drop your unsold nft",
        result_type="mixed",
        count=20
    )
    for tweet_number, result in enumerate(search_results):
        tweet_details = result._json
        tweet_id = tweet_details['id_str']
        try:
            api.update_status(
                status=f"https://opensea.io/collection/{cfg.opensea.collection}",
                in_reply_to_status_id=tweet_id,
                auto_populate_reply_metadata=True
            )
            logger.info(f'tweet posted: {tweet_number}')
        except:
            pass

if __name__ == "__main__":
    find_buyers()