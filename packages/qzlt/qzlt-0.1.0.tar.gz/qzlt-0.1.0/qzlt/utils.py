import random
from typing import List, Any


def sample(n: int, array: List[Any]) -> List[Any]:
    """
    Randomly samples `n` elements from an array

    :param n: Number of samples to be taken
    :param array: Array of elements
    :returns: Array of sampled elements
    """
    array_ = [*array]
    random.shuffle(array_)
    return [*array_[0:n]]
