# listening to stream for subreddit
def poststream():
    for submissions in reddit.subreddit("RidersChallengeTest").stream.submissions(skip_existing=True):
        iscomplete(submissions)