import numpy as np

import covidTTI.utils as utils

class Contact():

    def __init__(
        self, 
        case,
        infectious_period,
        incubation_period,
        is_household = True
        ):

        self.index_case = case
        self.is_household = is_household
        self.parameters = case.parameters
        self.incubation_period = incubation_period
        self.infectious_period = infectious_period
        self.rng = case.rng

        # draw uniformly from the infectious length
        # to get the day that the individual came into
        # contact with the index case
        self.day_exposed = self.rng.integers(
            low = 0, 
            high = self.parameters['epi_params']['max_infectious_day']
        )

        self.infect()
        self.trace()
        self.test()
        self.isolate()

    def infect(self):
        '''
        Calculates whether or not the contact has covid
        '''

        if self.index_case.symptomatic:
            infection_scale = 1
        else:
            infection_scale = self.parameters['epi_params']['asymp_factor']

        # if a member of the household
        if self.is_household:
            self.has_covid = utils.bernoulli(
                infection_scale * self.parameters['epi_params']['sar']['household'],
                self.rng
                )
            if self.has_covid:
                # day infected is sample from the infection profile
                self.day_infected = utils.draw_from_pdf(self.rng, self.infectious_period)
            else:
                self.day_infected = np.nan
        # if not a member of the household, then
        # the probability the contact has covid is a function of 
        # the day they came into contact, and of the infectiosness
        # distribution
        else:
            viral_load = self.infectious_period[self.day_exposed]
            self.has_covid = utils.bernoulli(
                viral_load * infection_scale * self.parameters['epi_params']['sar']['other'] * self.parameters['epi_params']['max_infectious_day'],
                self.rng
                )
            
            if self.has_covid:
                self.day_infected = self.day_exposed
            else:
                self.day_infected = np.nan  

        # establish whether case is symptomatic or not
        if self.has_covid:
            self.symptomatic = utils.bernoulli(
                self.parameters['epi_params']['p_symp'],
                self.rng
            )
            if self.symptomatic:
                self.day_symptomatic = utils.draw_from_pdf(
                    self.rng, self.incubation_period
                    )
            else:
                self.day_symptomatic = np.nan
        else:
            self.symptomatic = False 
            self.day_symptomatic = np.nan     

    def trace(self):
        '''
        Calculate whether the contact was traced or not
        '''

        # if the index case enters contacts, then establish whether
        # contact was successfull contacted and when
        if self.index_case.enters_contacts and self.has_covid:
            # if contact is a household member
            # assume tracing is successful
            # and contact is traced on same day as contacts entered
            if self.is_household:
                self.traced = True
                self.day_traced = self.index_case.day_contacts_entered
            else:
                self.traced = utils.bernoulli(
                    self.parameters['trace_params']['p_traced'],
                    self.rng
                )
                # assume tracing occurs a maximum of 3 days after contacts
                # were entered by the index case
                # TODO: change this to a data-driven approach
                if self.traced:
                    self.day_traced = self.index_case.day_contacts_entered + \
                        self.rng.integers(1, 3)
                else:
                    self.day_traced = np.nan
                
        else:
            self.traced = False
            self.day_traced = np.nan

    def test(self):
        '''
        Calculate whether (and when) the contact was tested
        '''
        
        # is testing done on symptoms?
        if self.symptomatic:
            test_on_symptoms = utils.bernoulli(
                self.parameters['test_params']['p_symp_test'],
                self.rng
            )
            if test_on_symptoms:
                # day tested is a maximum of 3 days after symptom onset
                # TODO: inform the testing date using data
                day_test_on_symptoms = self.day_symptomatic \
                     + self.rng.integers(1, 3)
                
        else:
            test_on_symptoms = False
        
        if not test_on_symptoms:
            day_test_on_symptoms = np.nan

        # is testing done on tracing?
        if self.traced and self.has_covid:
            test_on_tracing = utils.bernoulli(
                self.parameters['test_params']['p_trace_test'],
                self.rng
            )
            if test_on_tracing:
                # is done after the index case has been contacted
                # plus the number of days in communicating result
                # plus the number of days it takes for an individual to test
                # TODO: drive this result with data
                day_test_on_tracing = self.index_case.day_contacts_entered \
                    + self.rng.random.rand_int(1,5)
            else:
                day_test_on_tracing = np.nan
        else:
            test_on_tracing = False
            day_test_on_tracing = np.nan

        # is random asymptomatic (i.e. mass testing) done?
        if self.has_covid:
            test_on_mass = utils.bernoulli(
                self.parameters['test_params']['p_mass_test'],
                self.rng
            )
            
            if test_on_mass:
                # day tested on mass is drawn from a uniform distribution
                # covering the infectious period
                day_test_on_mass = self.rng.integers(1, 14)
            else:
                day_test_on_mass = np.nan
        else:
            test_on_mass = False
            day_test_on_mass = np.nan

        # contact is tested whether any of the above are true
        if test_on_symptoms or test_on_mass or test_on_tracing:
            self.tested = True
            self.day_tested = np.nanmin([
                day_test_on_symptoms, 
                day_test_on_tracing, 
                day_test_on_mass
                ])
            
        else:
            self.tested = False
            self.day_tested = np.nan

    def isolate(self):
        '''
        Calculate whether (and when) the contact isolated
        '''

        # isolate on symptoms
        if self.symptomatic:
            isolate_on_symptoms = utils.bernoulli(
                self.parameters['isolate_params']['p_symp_isolate'],
                self.rng
            )
            if isolate_on_symptoms:
                # assume isolates on symptom onset
                day_isolate_on_symptoms = self.day_symptomatic
            else:
                day_isolate_on_symptoms = False
        else:
            isolate_on_symptoms = False
            day_isolate_on_symptoms = np.nan


        # isolate on trace
        if self.traced:
            isolate_on_trace = utils.bernoulli(
                self.parameters['isolate_params']['p_trace_isolate'],
                self.rng
                )
            if isolate_on_trace:
                day_isolate_on_trace = self.day_traced
            else:
                day_isolate_on_trace = np.nan

        else:
            isolate_on_trace = False
            day_isolate_on_trace = np.nan

        # isolate on test
        if self.tested:
            isolate_on_test = utils.bernoulli(
                self.parameters['isolate_params']['p_test_isolate'],
                self.rng
            )
            if isolate_on_test:
                # TODO: change to day test result communicated
                day_isolate_on_test = self.day_tested
            else:
                day_isolate_on_test = np.nan
            
        else:
            isolate_on_test = False
            day_isolate_on_test = np.nan

        if isolate_on_symptoms or isolate_on_test or isolate_on_trace:
            self.isolated = True
            self.day_isolated = np.nanmin([
                day_isolate_on_test,
                day_isolate_on_symptoms,
                day_isolate_on_trace
            ])
        else:
            self.isolated = False
            self.day_isolated = np.nan


        

