# Checking if a title has brackets
def iscomplete(stream):
    if check_title.search(stream.title):
        print(re.search(r"^\[([A-Za-z0-9_]+)\]",submissions.title))