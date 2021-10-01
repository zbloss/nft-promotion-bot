import hydra
import shutil
import tweepy
import random
import logging
import requests
from omegaconf import DictConfig, OmegaConf
from opensea import OpenseaAPI

def get_asset_metadata(asset: dict):
    name = asset['name']
    description = asset['description'].replace(name, '')
    description = ' '.join(description.split())
    permalink = asset['permalink']
    asset_contract_address = asset['asset_contract']['address']
    current_price = float(asset['sell_orders'][0]['current_price']) / 1000000000000000000
    current_price = round(current_price, 4)
    image_url = asset['image_url']
    return {
        'name': name,
        'description': description,
        'permalink': permalink,
        'asset_contract_address': asset_contract_address,
        'current_price': current_price,
        'image_url': image_url
    }

def download_asset_image(image_url: str, filename: str = 'sample_image.png'):
    response = requests.get(image_url, stream = True)
    # Check if the image was retrieved successfully
    if response.status_code == 200:
        response.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
            f.close()
        return filename
    else:
        return None

def build_tweet(asset_metadata: dict, hashtags: str) -> str:

    tweet = '{name}: {current_price}Ξ\n{permalink}\n{hashtags}'.format(
        name=asset_metadata['name'],
        current_price=asset_metadata['current_price'],
        asset_contract_address=asset_metadata['asset_contract_address'],
        permalink=asset_metadata['permalink'],
        hashtags=hashtags
    )
    return tweet

@hydra.main(config_path="../configs", config_name="base_config")
def post_tweet(cfg: DictConfig) -> None:
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    try:
        secrets = OmegaConf.load(cfg.twitter.path_to_secrets)
        api_key = secrets['twitter']['api_key']
        api_secret = secrets['twitter']['api_secret']
        access_token = secrets['twitter']['access_token']
        access_token_secret = secrets['twitter']['access_token_secret']
        logger.info('secrets loaded')

    except FileNotFoundError:
        logger.warn('secrets.yaml not found, attempting to load from environment variables.')
        import os
        api_key = os.getenv('api_key')
        api_secret = os.getenv('api_secret')
        access_token = os.getenv('access_token')
        access_token_secret = os.getenv('access_token_secret')
        logger.info('secrets loaded from environment variables')

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    logger.info('twitter client authenticated')

    opensea = OpenseaAPI(asset_owner=cfg.opensea.asset_owner)
    assets = opensea.get_assets(collection=cfg.opensea.collection)
    logger.info('assets loaded')

    number_of_assets = len(assets)
    random_asset_index = random.randint(0, number_of_assets)
    asset = assets[random_asset_index]
    asset_metadata = get_asset_metadata(asset)
    logger.info('asset metadata extracted')

    image_filename = download_asset_image(asset_metadata['image_url'])
    if image_filename is not None:
        logger.info('asset image downloaded')
    else:
        logger.error('unable to download asset image')
        raise Exception('Error downloading the asset image')

    media = api.media_upload(image_filename)
    logger.info('asset iamge uploaded to twitter media')

    message = build_tweet(asset_metadata, cfg.twitter.hashtags)
    api.update_status(message, media_ids=[media.media_id])
    logger.info('tweet posted')



if __name__ == "__main__":
    post_tweet()