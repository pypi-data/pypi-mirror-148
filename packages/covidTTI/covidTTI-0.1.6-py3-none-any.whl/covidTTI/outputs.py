import covidTTI.analysis as analysis

def create_output(model):

    R_0 = analysis.calculate_R_0(model)
    R_eff = analysis.calculate_R_eff(model)
    fractional_R = analysis.calculate_infections_stopped(model)
    n_covid = len([c for c in model.contacts if c.has_covid])
    n_isolated = len([c for c in model.contacts if c.isolated])
    fraction_stopped = fractional_R/len(model.cases)

    output_dict = {
        "R_0" : R_0,
        "R_eff" : R_eff,
        "fractional_R" : fractional_R,
        "n_covid" : n_covid,
        "n_isolated": n_isolated,
        "fraction_stopped" : fraction_stopped
    } 

    return output_dict
