__author__ = 'greg'

import random

class GeneralProtestSloganGenerator(object):

    slogans = ["Down with this sort of thing",
               "Jesus wouldn't want this so why would you?",
               "God hates signs!!!",
               "That would be an echenemical matter",
               "Get a brain morons!",
               "There are two types of people in this world, those who understand binary and those who don't!"]

    @classmethod
    def generateSlogan(self):
        random.seed(None)
        val = random.randrange(0,len(self.slogans)-1,1)
        return(self.slogans[val])

print(GeneralProtestSloganGenerator.generateSlogan())