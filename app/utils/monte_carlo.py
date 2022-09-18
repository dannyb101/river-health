import numpy as np

"""
Log normal function which takes the desired array size, mean and standard deviation of the log normally distributed river flow data
This then uses algebra to calculate the mean and standard deviation of the underlying normal distribution
These underlying values are then used to create a random log-normal distribution - returning an array of the desired size
"""
def log_normal_dist(log_normal_mean, log_normal_std, size):
    normal_std = np.sqrt(np.log(1 + (log_normal_std/log_normal_mean)**2))
    normal_mean = np.log(log_normal_mean) - normal_std**2 / 2
    random_dist = np.random.lognormal(normal_mean, normal_std, size)

    return random_dist

"""
Normal distribution function takes the mean, standard deviation and desired size of output array
"""
def normal_dist(mean, std, size):
    random_dist = np.random.normal(mean, std, size)

    return random_dist
