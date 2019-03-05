# -*- coding: utf-8 -*-
from transition import Transition
from state import State
import os
import copy
import sp
from sp import *
from parser import Parser
from itertools import product
from automateBase import AutomateBase
from automate import Automate

#2.1 Creation d'automates
#1.
s0=State(0,True,False)
s1=State(1,False,False)
s2=State(2,False,True)

t1=Transition(s0,"a",s0)
t2=Transition(s0,"b",s1)
t3=Transition(s1,"a",s2)
t4=Transition(s1,"b",s2)
t5=Transition(s2,"a",s0)
t6=Transition(s2,"b",s0)

autom= Automate([t1,t2,t3,t4,t5,t6])
#print(autom)
#autom.show("A_ListeTrans")

#2.
auto1=Automate([t1,t2,t3,t4,t5,t6],[s0,s1,s2])
#print(auto1)
#auto1.show("A_ListeTrans")

#les automates sont identiques

#3.

auto2=Automate.creationAutomate("auto.txt")
#print(auto2)
#auto2.show("A_ListeTrans")


#2.2 Premiere manipulation
#1.
autom.removeTransition(t1)
print(autom)
#autom.show("A_ListeTrans")

#2.
autom.removeState(s1)
print(autom)
autom.addState(s1)
s2=State(0,True,False)
autom.addState(s2)
print(autom)

#3.
print(auto1.getListTransitionsFrom(s1))

#3. Exercices de base : test et complétions














