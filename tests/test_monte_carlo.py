from random import random
import numpy
from app.utils import monte_carlo 

"""
In order to test a pseudo-random number generator we can specify the seed it uses
this means that it will always produce the same random numbers in the same order
""" 
numpy.random.seed(1)

def test_log_normal_dist_one_sample():
    random_value = monte_carlo.log_normal_dist(5, 2, 1)[0]
    assert round(random_value, 8) == 8.67991825

def test_normal_dist_one_sample():
    random_value = monte_carlo.normal_dist(5, 2, 1)[0]
    assert round(random_value, 8) == 3.77648717

def test_log_normal_dist_array():
    rand_array = monte_carlo.log_normal_dist(5, 2, 5)
    assert list(rand_array) == [3.7876586885566463,3.0705704132672627,6.479406667748254,1.9127707219396068,9.092247918411717]

def test_normal_dist_array():
    rand_array = monte_carlo.normal_dist(5, 2, 5)
    assert list(rand_array) == [3.4775861982097944,5.638078192114197,4.50125924904518,7.924215874089948,0.8797185810046919]