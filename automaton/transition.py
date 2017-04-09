#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 18:56:27 2017

@author: WANG Huan
"""
from collections import Iterable  

class Transition(object):
    
    def __init__(self,application=set()):
        self.__application =application
    
    def put(self,etatSrc,label,etatDest):
        self.__application.add((etatSrc,label,etatDest))
    
    def remove(self,trans):
        self.__application.remove(trans)
        return trans
        
    def getEtat(self,etatSrc,label):
        """ get end state by the start state and the symbole """
        resultat = set()
        for x in self.__application:
            if etatSrc==x[0] and label==x[1] :
                if isinstance(x[2],str):
                    resultat.add(x[2])
                else:
                    resultat = resultat | set(x[2])
            
        return resultat

    
    def getTransition(self,start=None,symbol=None,end = None):
        """ get end state by the given arguments """
        if start == None:
            startSet = self.__application.copy()
        elif isinstance(start, Iterable):
            startSet = set([ trans for trans in self.__application 
                            for state in start if trans[0] == state])
        else:
            startSet = set([ x for x in self.__application  if x[0]==start])
        
        
        if symbol == None:
            symbolSet = self.__application.copy()
        elif isinstance(symbol, Iterable) and symbol != '':
            symbolSet = set([ trans for trans in self.__application 
                            for lettre in symbol if trans[1] == lettre])
        else:
            symbolSet = set([ x for x in self.__application if x[1]==symbol])
        
        
        if end == None:
            endSet = self.__application.copy()
        elif isinstance(end, Iterable):
            endSet = set([ trans for trans in self.__application 
                            for state in end if trans[2] ==state])
        else:
            endSet = set([ x for x in self.__application if x[2]==end])    
        
        return startSet.intersection(endSet,symbolSet)
        
    
    def removeTransitionByState(self,state):
        """remove all the transition releving the state given.
        return all the transition removed
        """
        list = []
        for element in self.__application.copy():
            if element[0]==state or element[2]==state:
                self.__application.remove(element)
                list.append(element)
        return tuple(list)

    def exist(self,start,symbol,end):
        return (start,symbol,end) in self.__application
    
    def __str__(self):
        return str(self.__application)
    
    def __iter__(self):
        return iter(self.__application)
    
    def clear(self):
        self.__application.clear()

