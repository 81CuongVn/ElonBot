# ElonBot
**Final Output: Discord Bot**

*Introduction to Big Data | CPE 32 | Team Poopoo*

*Project Lead: Eduard Naldoza*

*Programmers: Eduard Naldoza, Steve Ibañez, Miguel Villanueva*

A Discord Bot that lets you stalk on a specific Twitter account that can notify you when a new tweet about a specific keyword is posted at any time of day every five minutes on any of your Discord servers.
This program primarily uses the *discord.py* and *tweepy* libraries and **Flask** for the http portion of the program. *Replit* is used to host the program, and  **UptimeRobot** is used to keep the bot running 24/7. 

### ElonBot Commands:

  Type "**$stalk** *[Twitter Handle]*" to select a Twitter account to get tweets from.

   Type "**$addkey** *[keyword]*" to add a keyword to look for in account's tweets.

  Type "**$delkey** *[keyword]*" to remove a keyword.

  Type "**$check"** to start searching.

  Type "**$change** *[Twitter handle]*" change the Twitter account to get tweets from.

  Type "**$shutup"** to shut ElonBot up.

  Type "**$clearkey"** to clear the keywords listed.



## How to use:
1. First, use the command **"$stalk"** and input a Twitter username after the command. 
	
	*(Refrain from using the **"@"** symbol.)*
2. Use the **"$addkey"** command alongside with the keywords you wanted to search for one by one.

	*(Note: If you want to delete a keyword just type the command **"$delkey"** with the keyword to be deleted.)*
3. If you are ready to search, you can now enter the command **"$check"**.




### Notes:


-	If you initiated the command **"check"** before entering a **"stalk"** command, the bot will ask you to put an account first.

-	To change the user to be stalked, you can put the "**$change"** command together with the new twitter account.

-	To clear the keywords listed, do the "**$clearkey**" command.

-	To terminate the bot, you can iput the "**$shutup**" command.