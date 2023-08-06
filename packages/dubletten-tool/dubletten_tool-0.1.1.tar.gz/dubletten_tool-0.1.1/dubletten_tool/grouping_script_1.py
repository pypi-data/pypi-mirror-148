import os
import pandas as pd
from copy import deepcopy
from collections import Counter, defaultdict
import numpy as np 
import re
from apis_core.apis_entities.models import Person, Institution, Place, Event, Work
from apis_core.apis_relations.models import *
from apis_core.apis_metainfo.models import Collection
from apis_core.apis_vocabularies.models import *
#import Levenshtein as lev
import logging


log = logging.getLogger("mylogger")
log.setLevel(logging.INFO)

log.info("logger init")

# base entities
P = Person
I = Institution
PL = Place
W = Work
E = Event

#functions
F = PersonInstitutionRelation

#other relations
PI = PersonInstitution
PE = PersonEvent
PP = PersonPlace
IP = InstitutionPlace

#collections
HSV = Collection.objects.get(name="Import HSV full 22-6-21")
HZAB = Collection.objects.get(name="Import HZAB full 10-3-21")
ACC = Collection.objects.get(name="Import ACCESS full 13-10-21")
MAN = Collection.objects.get(name="manually created entity")

#other
ENTS = [P, I, PL, W, E]

def get_hs(instname):
    if "(" in instname:
        temp = instname.replace("(", "$", 1)
        hs = temp.split("$")[1][:-1]
        return hs
    else:
        return None


df_per = pd.DataFrame(Person.objects.all().values()).set_index("id")
per = df_per[["name", "first_name", "gender", "start_date", "end_date", "start_date_written", "end_date_written"]]
per["fullname"] = per.name + ", " + per.first_name



def get_groups():
    names_gender = []
    df_test = []
    frames = []
    c = 0
    for d, group in per.groupby(["fullname", "gender"]):
        if len(group) > 1:
            log.info(f"{len(group)}, {d}, {[f for f in group.index]}")
            names_gender.append((len(group), d))
            df_test.append({"count":len(group), "key":d})
            c += len(group)
            frames.append(group)
    
    return names_gender





###### Levenshtein Distance #####

# DISTANCE_VALUE = 2
# def lev_distance(a, series, container):
#     for pk, b in series.items():
#         dist = lev.distance(a,b)
#         if 0 < dist <= DISTANCE_VALUE:
#             container.append((dist, b, pk))
#     return container

# test = "Müller"
# container = []

# #container = lev_distance(test, per.name, container)




