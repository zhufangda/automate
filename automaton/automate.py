#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 15:41:46 2017

@author: WANG Huan
"""

import xml.etree.ElementTree as ET
from xml.dom.minidom import Document
import exception as excep
import transition
import warnings
from lxml import etree

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
                 trans= transition.Transition()):
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
              +'etats:\t\t'+ str(self.etats) + "\n\t"  \
              +'etat_init:\t'+ str(self.etat_init) + "\n\t"  \
              +'etats_final:\t'+ str(self.etats_final) + "\n\t"  \
              +'alphabet:\t'+ str(self.alphabet) + '\n\t' \
              +'trans:\t'+ str(self.trans) + '\n'
              
    @property
    def trans(self):
        return self.__trans
    
    @property
    def etats(self):
        return self.__etats
    
    @property
    def etat_init(self):
        return self.__etat_init
    
    @property
    def etats_final(self):
        return self.__etats_final
    
    @property
    def alphabet(self):
        return self.__alphabet
    
    def add_transition(self, start, symbol, end, replace = False):
        """add a given state to the automaton"""
        if start not in self.__etats:
            raise excep.StateNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined start state '%s'"
                                % (symbol, start))
        if end not in self.__etats:
            raise excep.StateNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined end state '%s'"
                                % (symbol, end))
        if symbol not in self.__alphabet:
             raise excep.SymbolNotFound("Can not add a transition on lettre '%s' that"
                                " starts in a undefined end state '%s'"
                                % (symbol, end))
        if (start,symbol,end) in self.__trans and replace == False:
            raise excep.Duplicate("Cannot add transition ("
                                     " '%s'because this transition already exists."
                                     % str((start,symbol,end)))
        else:
            self.__trans.put(start,symbol,end)
        return (start,symbol,end)
        
    def add_state(self,state,final = False,init = False, replace = False):
        """Adds a given state to the automaton."""
        if state in self.__etats and not replace:
            raise excep.Duplicate("State '%s' already defined" % str(state))
        if init :
            if self.__etat_init != None and not replace:
                raise excep.Duplicate("Cannot add the state '%(state)s'"
                                      " as start state, beacause a start "
                                      "state '%(origineState)s' already" 
                                      "exists" % {'state':state,
                                      'origineState':self.__etat_init})
            self.__etat_init = state
        if final:
            self.__etats_final.add(state)
        self.__etats.add(state)
        return state
        
    def add_symbol(self,symbol):
        """add a given symbol to the automaton"""
        self.__alphabet.add(symbol)
        return symbol 
    
    def remove_state(self,state):
        """remove the state given and the relevant transitions"""
        if state not in self.__etate:
            raise excep.StateNotFound("Can not add the starts %s." % state)
        if state == self.__etat_init:
            warnings.warn('The state is an initial state')
            self.__etat_init = None
        if state in self.__etats__final:
            warnings.warn('The state is a final state')
            self.__etats_final.remove(state)
        self.__etats.remove(state)
        return state
        
    def import_XML(self,filePath):
        self.clear()
        tree = ET.parse(filePath)
        root = tree.getroot()
        self.__identify = tree.find("automate").attrib['id']
        for etat in root.iter('etat'):
            self.add_state(etat.attrib['nom'],
                           final = 'final' in etat.attrib 
                                       and etat.attrib['final'] == 'Yes',
                           init = 'initial' in etat.attrib
                                       and etat.attrib['initial'] == 'Yes')
        for trans in root.iter('trans'):
            self.add_symbol(trans.attrib['label'])
            self.add_transition(trans.attrib['deb'],
                                trans.attrib['label'],
                                trans.attrib['fin'])
            
    def isComplet(self):
        for etat in self.__etats:
            for alphabet in self.__alphabet:
                if self.__trans.getEtat(etat,alphabet) == set() :
                    return False
        return True
    
    def isDeterministe(self):
        for etat in self.__etats:
            for alphabet in self.__alphabet:
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
        if not '' in self.__alphabet:
            return 
        
        videLabelSet = self.__trans.getTransition(symbol = '')
        
        while len(videLabelSet) > 0:
            for transInSet in videLabelSet:
                for nextSet in self.__trans.getTransition(start = transInSet[2]):
                    if nextSet[0] in self.__etats_final:
                        self.__etats_final.remove(nextSet[0])
                        self.__etats_final.add(transInSet[0])
                    self.__trans.put(transInSet[0],nextSet[1],nextSet[2])
                self.__trans.remove(transInSet)
            videLabelSet = self.__trans.getTransition(symbol = '')  
        
        self.__alphabet.remove('')
        
    def determiniser(self):
        self.getNFA()
        
        while not self.isDeterministe():
            continuable = False
            alphabet = self.__alphabet.copy()
            etats = self.__etats.copy()
            
            for etat in etats:
                for lettre in alphabet:
                    newEtat = tuple(self.__trans.getEtat(etat,lettre))
                    if len(newEtat) < 2:
                        continue
                    print(etat,lettre)
                    print('newEtat:' + str(newEtat))
                    self.add_state(newEtat
                            ,final = not set(newEtat).isdisjoint(self.__etats_final)
                            ,replace = True)
                    for trans in self.__trans.getTransition(start = newEtat):
                        print('add transition from new')
                        print(self.add_transition(newEtat,trans[1],trans[2]))
                    for trans in self.__trans.getTransition(start = etat,symbol = lettre):
                        print('remove transition')
                        print(self.__trans.remove(trans))
                    print('add transition to new')
                    print(self.add_transition(start = etat,symbol = lettre,end = newEtat))
                    continuable = True
                    break
            if continuable:
                break
    def minimiser(self):
        self.determiniser()
        
        if not (self.isDeterministe()):
            raise Exception("Automate is not deterministe!")
        partitionList = [self.__etats_final, self.__etats.difference(self.__etats_final)]
        isDivisable = True
        
        while isDivisable:
            isDivisable = False
            oriLength = len(partitionList)
            for lettre in self.__alphabet:
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
        etatFinal = list(self.__trans.getEtat(etat,label))
        if etatFinal == []:
            return None
        for i in range(len(partitionList)-1):
            if etatFinal[0] in partitionList[i]:
                return i
        return None
     
    def clear(self):
        self.__alphabet.clear()
        self.__identify = None
        self.__etats.clear()
        self.__etat_init=None
        self.__etats_final.clear()
        self.__trans.clear()
    
    def export_XML(self,pathFile):
        root = etree.Element('session')
        automate = etree.SubElement(root,'automate')
        automate.set('id',self.__identify)
        etats = etree.SubElement(automate,'etats')
        transitions = etree.SubElement(automate,'transitions')
        
        for etat in self.__etats:
            state = etree.SubElement(etats,'etat')
            if etat == self.__etat_init:
                state.set('initial','Yes')
            if etat in self.__etats_final:
                state.set('final','Yes')
            state.set('nom',str(etat))
        
        for trans in self.__trans:
            transition = etree.SubElement(transitions,'trans')
            transition.set('deb',str(trans[0]))
            transition.set('label',trans[1])
            transition.set('fin',str(trans[2]))
        
        tree = etree.ElementTree(root)
        tree.write('export.xml', pretty_print=True,
               xml_declaration=True, encoding='UTF-8')

        
automate = Automate()

automate.import_XML('../res/automate1.xml')
print("Origine:" + str(automate))
automate.getNFA()
print("NFA:" + str(automate))
automate.determiniser()
print("Determiniser" + str(automate))    
automate.minimiser()
print("Minimiser:" + str(automate))
automate.export_XML('helo')