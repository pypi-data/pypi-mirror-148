from typing import List, Iterable, Union
import random


def generate_password(sources: List[str], length: int) -> str:
    if len(sources) > length:
        raise ValueError("Too many required sources or length is too short")
    password = ""
    while len(password) < length:
        for source in sources:
            password = password + random.choice(source)
        random.shuffle(sources)
    return password
