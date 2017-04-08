#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:41:46 2017

@author: WANG Huan
"""

import xml.etree.ElementTree as ET
from automaton import exception as excep

class Automate(object):
    __slots__ = ('__identify',
                 '__etats',
                 '__etat_init',
                 '__etats_final',
                 '__alphabet',
                 '__trans') 
    def __init__(self,
                 identify = 0,
                 etats=set(),
                 etat_init=None,
                 etats_final = set(),
                 alphabet =set() ,
                 trans= Transition.Transition()):
        self.__identify = identify
        self.__etats = etats
        self.__etat_init = etat_init
        self.__etats_final = etats_final
        self.__alphabet = alphabet
        self.__trans = trans
            
    def __str__(self):
        return 'id:' + str(self.__identify) + "\n" \
              +'Complet:\t' + str(self.isComplet()) + '\n\t' \
              +'Deterministe:\t' + str(self.isDeterministe()) + '\n\t' \
              +'etats:\t\t'+ str(self.__etats) + "\n\t"  \
              +'etat_init:\t'+ str(self.__etat_init) + "\n\t"  \
              +'etats_final:\t'+ str(self.__etats_final) + "\n\t"  \
              +'alphabet:\t'+ str(self.__alphabet) + '\n\t' \
              +'trans:\t'+ str(self.__trans) + '\n'
    
    def add_transition(self, start, symbol, end, replace = False):
        """add a given state to the automaton"""
        if start not in self.__etats:
            raise excep.StateNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined start state '%s'"
                                % (label, start))
        if end not in self.__etats:
            raise excep.StateNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined end state '%s'"
                                % (label, end))
        if symbol not in self.__alphabets:
             raise excep.SymbolNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined end state '%s'"
                                % (symbol, end))
        if (start,symbol,end) in self.__trans and replace == False:
            raise excep.Duplicateaise("Cannot add transition from"
                                     " '%(start_state)s' to '%(end_state)s'"
                                     " on symbol '%(event)s' because a"
                                     " transition from '%(start_state)s'"
                                     " to '%(existing_end_state)s' on"
                                     " symbol '%(event)s' already exists."
                                     % {'existing_end_state': target.name,
                                        'end_state': end, 'event': event,
                                        'start_state': start})
        else:
            self.__trans.put(start,symbol,end)
        
    def add_state(self,state,final = False,init = False):
        """Adds a given state to the automaton."""
        if state in self._etats:
            raise excep.Duplicate("State '%s' already defined" % state)
        if init:
            if self.__etat_init != None:
                raise excep.Duplicate("Cannot add the state '%(state)s'"
                                      " as start state, beacause a start "
                                      "state '%(origineState)s' already" 
                                      "exists" % {'state':state,
                                      'origineState':self.__etat_init})
        self.__etats.add(state)
        if final:
            self.__etats_final.add(state)
            
    def add_symbol(self,symbol):
        self.__alphabet.add(symbol)
        
    def remove_state(self,state):
        """remove the state given and the relevant transitions"""
        if state not in self.__etate:
            raise excep.StateNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined start state '%s'"
                                % (label, start))
        if state == self.__etat_init:
            warnings.warn('The state is an initial state')
        if state in self.__etats__final:
            warnings.warn('The state is a final state')
        
        self.__etat
        
    def import_XML(self,filePaht):
        tree = ET.parse('../res/jeu0.xml')
        root = tree.getroot()
        self.__alphabets = set()
        self.__identify = tree.find("automate").attrib['id']
        for etat in root.iter('etat'):
            type(etat.attrib)
            self.add_state(etat.attrib['nom'],
                           final = 'final' in etat.attrib,
                           init = 'initial' in etat.attrib)
        for trans in root.iter('trans'):
            self.add_transition(trans.attrib['deb'],
                                trans.attrib['label'],
                                trans.attrib['fin'])
            self.__alphabets.add(trans.attrib['label'])
    
    
    def isComplet(self):
        for etat in self.__etats:
            for alphabet in self.__alphabets:
                if self.__trans.getEtat(etat,alphabet) ==[] :
                    return False
        return True
    
    def isDeterministe(self):
        for etat in self.__etats:
            for alphabet in self.__alphabets:
                if len(self.__trans.getEtat(etat,alphabet))>1 :
                    return False
        return True
    
    def isReconnu(self, mot):
        q = self.__etat_init
        
        def reconnu(mot,q):
            trueList =[]
            if mot=='':
                if q in self.__etats_final:
                    return True
                else:
                    return False
            else:
                if len(self.__trans.getEtat(q,mot[0])) != 0:
                    etatList = set(self.__trans.getEtat(q,mot[0]))
                    trueList.extend( [reconnu(mot[1:],x) for x in etatList])
                if len(self.__trans.getEtat(q,'')) != 0:
                    etatList=set(self.__trans.getEtat(q,''))
                    trueList.extend([reconnu(mot,x) for x in etatList])
                
                if True in trueList:
                    return True
                else:
                    return False
        return reconnu(mot,q)

    def getNFA(self):
        if not '' in self.__alphabets:
            return ;
        
        videLabelSet = self.__trans.getTransitionByLabel('')
        
        while len(videLabelSet) > 0:
            for transSet in videLabelSet:
                for nextSet in self.__trans.getTransitionByScr(transSet[2]):
                    if nextSet[0] in self.__etats_final:
                        self.__etats_final.remove(nextSet[0])
                        self.__etats_final.add(transSet[0])
                    self.__trans.remove(nextSet)
                    self.__trans.put(transSet[0],nextSet[1],nextSet[2])
                self.__trans.remove(transSet)
            videLabelSet = self.__trans.getTransitionByLabel('')  
            print('videLabel:' + str(videLabelSet))
        
    def determiniser(self):
        self.getNFA()
        
        def f(etat = self.__etat_init):
            if self.isDeterministe:
                return
            
            etatDesList =[self.__trans.getTransitionByScr(etat,lettre) for lettre in self.__alphabets]
                if len(etatDesList) == 0:
                    continue
                if len(etatDesList) == 1:
                    return f(etatDesList[0])
                if len(etatDesList) >1 :
                    for etatDes in etatDesList:
                        self.__trans.remove(etat,lettre,etatDes)
                    []
                    self.__etats.add(etatDesList)
            
    
        
        



    def minimiser(self):
        if not (self.isDeterministe()):
            raise Exception("Automate is not deterministe!")
        partitionList = [self.__etats_final, self.__etats.difference(self.__etats_final)]
        isDivisable = True
        
        
        while isDivisable:
            isDivisable = False
            for lettre in self.__alphabets:
                oriLength = len(partitionList)
                for partition in partitionList:
                    if len(partition) == 1:
                        continue
                    maxNumber =  len(partitionList)+1
                    sousSetList = [set() for x in range(maxNumber)] 
                    
                    for x in partition:    
                            index = self.__findEtat(x,lettre,partitionList)
                            if index ==None:
                                sousSetList[maxNumber-1].add(x)
                            else:
                                sousSetList[index].add(x)
                    partitionList.remove(partition)
                    partitionList.extend([x for x in sousSetList if len(x)>0])
                if oriLength != len(partitionList):
                    isDivisable = True
       
        
    def __findEtat(self,etat,label,partitionList):
        etatFinal = self.__trans.getEtat(etat,label)
        if etatFinal == []:
            return None
        for i in range(len(partitionList)-1):
            if etatFinal[0] in partitionList[i]:
                return i
        return None
        
automate = Automate()
automate.import_XML('../res/jeu0.xml')

automate.getNFA()
print(automate)
    