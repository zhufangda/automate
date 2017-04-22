#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections import Iterable  

class Transition(object):
    
    def __init__(self,application=set()):
        self.__application =application
    
    def put(self,etatSrc,label,etatDest):
        """Put a transition in the list of transitions.
        Args:
            etatSrc:initial state 
            label: letter
            etatDest: final state
        """
        self.__application.add((etatSrc,label,etatDest))
    
    def remove(self,trans):
        """Remove a transition.
        Args:
            a transition given
        Returns:
             a transition removed
        """
        self.__application.remove(trans)
        return trans
        
    def getEtat(self,etatSrc,label):
        """ get end state by the start state and the symbole.
        Args:
            etatSrc:initial state 
            label: letter
        Returns:
            the set of final state
        """
        return set([x[2] for x in self.__application if etatSrc==x[0] and label==x[1]])
                 
    def getTransition(self,start=None,symbol=None,end = None):
        """ get the transition by the given arguments.
        Args:
            start: initial state 
            symbol: lettre
            end: final state
        Returns:
            the set of transitions related to the given arguments.
        """
        if start == None:
            startSet = self.__application.copy()
        elif isinstance(start, set):
            startSet = set([ trans for trans in self.__application 
                            for state in start if trans[0] == state])
        else:
            startSet = set([ x for x in self.__application  if x[0]==start])
        
        
        if symbol == None:
            symbolSet = self.__application.copy()
        elif isinstance(symbol, set) and symbol != '':
            symbolSet = set([ trans for trans in self.__application 
                            for lettre in symbol if trans[1] == lettre])
        else:
            symbolSet = set([ x for x in self.__application if x[1]==symbol])
        
        
        if end == None:
            endSet = self.__application.copy()
        elif isinstance(end, set):
            endSet = set([ trans for trans in self.__application 
                            for state in end if trans[2] ==state])
        else:
            endSet = set([ x for x in self.__application if x[2]==end])    
        
        return startSet.intersection(endSet,symbolSet)
        
    
    def removeTransitionByState(self,state):
        """remove all the transition related to the state given.
        Args:
            a state given
        Returns: 
            the tuple of all the transition removed.
        """
        list = []
        for element in self.__application.copy():
            if element[0]==state or element[2]==state:
                self.__application.remove(element)
                list.append(element)
        return tuple(list)

    def exist(self,start,symbol,end):
        """Check if the transition given exist.
        Args:
            start: initial state 
            symbol: lettre
            end: final state
        Returns:
            True,if the transition given exist,False, if not.
        """
        return (start,symbol,end) in self.__application
    
    def __str__(self):
        return str(self.__application)
    
    def __iter__(self):
        return iter(self.__application)
    
    def clear(self):
        self.__application.clear()

