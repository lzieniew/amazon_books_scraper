
def strip_author_string(author: str):
    author = author.replace('Written by:', '')
    author = author.replace('Art by:', '')
    return author
