# -*- coding: utf-8 -*-
from transition import Transition
from state import State
import itertools
import os
import copy
import sp
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase


class Automate(AutomateBase):
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        # successeurs : list[State]
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs

    def succ(self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        re = []
        for state in listStates:
            re+=self.succElem(state, lettre)
        return re

    def acc(self):
        """ -> list[State]
        rend la liste des états accessibles
        """
        return

    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                    print "L'automate accepte le mot abc"
            else:
                    print "L'automate n'accepte pas le mot abc"
    """

    @staticmethod
    def accepte(auto, mot):
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        i = 0
        listCh = auto.getListInitialStates()
        while i < len(mot):
            listCh = auto.succ(listCh, mot[i])
            i += 1
            if listCh == []:
                return False #si il y a pas de successeurs on retourne false.
        listFin = auto.getListFinalStates()
        liste_de = [x for x in listCh if x in listFin]
        if liste_de != [] :
            return True #s'il exite au point un etat final dans la liste d'etats successeurs on retourne true.

        return False




    @staticmethod
    def estComplet(auto, alphabet):
        """ Automate x str -> bool
    rend True si auto est complet pour alphabet, False sinon
    """
        """on parcoure lettre par lettre et on voit pour chaque lettre si l'automate est complet
        s'il y a un cas ou il n'y a pas de successeur on retourne false."""
        for c in alphabet:
            for state in auto.listStates :
                if len(auto.succElem(state,c))<1 :
                    return False

        return True


    @staticmethod
    def estDeterministe(auto):
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        if len(auto.getListInitialStates())>1 :
            return False # Si l'automate a plus qu'un seul etat initial on renvoie False.

        for state in auto.listStates :
            re=auto.getListTransitionsFrom(state)# Pour chaque etat on prend la liste de transition source de cet etat

            for transition in re :
                c = 0
                for a in re :
                    if a.etiquette == transition.etiquette :
                        c+=1 #on compte le nombre de transition avec la meme etiquette
            if c>1 :
                return False
        return True


    @staticmethod
    def completeAutomate(auto, alphabet):
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        if Automate.estComplet(auto,alphabet) :
            return auto #Si l'automate est complet on le retoune lui meme.

        autoNew=copy.deepcopy(auto)
        puit=State(99,False,False,"puit")
        autoNew.addState(puit)
        for c in alphabet:
            for state in auto.listStates : #on parcoure etat par etat
                if len(auto.succElem(state,c))<1 : #Si un etat n'est pas complet on ajoute une transition vers l'etat puit
                    autoNew.addTransition(Transition(state,c,puit))
            autoNew.addTransition(Transition(puit,c,puit))#Creation des boucles pour l'etat puit

        return autoNew


    @staticmethod
    def determinisation(auto):
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if Automate.estDeterministe(auto)==True :
            return auto #Si l'automate est detemiste on le renvoie.

        alpha=auto.getAlphabetFromTransitions()
        listee=[]
        listee.append(set(auto.getListInitialStates()))
        #Creation d'une liste avec tous les etats du nouvel automate (liste de set).
        for ensemble in listee :
            for c in alpha :
                new = set(auto.succ(list(ensemble),c))
                if new not in listee :
                    listee.append(new)

        autonew = Automate([],[])
        #Creation des etats dans le nouvel automate.
        autonew.listStates.append(State(0,True,False))
        for i in range (1,len(listee)) :
            setFinal=set(auto.getListFinalStates())
            if listee[i].isdisjoint(setFinal)==False:
                autonew.listStates.append(State(i,False,True))
            else :
                autonew.listStates.append(State(i, False, False))

        #Creation des transitions.
        for i in range(0,len(listee)):
            for c in alpha:
                setSucc=set(auto.succ(list(listee[i]),c))
                indiceSucc=listee.index(setSucc)
                newTrasition=Transition(autonew.listStates[i],c,autonew.listStates[indiceSucc])
                autonew.addTransition(newTrasition)

        return autonew


    @staticmethod
    def complementaire(auto, alphabet):
        """ Automate x str -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de auto
        """
        autoNew=copy.deepcopy(auto)
        if (Automate.estComplet(autoNew,alphabet)==False):#On complete l'automate
            autoNew=Automate.completeAutomate(autoNew,alphabet)
        if (Automate.estDeterministe(autoNew)==False):#on determinise l'automate
            autoNew=Automate.determinisation(auto)
        for state in autoNew.listStates:#Pour chaque etat non final de l'automate on le rend final et reciproquement.
            if state.fin==False:
                state.fin=True
            else :
                state.fin=False


        return autoNew


    @staticmethod
    def intersection(auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        autoNew1=auto1
        autonew2=auto2

        if (Automate.estDeterministe(auto1)==False):
            autoNew1=Automate.determinisation(auto1)
        if(Automate.estDeterministe(auto2)==False):
            autonew2=Automate.determinisation(auto2)

        autoNew=Automate([],[])

        listeAlpha1=autoNew1.getAlphabetFromTransitions()
        listeAlpha2=autonew2.getAlphabetFromTransitions()
        listeAlpha=[val for val in listeAlpha1 if val in listeAlpha2 ]

        listeInt1=autoNew1.getListInitialStates()
        listeInt2=autonew2.getListInitialStates()
        listeProduit=list(itertools.product(listeInt1,listeInt2))

        #creation de la liste des etats du nouvel automate
        for couple in listeProduit:
            for c in listeAlpha:
                listee=autoNew1.succElem(couple[0],c)
                listee+=autonew2.succElem(couple[1],c)
                if (len(listee)!=2):
                    continue
                if tuple(listee) not in listeProduit:
                    listeProduit.append(tuple(listee))
        #creation des etats
        for i in range(0,len(listeProduit)):
            if (i==0):
                autoNew.listStates.append(State(i, True, False))
            else :
                autoNew.listStates.append(State(i,False,False))
        #creation des transition
        for couple in listeProduit:
            for c in listeAlpha:
                listee = autoNew1.succElem(couple[0],c)
                listee+=autonew2.succElem(couple[1],c)
                indiceCouple=autoNew.listStates[listeProduit.index(couple)]
                indiceSucc=autoNew.listStates[listeProduit.index(tuple(listee))]
                autoNew.addTransition(Transition(indiceCouple,c,indiceSucc))
        #creation des etats finaux
        listFin1=autoNew1.getListFinalStates()
        listFin2=autonew2.getListFinalStates()

        listeProduitFin = list(itertools.product(listFin1, listFin2))

        for couple in listeProduitFin:
            if couple in listeProduit:
                autoNew.listStates[listeProduit.index(couple)].fin=True

        return autoNew


    @staticmethod
    def union(auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        autoNew=copy.deepcopy(auto1)

        listet = auto2.listTransitions
        # copy transition
        for i in listet:
            autoNew.listTransitions.append(copy.deepcopy(i))
        # copy states
        listeLabelStates = []
        for i in autoNew.listStates:
            listeLabelStates.append(i.label)

        for i in autoNew.listTransitions:
            if (i.stateSrc.label not in listeLabelStates):
                autoNew.listStates.append(i.stateSrc)
                listeLabelStates.append(i.stateSrc.label)
            if (i.stateDest.label not in listeLabelStates):
                autoNew.listStates.append(i.stateDest)
                listeLabelStates.append(i.stateDest.label)

        return autoNew


    @staticmethod
    def concatenation(auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        autoNew1=copy.deepcopy(auto1)
        autoNew2=copy.deepcopy(auto2)
        listfin1=autoNew1.getListFinalStates()
        listfin2=autoNew2.getListFinalStates()
        listint1=autoNew1.getListInitialStates()
        listint2=autoNew2.getListInitialStates()
        litvide1=False
        litvide2=False
        listttt=autoNew1.getListFinalStates()

        for i in listfin1:
            if i in listint1:
                litvide1=True
                break
        for i in listfin2:
            if i in listint2:
                litvide2=True
                break
        if litvide1==False:
            for i in listint2:
                i.init=False
        if litvide2==False:
            for i in listfin1:
                i.fin=False
        autoNew1=autoNew1.prefixStates("A")
        autoNew2=autoNew2.prefixStates("B")

        autoNew = copy.deepcopy(autoNew1)

        listet = autoNew2.listTransitions
        # copy transition
        for i in listet:
            autoNew.listTransitions.append(copy.deepcopy(i))
        # copy states
        listeLabelStates = []
        for i in autoNew.listStates:
            listeLabelStates.append(i.label)
        listIntNew2=[]
        for i in autoNew.listTransitions:
            if (i.stateSrc.label not in listeLabelStates):
                if (i.stateSrc.init==True):
                    listIntNew2.append(i.stateSrc)
                autoNew.listStates.append(i.stateSrc)
                listeLabelStates.append(i.stateSrc.label)
            if (i.stateDest.label not in listeLabelStates):
                if (i.stateDest.init==True):
                    listIntNew2.append(i.stateDest)
                autoNew.listStates.append(i.stateDest)
                listeLabelStates.append(i.stateDest.label)

        for t in autoNew.listTransitions:
            if t.stateDest in listttt:
                for j in listIntNew2:
                    autoNew.addTransition(Transition(t.stateSrc,t.etiquette,j))


        return autoNew


    @staticmethod
    def etoile(auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        autoNew = copy.deepcopy(auto)
        listinit = autoNew.getListInitialStates()
        """gestion du cas ou l'automate n'est pas sous forme standard mais marche que si l'etat initial n'est pas final"""
        """standard = True
        listTo=[]
        
        for i in autoNew.listTransitions :
            if i.stateDest in listinit:
                listTo.append(i)
                standard=False
        if standard == False :
            for i in listinit:
                listFrom=autoNew.getListTransitionsFrom(i)
                s=State(99+i.id,False,False,"p"+i.label)
                autoNew.addState(s)
                for j in listFrom:
                    autoNew.addTransition(Transition(s,j.etiquette,j.stateDest))
                for j in listTo:
                    autoNew.addTransition(Transition(j.stateSrc,j.etiquette,s))
                    autoNew.removeTransition(j)"""

        listfin = autoNew.getListFinalStates()
        #tout les etats initiaux en etats finaux
        for i in autoNew.getListInitialStates():
            i.fin=True
        #chasque transition des etats initiaux va etre dupliqué de l'etats dest au etats finaux 
        for i in listinit:
            listTransition=autoNew.getListTransitionsFrom(i)

            if (listTransition==[]):
                continue

            for t in listTransition:
                for f in listfin:

                    autoNew.addTransition(Transition(f,t.etiquette,t.stateDest))

        return autoNew
