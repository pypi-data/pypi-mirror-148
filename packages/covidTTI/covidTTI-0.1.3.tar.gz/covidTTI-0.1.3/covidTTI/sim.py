from covidTTI.model import TTIModel
from covidTTI.outputs import create_output

def run(config, seed = 1):

    seed = seed
    model = TTIModel(config)
    outputs = create_output(model)

    return outputs