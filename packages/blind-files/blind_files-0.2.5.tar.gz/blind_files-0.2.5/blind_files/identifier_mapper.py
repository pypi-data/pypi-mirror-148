from hashlib import blake2b
from itertools import product
from pkgutil import get_data


def load_noun_list():
    data = get_data("blind_files", "data/nounlist.txt")

    if data is None:
        raise Exception("Couldn't find noun list")

    return [line.strip() for line in data.decode("utf-8").splitlines()]

class IdentifierMapper:
    def __init__(self, key):
        self.key = key
        nouns = load_noun_list()[:4096]
        self.noun_pairs = list(product(nouns, repeat=2))

    def __call__(self, identifier):
        hash_value = blake2b(
            identifier.encode('utf-8'),
            digest_size=3,
            key=self.key.encode(),
        ).digest()
        index = int.from_bytes(hash_value, byteorder='big')
        noun_pair = self.noun_pairs[index]
        return '_'.join(noun_pair)
