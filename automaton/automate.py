#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
from xml.dom.minidom import Document
import exception as excep
import transition
import warnings
from lxml import etree
import copy

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
        return 'id:\n\t' + str(self.__identify) + "\n" \
              +'Complet:\n\t' + str(self.isComplet()) + '\n' \
              +'Deterministe:\n\t' + str(self.isDeterministe()) + '\n' \
              +'etats:\n\t'+ str(self.etats) + "\n"  \
              +'etat_init:\n\t'+ str(self.etat_init) + "\n"  \
              +'etats_final:\n\t'+ str(self.etats_final) + "\n"  \
              +'alphabet:\n\t'+ str(self.__alphabet) + '\n' \
              +'trans:\n\t'+ str(self.trans) + '\n'
              
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
    def identify(self):
        return self.__identify
    @identify.setter
    def identify(self,identify):
        self.__identify = identify
    
    def add_transition(self, start, symbol, end, replace = False):
        """Adds a given transititon to the automaton.
    
        Args:
            start: the intial state.
            symbol: a letter of transition.
            end: the final state.
            replace: If it is false, an exception will raise 
                     when users try to add an exisent transition.
                     If it is true, there is no exception 
                     when users intend to add an existent transition
        Returns:
            a tuple that represents the transition added:(intial state,lettre,final state).  
        Raises:
            StateNotFound: An error occurred when the state donated by arguments is not in state list.
            SymbolNotFound:An error occurred when the symbol donated by arguments is not in symbol list.
            Duplicate:An error occurred when replace is false and this transition already exists.
        """        
        if start not in self.__etats:
            raise excep.StateNotFound("Can not add a transition ('%s','%s','%s')"
                                " because starts '%s' is undefined"
                                % (start,symbol, end,start))
        if end not in self.__etats:
            raise excep.StateNotFound("Can not add a transition ('%s','%s','%s')"
                                " because end '%s' is undefined"
                                % (start,symbol, end,end))
        if symbol not in self.__alphabet:
             raise excep.SymbolNotFound("Can not add a transition ('%s','%s','%s')"
                                "on lettre '%s' because that symbol is undefined"
                                % (start,symbol, end,symbol))
        if (start,symbol,end) in self.__trans and replace == False:
            raise excep.Duplicate("Cannot add transition ("
                                     " '%s'because this transition already exists."
                                     % str((start,symbol,end)))
        else:
            self.__trans.put(start,symbol,end)
        return (start,symbol,end)
        
    def add_state(self,state,final = False,init = False, replace = False):
        """Adds a given state to the automaton.
    
        Args:
            state: the state that will be added.
            final: True if it is final state, False if not.
            init: True if it is initial state, False if not.
            replace: If it is false, an exception will raise 
                     when users try to add an exisent transition.
                     If it is true, there is no exception 
                     when users intend to add an existent transition
        Returns:
            the state that is added..  
        Raises:
            Duplicate:An error occurred when replace is false and this transition already exists.
        """        
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
        """Adds a given letter to the automaton.
    
        Args:
            symbol: a given letter.    
        Returns:
            the letter that is added.
        """       
        self.__alphabet.add(symbol)
        return symbol 
    def remove_stateUseless(self):
        """Removes a state that is neither initial state,nor final state of an automaton
           but it is only final state of some transitions.
        """       
        for state in list(self.__etats):
            if state != self.__etat_init and len(self.__trans.getTransition(end = state))<1:
                 self.remove_state(state)
                 for trans in self.__trans.getTransition(start = state):
                     self.__trans.remove(trans)
                    
    def remove_state(self,state):
        """Removes the state given and the relevant transitions.
        Args:
            state:the state that will be removed.    
        Returns:
            the state that is removed.
        Raises:
            StateNotFound: An error occurred when the state donated by arguments is not in state list.
        """       
        if state not in self.__etats:
            raise excep.StateNotFound("Can not remove the starts %s." % state)
        if state == self.__etat_init:
            warnings.warn("The state '%s' is an initial state" % state)
            self.__etat_init = None
        if state in self.__etats_final:
            warnings.warn("The state '%s' is a final state" % state)
            self.__etats_final.remove(state)
        self.__etats.remove(state)
        for trans in self.__trans.getTransition(start = state):
            self.__trans.remove(trans)
        for trans in self.__trans.getTransition(end = state):
            self.__trans.remove(trans)
        
        return state
    
     
    def import_Automate(self,child):
        """import un file of XML.
        Args:
            filePavth: the path of the file XML.
        """ 
        self.__identify =child.attrib["id"]
        for etat in child.iter('etat'):
            x = self.add_state(etat.attrib['nom'],
                           final = 'final' in etat.attrib 
                                       and etat.attrib['final'] == 'Yes',
                           init = 'initial' in etat.attrib
                                       and etat.attrib['initial'] == 'Yes')
        for trans in child.iter('trans'):
            self.add_symbol(trans.attrib['label'])
            self.add_transition(trans.attrib['deb'],
                                trans.attrib['label'],      
                          trans.attrib['fin'])
            
    def isComplet(self):
        """Check if the automaton is complet.
    
        Returns:
            True if the automaton is complet, False if not.
        """        
        for etat in self.__etats:
            for alphabet in self.__alphabet:
                if self.__trans.getEtat(etat,alphabet) == set() :
                    return False
        return True
    
    def isDeterministe(self):
        """Check if the automaton is deterministe.
    
        Returns:
            True if the automaton is deterministe, False if not.
        """
        for etat in self.__etats:
            for lettre in self.__alphabet:
                if len(self.__trans.getEtat(etat,lettre))>1 :
                    return False
        return True
    
    def isReconnu(self, mot):
        """Check if the word given can be recognized by the automaton.
        Args:
            the word given.
        Returns:
            True,if the word given can be recognized, False, if not.
        """        
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
        """Delete the empty transition and get the nondeterministic finite automaton."""
        
        if not '' in self.__alphabet:
            return 
        
        videLabelSet = self.__trans.getTransition(symbol = '')
        
        while len(videLabelSet) > 0:
            for transInSet in videLabelSet:
                for nextSet in self.__trans.getTransition(start = transInSet[2]):
                    if nextSet[0] in self.__etats_final:
                        self.__etats_final.add(transInSet[0])
                    self.__trans.put(transInSet[0],nextSet[1],nextSet[2])
                self.__trans.remove(transInSet)
            videLabelSet = self.__trans.getTransition(symbol = '')  
         
        self.__alphabet.remove('')
        self.remove_stateUseless()
        
    def determiniser(self):
        """Trun a nondeterministic finite automaton into a deterministic finite automaton"""
        self.getNFA()
        
        while not self.isDeterministe():
            for oldTrans in copy.deepcopy(self.__trans):
                newEtat = self.__trans.getEtat(oldTrans[0],oldTrans[1])
                if len(newEtat) < 2:
                    continue
                for etat in newEtat.copy():
                    if isinstance(etat,str):
                        pass
                    else:
                        newEtat.remove(etat)
                        newEtat = newEtat | set(etat)
                    if tuple(newEtat) in self.__etats:
                        continue
                newEtat = tuple(newEtat)
                if len(newEtat) < 2:
                    continue
                self.add_state(newEtat
                        ,final = not set(newEtat).isdisjoint(self.__etats_final)
                        ,replace = True)
                
                for trans in self.__trans.getTransition(start = oldTrans[0]
                                                        ,symbol = oldTrans[1]):

                    self.__trans.remove(trans)
                self.add_transition(start = oldTrans[0]
                                        ,symbol = oldTrans[1]
                                        ,end = newEtat)

                for trans in self.__trans.getTransition(start = set(newEtat)):
                    self.add_transition(newEtat,trans[1],trans[2],replace = True)

                self.remove_stateUseless()
                
    def minimiser(self):
        """Trun a deterministic finite complete automaton into minimal AFDC"""
        self.determiniser()
        
        if not (self.isDeterministe()):
            raise Exception("Automate is not deterministe!")
        partitionList = [self.__etats_final,
                         self.__etats.difference(self.__etats_final)]
        isDivisable = True
        
        while isDivisable:
            isDivisable = False
            oriLength = len(partitionList)
            
            for lettre in self.__alphabet:
                for partition in partitionList.copy():    
                    if len(partition) <= 1:
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
                    
        for partition in partitionList:
            if len(partition) <2:
                continue
            newEtat = partition
            newState = set()
            for etat in newEtat:
                if isinstance(etat,str):
                    newState.add(etat)
                else:
                    newState = newState | set(etat)
            newState = tuple(newState)
            
            if self.__etat_init in partition:
                self.__etat_init = newState
            if not self.__etats_final.isdisjoint(newEtat):
                self.__etats_final.add(newState)
                self.__etats_final.difference_update(newState)
            self.__etats.add(newState)
            for state in partition:
                self.__etats.remove(state)
                for trans in self.__trans.getTransition(start = state):
                    self.__trans.remove(trans)
                    if trans[2] in partition:
                        self.__trans.put(newState, trans[1],newState)
                    else:
                        self.__trans.put(newState, trans[1],trans[2])
                for trans in self.__trans.getTransition(end = state):
                    self.__trans.remove(trans)
                    if trans[0] in partition:
                        self.__trans.put(newState, trans[1],newState)
                    else:
                        self.__trans.put(trans[0], trans[1],newState)
                        
                        
    def __findEtat(self,etat,label,partitionList):
        etatFinal = list(self.__trans.getEtat(etat,label))
        if len(etatFinal) < 1:
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
        """Store the present automaton in a file of XML"""
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
        tree.write(pathFile, pretty_print=True,
               xml_declaration=True, encoding='UTF-8')


def openXML(filePath):
    tree = ET.parse(filePath)
    root = tree.getroot()
    automateList = []
    for child in root.iter('automate'):
        automate = Automate()
        automate.identify = child.attrib["id"]
        for etat in child.iter('etat'):
            automate.add_state(etat.attrib['nom'],
                           final = 'final' in etat.attrib 
                                       and etat.attrib['final'] == 'Yes',
                           init = 'initial' in etat.attrib
                                       and etat.attrib['initial'] == 'Yes')
        for trans in child.iter('trans'):
            automate.add_symbol(trans.attrib['label'])
            automate.add_transition(trans.attrib['deb'],
                                trans.attrib['label'],      
                          trans.attrib['fin'])
            
        automateList.append(copy.deepcopy(automate))
        automate.clear()
    return automateList
