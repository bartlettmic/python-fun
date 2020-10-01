#!/usr/bin/env python
from random import randint, choice

consonants= "bdfghjklmnprstvwz"
vowels="aeiouy"
syllables = randint(2,2)
name = ""

for i in range(syllables):
    fricative = choice(consonants) 
    fricative = ('' if fricative == '-' else fricative)
    sonorant = choice(vowels)
    # sonorant = ('' if sonorant == '-' else sonorant)
    name += fricative + sonorant 

print(name)
