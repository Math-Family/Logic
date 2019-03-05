# -*- coding: utf-8 -*-

from automate import Automate
from state import State
from transition import Transition
from parser import *

print ("DEBUT PROGRAMME\n")


# Automate A0
s_a0_0 = State(0,True,True)
s_a0_1 = State(1,False,False)
s_a0_2 = State(2,False,False)
s_a0_3 = State(3,False,False)
t_a0_1 = Transition(s_a0_0,"b",s_a0_0)
t_a0_2 = Transition(s_a0_0,"c",s_a0_0)
t_a0_3 = Transition(s_a0_0,"a",s_a0_1)
t_a0_4 = Transition(s_a0_1,"b",s_a0_2)
t_a0_5 = Transition(s_a0_2,"c",s_a0_3)
t_a0_6 = Transition(s_a0_3,"b",s_a0_0)
lt_a0 = [t_a0_1,t_a0_2,t_a0_3,t_a0_4,t_a0_5,t_a0_6]
aut0 = Automate(lt_a0)
# Automate A1
s_a1_0 = State(0,True,False)
s_a1_1 = State(1,False,False)
s_a1_2 = State(2,False,True)
t_a1_0 = Transition(s_a1_0,"a",s_a1_1)
t_a1_1 = Transition(s_a1_1,"a",s_a1_0)
t_a1_2 = Transition(s_a1_1,"b",s_a1_2)
t_a1_3 = Transition(s_a1_2,"b",s_a1_2)
lt_a1 = [t_a1_0,t_a1_1,t_a1_2,t_a1_3]
aut1 = Automate(lt_a1)
# Automate A2
s_a2_0 = State(0,True,False)
s_a2_1 = State(1,False,False)
s_a2_2 = State(2,False,True)
t_a2_0 = Transition(s_a2_0,"a",s_a2_1)
t_a2_1 = Transition(s_a2_1,"a",s_a2_2)
t_a2_2 = Transition(s_a2_1,"b",s_a2_2)
t_a2_3 = Transition(s_a2_2,"b",s_a2_1)
lt_a2 = [t_a2_0,t_a2_1,t_a2_2,t_a2_3]
aut2 = Automate(lt_a2)
# Automate A3
s_a3_0 = State(0,True,False)
s_a3_1 = State(1,False,False)
s_a3_2 = State(2,False,False)
s_a3_3 = State(3,False,True)
t_a3_1 = Transition(s_a3_0,"a",s_a3_1)
t_a3_2 = Transition(s_a3_0,"a",s_a3_2)
t_a3_3 = Transition(s_a3_0,"b",s_a3_0)
t_a3_4 = Transition(s_a3_0,"b",s_a3_3)
t_a3_5 = Transition(s_a3_1,"a",s_a3_3)
t_a3_6 = Transition(s_a3_1,"b",s_a3_1)
t_a3_7 = Transition(s_a3_2,"a",s_a3_3)
t_a3_8 = Transition(s_a3_2,"a",s_a3_0)
t_a3_9 = Transition(s_a3_2,"b",s_a3_2)
t_a3_10 = Transition(s_a3_2,"b",s_a3_1)
t_a3_11 = Transition(s_a3_3,"b",s_a3_3)
t_a3_12 = Transition(s_a3_3,"a",s_a3_2)
lt_a3 = [t_a3_1,t_a3_2,t_a3_3,t_a3_4,t_a3_5,t_a3_6,t_a3_7,t_a3_8,t_a3_9,t_a3_10,t_a3_11,t_a3_12]
aut3 = Automate(lt_a3)

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode accepte")
b1 = aut3.accepte(aut3, "babaa")
print b1
b2 = aut3.accepte(aut3, "abbaaa")
print b2

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode estComplete")
b3 = aut3.estComplet(aut3, aut3.getAlphabetFromTransitions())
print b3
b4 = aut0.estComplet(aut0, aut0.getAlphabetFromTransitions())
print b4

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode estDeterministe")
b5 = aut3.estDeterministe(aut3)
print b5
b6 = aut0.estDeterministe(aut0)
print b6

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode completeAutomate")
aut1compl = aut1.completeAutomate(aut1, aut1.getAlphabetFromTransitions())
print aut1compl
""" [0(init)-a->1] [1-a->0(init)] [1-b->2(fin)] [2(fin)-b->2(fin)]
    [0(init)-b->Puit] [2(fin)-a->Puit] [Puit-a->Puit] [Puit-b->Puit]"""
aut1compl.show("A1-complete")

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode determinisation")
aut3det = aut3.determinisation(aut3)
print aut3det
""" [0(init)-a->1] [0(init)-b->2(fin)] [1-a->2(fin)]
    [1-b->1] [2(fin)-a->1] [2(fin)-b->2(fin)]"""
aut3det.show("A3-determinise")

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode complementaire")
aut3complem =aut3.complementaire(aut3, aut3.getAlphabetFromTransitions())
print aut3complem
""" [0(init)(fin)-a->1(fin)] [0(init)-b->2] [1-a->2(fin)]
    [1-b->1] [2(fin)-a->1] [2(fin)-b->2(fin)]"""
aut3complem.show("A3-complementaire")

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode intersection")
autintersec = aut1.intersection(aut1, aut2)
print autintersec
""" [0(init)-a->1] [1-a->2] [1-b->3(fin)] [3(fin)-b->4] [4-b->3(fin)] """
autintersec.show("intersection_A1_A2")

wait = raw_input("\nTo proceed press return!\n")

print ("Méthode concatenation")
a0a1concat = aut0.concatenation(aut0, aut1)
print a0a1concat
""" [0(init)-b->4(init)] [0(init)-c->4(init)] [3-b->4(init)] [0(init)-b->0(init)]
    [0(init)-c->0(init)] [0(init)-a->1] [1-b->2] [2-c->3]
    [3-b->0(init)] [4(init)-a->5] [5-a->4(init)] [5-b->6(fin)]
    [6(fin)-b->6(fin)]"""
a0a1concat.show("Concatenation_A0_A1")

a1a0concat = aut0.concatenation(aut1, aut0)
print a1a0concat
""" [1-b->3(fin)] [2-b->3(fin)] [0(init)-a->1] [1-a->0(init)] [1-b->2]
    [2-b->2] [3(fin)-b->3(fin)] [3(fin)-c->3(fin)] [3(fin)-a->4] [4-b->5]
    [5-c->6] [6-b->3(fin)]"""
a1a0concat.show("Concatenation_A1_A0")


print "\nFIN PROGRAMME\n"



