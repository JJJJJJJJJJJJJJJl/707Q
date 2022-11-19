from enum import Enum

"""
    Enums are based on leafly.com metrics.
"""

class Type(Enum):
    nan = 0
    indica = 1
    hybrid = 2
    sativa = 3

# Contains both positive and negative effects
class Effect(Enum):
    nan = 0
    anxious = 1
    aroused = 2
    creative = 3
    dizzy = 4
    dry_eyes = 5
    dry_mouth = 6
    energetic = 7
    euphoric = 8
    focused = 9
    giggly = 10
    happy = 11
    headache = 12
    hungry = 13
    paranoid = 14
    relaxed = 15
    sleepy = 16
    talkative = 17
    tingly = 18
    uplifted = 19

class Terpene(Enum):
    nan = 0
    caryophyllene = 1
    humulene = 2
    limonene = 3
    linalool = 4
    myrcene = 5
    ocimene = 6
    pinene = 7
    terpinolene = 8

class Flavor(Enum):
    nan = 0
    ammonia = 1
    apple = 2
    apricot = 3
    berry = 4
    blueberry = 5
    blue_cheese = 6
    butter = 7
    cheese = 8
    chemical = 9
    chestnut = 10
    citrus = 11
    coffee = 12
    diesel = 13
    earthy = 14
    flowery = 15
    grape = 16
    grapefruit = 17
    honey = 18
    lavender = 19
    lemon = 20
    lime = 21
    mango = 22
    menthol = 22
    mint = 23
    nutty = 24
    orange = 25
    peach = 26
    pear = 27
    pepper = 28
    pine = 29
    pineapple = 30
    plum = 31
    pungent = 32
    rose = 33
    sage = 34
    skunk = 35
    #Spicy/Herbal - remember this when formatting collected flavors -> "/" to "_"
    spicy_herbal = 36
    strawberry = 37
    sweet = 38
    tar = 39
    tea = 40
    tobacco = 41
    # Tree Fruit - also this -> " " to "_"
    tree_fruit = 42
    tropical = 43
    vanilla = 44
    violet = 45
    woody = 46

""" 
    Each instance of the Strain object corresponds to a data-point in the data-set.

    NaN attribute values:
        Integer = -1
        String = ""
        List = []
        Enum = EnumType.nan
"""
class Strain(object):
    def __init__(self, name="", images=[], type=Type.nan, main_effect=Effect.nan, effects=[], thc=-1, cbd=-1, cbg=-1, main_terpene=Terpene.nan, main_flavor=Flavor.nan, flavors=[]):
        self._name = name;
        self._images = images;
        self._type = type;
        self._main_effect = main_effect;
        self._effects = effects;
        self._thc = thc;
        self._cbd = cbd;
        self._cbg = cbg;
        self._main_terpene = main_terpene;
        self._main_flavor = main_flavor;
        self._flavors = flavors;
    
    @property
    def name(self):
        return self._name;
    
    @name.setter
    def name(self, name):
        self.name = name;

    @property
    def images(self):
        return self._images;

    @property
    def type(self):
        return self._type;
    
    @property
    def main_effect(self):
        return self._main_effect;
    
    @property
    def effects(self):
        return self._effects;

    @property
    def thc(self):
        return self._thc;
    
    @property
    def cbd(self):
        return self._cbd;
    
    @property
    def cbg(self):
        return self._cbg;

    @property
    def main_terpene(self):
        return self._main_terpene;

    @property
    def main_flavor(self):
        return self._main_flavor;

    @property
    def flavors(self):
        return self._flavors;


def main():
    print("Strain Object Class File");
    print(Type["sativa"]);

if __name__ == "__main__":
    main();