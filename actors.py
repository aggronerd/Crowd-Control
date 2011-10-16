__author__ = 'greg'

from direct.actor.Actor import Actor

class Person(Actor):

    name = "Greg Doran"

    #Core attributes
    agility = 1.0
    strength = 1.0
    willpower = 1.0 #effects motivation and resistance
    charisma = 1.0 #leadership
    intelligence = 1.0
    wisdom = 1.0

    #Physical attributes
    height = 6.0
    weight = 2.0
    health = 1.0

    #Alignment
    good_bad = 0.0
    lawful_chaotic = 0.0

    #Status (might be calculated on the fly based on modifiers)
    calm_stressed = 0.0
    contempt_angry = 0.0
    sad_happy = 0.0
    fearful_resistant = 0.0
    demoralised_motivated = 0.0

    #collections
    traits = [] #eg. leader of men, easily clostraphobic, hard to wind down, easily wound up, scared of working class
    modifiers = [] # describes changes to the statuses (eg. had a tough day at work +1 stress) - must also describe when they ware of and the gradient, if any they follow.

    def __init__(self):
        Actor.__init__(self, "models/man")
        self.setScale(0.5, 0.5, 0.5)

    def checkConditions(self):
        print("checking conditions")

    def think(self):
        #radomise chance of action following any of the above conditions
        #obviously effected by the existing actions undertaken.
        print("thinking...")

    def resolveEmotions(self):
        #over time various things will effect the amout emotions go up or down, these are set of modifiers
        print("resolving emotions")


  