# What is it?
This bot was created for company called 'Eko Expert', in this repository you can find 2 scripts of bots, and this bots work together.

First bot is Admin part (admin.py)

What you can do with it:
1. You can add questions and answers and select section of this questions, after that add to database, further it will be used in client part (client.py)
2. You can clear your database (if you have premission for that)
3. See all database in json format

plusees of my code:
1. You can add people, who can use this bot.
2. Own database on redis.
3. A lots of keyboards, you must write only questions and answers.
3. You can't get fault(only if you really want fault), because i always have checks for valid or invalid arguments.
4. 'Beautiful' code.

Main part is Client part (client.py)

What it can do:
1. You can see 5 default selections, in all selections some questions and answers about how this company works.
2. If you don't find question, you can ask specialist, after that this message will be forward to chat.

plusees of my code:
1. There are keyboards for all functions (except asking specialist).
2. You can't get fault(only if you really want fault :-) ), because i always have checks for valid or invalid arguments.
3. This bot ALWAYS have valid database, because after all movements in this bot, databse is refreshes.
4. Same database with admin part (Redis)
