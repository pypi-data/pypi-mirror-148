import sys
import pickle

class GPTuner():

    def __init__(self, tuning_vars=[], objective=None):
        # a dict of dicts
        # key to dict: names of each variable
        # each dict has several fields...
        self.tuning_vars = tuning_vars
        #input: a list of tuning vars
        #output: 
        self.objective = objective

    #returns a bunch of skopt spaces
    #see here for details: https://scikit-optimize.github.io/stable/modules/classes.html?highlight=space#module-skopt.space.space
    def tuning_space(self):
        return [x[1] for x in self.tuning_vars]

    def tune():
        # serialize the objects and send them to the remote
        pass

class TunableTransform():
    
    def __init__(self, file_location):
        self.file_location = file_location
    
    def makeTunable(name=None):
        if name is None:
            # random name; come up with something
            self.name = 