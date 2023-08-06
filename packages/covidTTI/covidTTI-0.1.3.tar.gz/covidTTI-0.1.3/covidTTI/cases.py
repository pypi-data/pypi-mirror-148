import numpy as np

import covidTTI.utils as utils

class indexCase():

    def __init__(
        self,
        parameters,
        incubation_period,
        random_seed = 1
        ):

        self.parameters = parameters
        self.rng = utils.init_seed(random_seed = random_seed)
        self.incubation_period = incubation_period
        self.init_case()
        self.draw_contacts()
        self.report_contacts()

    def init_case(self):

        # is symptomatic?
        self.symptomatic = utils.bernoulli(
            self.parameters['epi_params']['p_symp'], 
            self.rng
            )
        # how long in days infectious
        self.infectious_length = self.parameters['epi_params']['max_infectious_day']

        # when symptoms occur
        if self.symptomatic:
            self.day_symptom_onset = utils.draw_from_pdf(
                self.rng,
                self.incubation_period
                )
        else:
            self.day_symptom_onset = np.nan

    def draw_contacts(self):

        # number of household contacts
        # it is assumed that these contacts are come
        # into contact every day
        self.n_household = self.rng.choice(
            a = list(self.parameters['contact_params']['household_dict'].keys()), 
            p = list(self.parameters['contact_params']['household_dict'].values()), 
            size = 1
        )[0]

        # number of non-household contacts
        # it is multiplied by the length of the infectious
        # period
        n_household = 0
        for day in range(self.infectious_length):
            n_household += np.round(
                self.rng.poisson(lam = self.parameters['contact_params']['n_contacts'])
            )

        self.n_other = n_household

    def report_contacts(self):

        # does the cases supply contacts?
        # assume that contacts are only reported if the case is symptomatic
        if self.symptomatic:
            self.enters_contacts = utils.bernoulli(
                self.parameters['trace_params']['p_contacts_entered'],
                self.rng
            )
            # day contacts entered after infection
            # assume that it is a maximum of 5 days
            #  after symptomatic onset
            self.day_contacts_entered = \
                utils.draw_from_pdf(self.rng, self.incubation_period) + \
                    self.rng.integers(0, 5)
        else:
            self.enters_contacts = False 
            self.day_contacts_entered = np.nan
        


