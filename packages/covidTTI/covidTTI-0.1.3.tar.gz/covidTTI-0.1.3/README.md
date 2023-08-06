# covidTTI

[![Python Actions](https://github.com/JosiePark/TTI_impact/actions/workflows/pytest.yml/badge.svg)](https://github.com/JosiePark/TTI_impact/actions/workflows/pytest.yml)

## Introduction

A model to estimate the impact of testing, tracing and isolating on the R number.

A number of index cases are populated, that are assumed to have Covid. They can by symptomatic or not, and report contacts or not. Each index cases has household and non-household contacts. Household contacts are assumed to be contacts for everyday over the infectious period, and non-household contacts are assumed to come into contact on a single day over the infection period.

Contacts can catch Covid or not, be symptomatic or not, be tested or not, be traced or not, and isolated (or not) on each of these conditions.

## Structure

* The config file is located in the config.yaml directory
* Run scripts/scenarios.py to run the model for the parameters defined in the config file.
* covidTTI:
    * model.py : defines the model class and runs the model for all cases
    * cases.py : defines the case class and populates a single case
    * contacts.py : defines the contact class and populates a single contact
    * utils.py : defines some of the distributions (e.g. incubation period) from which samples are drawn
    * analysis.py : contains functions that calculate key statistics such as the R0 number and effective R number.
    * sim.py : runs the simulation given config settings
    * outputs.py : creates a dictionary of key outputs
    



