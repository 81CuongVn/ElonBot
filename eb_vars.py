help_msg = """
***ELONBOT COMMANDS:***

    Use **$stalk [Twitter Handle]** to select a Twitter account to get tweets from.

    Use **$addkey [keyword]** to add a keyword to look for in account's tweets.

    Use **$delkey [keyword]** to remove a keyword.

    Use **$clearkey** to remove all your keywords.

    Use **$change [Twitter handle]** to change the Twitter account to get tweets from.

    Use **$shutup** to shut ElonBot up.

Happy Stalking ;)
"""
#$stalk messages
msgStalkNoKey = """Okay, will notify you of {}'s tweets.
*Note: Use $addkey command to add keywords to look out for*"""
msgStalkHasKey = "Okay, will notify you of {}'s tweets."

#$addkey messages
msgAddKeyExists = "Keyword *{}* already in keywords."
msgAddKeyNew = "Keyword *{}* added to keywords."

#$delkey messages
msgDelkeyExists = "Keyword *{}* removed"
msgDelkeyNone = "Keyword *{}* is not in your list of keywords."

#$viewkey messages
msgviewkeyNone = """You haven't entered any keywords yet
*Note: Use $addkey command to add keywords to look out for*"""

keywords = []



