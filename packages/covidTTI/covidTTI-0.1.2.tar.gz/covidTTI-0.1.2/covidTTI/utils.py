import yaml
from scipy.stats import gamma, nbinom, lognorm
import numpy as np

def init_seed(random_seed = 1):
    """Function that generates a numpy random number generator given a seed

    :param random_seed: seed, defaults to 1
    :type random_seed: int, optional
    :return: The numpy random number generator
    :rtype: Numpy random number generator
    """
    return np.random.default_rng(seed = random_seed)


def load_config(fpath):
    """Function that loads the config yaml file

    :param fpath: Full file and path of the config file
    :type fpath: string
    :return: configuration setting
    :rtype: Dictionary
    """    

    with open(fpath, 'r') as f:
        config = yaml.safe_load(f)

    return config

def bernoulli(p, rng):
    """Function that draws from a bernoulli distribution with probability p

    :param p: probability the trial was successful
    :type p: float
    :param rng: random number generator
    :type rng: 
    :return: Whether the trial was successful or not
    :rtype: bool
    """   
    return rng.uniform() < p

def draw_from_pdf(rng, pdf, size = 1):

    result = np.argmax(rng.multinomial(1, pdf, size = size), axis = - 1)
    if size == 1:
        return result[0]
    else:
        return result

def calc_incubation_period(period, shape = 4.23, scale = 1/0.81):
    '''
    Draw from the incubation period - defined as the time
    from infection to symptom onset
    '''

    # calculate daily incubation period
    days = np.arange(period)
    incubation_period = gamma.pdf(days + 1, a = shape, scale = scale)

    incubation_period = incubation_period / sum(incubation_period)

    return incubation_period

def calc_exposed_to_infectious(period):

    days = np.arange(period)

    exposed_to_infectious = lognorm.pdf(days + 1, s = 1.5, scale = np.exp(4.5))

    return exposed_to_infectious / sum(exposed_to_infectious)

def calc_infectious_dist(period):

    days = np.arange(period)

    viral_load = nbinom.pdf(days + 1, n = 1, p = 0.45)
    return viral_load/np.sum(viral_load)

