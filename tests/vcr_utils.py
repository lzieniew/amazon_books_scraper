import os

import vcr


class DontUseCassettes:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def get_cassettes_by_names(names):
    if os.getenv('ONLY_REAL_REQUESTS'):
        return [DontUseCassettes()]
    result = []
    for name in names:
        result.append(vcr.use_cassette(name))
    if os.getenv('REAL_REQUESTS'):
        result.append(DontUseCassettes())
    return result
