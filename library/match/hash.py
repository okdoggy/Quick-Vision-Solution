import imagehash
from PIL import Image
import numpy as np


def compare_hash(image, ref):
    image1 = Image.fromarray(np.uint8(image))
    image2 = Image.fromarray(np.uint8(ref))

    hash1 = imagehash.dhash(image1)
    hash2 = imagehash.dhash(image2)

    return (hash1 - hash2)  # hamming distance
