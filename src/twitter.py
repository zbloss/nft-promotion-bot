import tweepy


class TwitterAPI:

    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):

        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth)


    def post_tweet(self, tweet: str):
        '''
        Posts the given message to twitter as a tweet.
        
        '''
        
        response = self.api.update_status(tweet)
        return response
