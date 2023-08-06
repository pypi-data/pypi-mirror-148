# returns the Euclidean distance between two equal size vectors (lists)
from typing import List
from .sqrt import sqrt

def distance(a : List[float], b: List[float]) -> float:
    assert len(a)==len(b), "The input lists are not same size!"

    diff = [(x-y)*(x-y) for x,y in zip(a,b)]
    return sqrt(sum(diff))