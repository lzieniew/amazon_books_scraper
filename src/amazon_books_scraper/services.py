

def get_first_n_words(input: str, n: int) -> str:
    return ' '.join(input.split()[:n])


def strip_author_string(author: str):
    author = author.replace('Written by:', '')
    author = author.replace('Art by:', '')
    return get_first_n_words(author, 2)
