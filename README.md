# ElonBot
**Final Output: Discord Bot**

*Introduction to Big Data | CPE 32 | Team Poopoo*

*Project Lead: Eduard Naldoza*

*Programmers: Eduard Naldoza, Steve Ibañez, Miguel Villanueva*

A Discord Bot that lets you stalk on a specific Twitter account that can notify you when a new tweet about a specific keyword is posted at any time of day every five minutes on any of your Discord servers.
This program primarily uses the *discord.py* and *tweepy* libraries and *Flask* for the http portion of the program. **Replit** is used to host the program, and  **UptimeRobot** is used to keep the bot running 24/7. 
 
  


## How to use:
1. First, use the command **"eb stalk"** and input a Twitter username after the command. 
	
	*(Enter only the twitter handle, refrain from using the **"@"** symbol.)*
2. Use the **"eb addkey"** command alongside with the keywords you wanted to search for one by one.

	*(Note: If you want to delete a keyword just type the command **"eb delkey"** with the keyword to be deleted.)*
3. If you are ready to monitor, you can now enter the command **"eb start"**. To stop the bot, enter the command **"eb stop"**


### ElonBot Commands:

  Type "**eb stalk** *[Twitter Handle]*" to select a Twitter account to get tweets from.

  Type "**eb stalking**" check which Twitter account is currently being monitored.

  Type "**eb addkey** *[keyword]*" to add a keyword to look for in account's tweets.

  Type "**eb delkey** *[keyword]*" to remove a keyword.

  Type "**eb check"** to manually tell ElonBot to check for new tweets.

  Type "**eb start**" to make ElonBot start searching

  Type "**eb stop"** to stop ElonBot from updating.

  Type "**eb clearkey"** to clear the keywords listed.

### Notes:


-	If you initiated the command **"eb check"**, **"eb start"**, **"eb stop"**, before entering a **"eb stalk"** command, the bot will ask you to put an account first.

-	To change the user to be stalked, you can put the "**eb stalk"** command together with the new twitter account.

-	To clear the keywords listed, do the "**eb clearkey**" command.
