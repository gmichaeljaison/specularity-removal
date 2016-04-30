"""
A simple demo file explaining how to use the method to remove highlights in images.
    Resuls are stored in results/ directory
"""

import logging

from specularity_removal import *


# change the log level accordingly
logging.basicConfig(level=logging.DEBUG)

# Example 1
# Images taken in different view points. In the order of alignment
fnames = [
    'data/pshycology-book-1.jpg',
    'data/pshycology-book-2.jpg',
    'data/pshycology-book-3.jpg'
]
remove_specularity(fnames)


# Example 2
# Images taken in different view points. In the order of alignment
fnames = [
    'data/calculus-book-1.jpg',
    'data/calculus-book-2.jpg'
]
remove_specularity(fnames)
