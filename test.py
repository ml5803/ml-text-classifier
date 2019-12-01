from __future__ import absolute_import, print_function

import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="o36wOsmM0BDtgjNEXmYl8Wy3d"
consumer_secret="5p086UZ99tDkD3hdO1TlPt7uWBAzKlsG0Bqca5ftEqYPBq0p1k"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="995028642995503105-J0GbXi4NoEJQnVMmhfaz2O30aoXfMuI"
access_token_secret="VeKGnjVLMv2p6lviReMpFwRdx9eDRX6I3g1qASbxsDbCq"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print(api.me().name)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

tl = api.user_timeline("PenguMike")
for item in tl:
    print(item.text)
