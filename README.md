# /r/RidersChallenge Points Tracker Bot
the /r/RidersChallenge subreddit features a community of motorcycle enthusiasts participating in a sort of always-running treasure hunt for pictures. 

## Goals of the Subreddit
The general process is this: 

1. an active post features a request, i.e., "Show me your bike at your favorite parts store"
2. Another active user will take a picture, upload it, and the title will reflect the completed status
    1. first, the title must include [something something Completed], where "Something Something" is a reference to the previous challenge in a single/few words
    2. second, the title must finish with a new challenge for those who wish to participate in the challenge to complete. 
3. The treasure hunt works on the honor system, as there's no simple way to automate the verification process of photo's being uploaded. 

## Goals of this Tracker Bot
the goals of this tracker bot are as follows:

1. automate the process of adding points 
2. automate the pinning of the current active challenge
3. automate the updates/maintenance of an active leaderboard
4. allow users to modify their flair while maintaining their current point count
5. (eventually) allow for easy resetting of the seasons, parsing each season into a final leaderboard
    1. archive old data
    2. store it in a publicly accessible location that can be accessed by past players

## Development History and Plans
the previous bot that performed this task was created/maintained by /u/slanktapper on reddit, who has recently decided to move on from this task. 

the original bot was created in PHP, using composer as the framework management system. The original code was confusing and hard to follow, and required a higher-level understanding of PHP-based coding to maintain. 

For the sake of ease of maintenance, ease of taking over, and general ease of creating and maintaining this iteration of the bot, it is being rebuilt with Python using [PRAW](https://praw.readthedocs.io/en/stable/) and a SQLITE3 flat-file database. 

As of now, at least unofficially, I am taking over development of the bot, and will be accepting pull requests as deemed appropriate.

## License

The project is to be licensed under the MIT License, detailed further in the LICENSE.md file in the root of this repository.