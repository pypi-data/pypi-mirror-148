import uuid
import numpy as np

from covidTTI.contacts import Contact
from covidTTI.cases import indexCase
import covidTTI.utils as utils

class TTIModel():

    def __init__(
        self, 
        parameters
        ):

        self.parameters = parameters
        self.n_cases = self.parameters['pop_params']['prevalence']
        self.init_params()
        self.init_cases()
        self.init_contacts()

    def init_params(self):

        self.incubation_period = utils.calc_incubation_period(
            self.parameters['epi_params']['max_infectious_day']
        )
        self.infectious_period = utils.calc_incubation_period(
            self.parameters['epi_params']['max_infectious_day']
        )

        self.exposed_to_infectious = utils.calc_exposed_to_infectious(
            self.parameters['epi_params']['max_infectious_day']
        )

    def init_cases(self):
        '''
        Initialise a list of cases simulated using the indexCase
        class
        '''

        cases = []
        for n in range(self.n_cases):
            cases.append(indexCase(self.parameters, self.incubation_period))

        self.cases = cases

    def init_contacts(self):
        '''
        Initialise secondary contacts for each indexCase
        '''

        secondary_contacts = []
        for case in self.cases:
            for n in range(case.n_household):
                secondary_contacts.append(
                    Contact(case,
                    self.infectious_period,
                    self.incubation_period,
                    is_household = True
                    )
                )
            for n in range(case.n_other):
                secondary_contacts.append(
                    Contact(case,
                    self.infectious_period,
                    self.incubation_period,
                    is_household = False
                    )
                )

        self.contacts = secondary_contacts



        


