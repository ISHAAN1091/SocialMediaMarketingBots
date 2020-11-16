import tweepy


# Authenticate to Twitter
auth = tweepy.OAuthHandler("QqSrJM6GHjN69XYcWarQeosXA", "P5mNstvvRXOzXCgig3d4BeubP62llscsHFczVEK92nidMUtXVb")
auth.set_access_token("1261330204116557824-q1L5td0zbzx9QvgYQAKxwZcYbpVtJ9", "QKu2zwVLMYILsYL7RDFZIOpFO3t2ZvT1sgnAybVoDVNMq")


# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


# Posting tweet
try:
    api.update_status("Test tweet from Tweepy Python1")
    print("status updated")
except Exception as e:
    print("error",e)