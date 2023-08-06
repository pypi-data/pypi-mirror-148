import numpy as np

import covidTTI.utils as utils

def calculate_R_0(model):
    '''
    Calculates what the R number would be without any
    interventions or isolating.

    This is the equivalent of the base Reproduction Number, or R0
    '''

    n_cases = len(model.cases)

    # count number of infected secondary cases
    infected_contacts = [c for c in model.contacts if c.has_covid]
    n_infected = len(infected_contacts)

    # R number is the average number of people that an
    # index case infects
    R_0 = n_infected/n_cases

    return R_0

def calculate_R_eff(model):
    '''
    Calculates the R number after interventions and isolating.

    This is equiavelent to the effective Reproduction number
    '''
    infections_post_intervention = len([c for c in model.contacts if ((not c.isolated) and (c.has_covid))])

    fractional_R = calculate_infections_stopped(model)

    R_eff = (infections_post_intervention + fractional_R)/len(model.cases)

    return R_eff

def calculate_infections_stopped(model):
    '''
    Calculate what proportion of onward infection was prevented
    by isolation
    '''

    onward_transmission = 0
    for c in model.contacts:
        if c.isolated and c.has_covid:
            # calculate the amount of onward transmission
            # from the day the contact isolate
            # TODO: this should be cumsum (i.e CDF of viral load)
            if c.day_isolated == 0:
                cum_transmission = 0
            else:
                cum_transmission = np.cumsum(model.infectious_period[:int(c.day_isolated)])[-1]
            onward_transmission += cum_transmission

    transmission_per_contact = onward_transmission
    
    return transmission_per_contact
