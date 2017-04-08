#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 18:56:27 2017

@author: WANG Huan
"""

class Transition(object):
    
    def __init__(self,application=set()):
        self.__application =application
    
    def put(self,etatSrc,label,etatDest):
        self.__application.add((etatSrc,label,etatDest))
    
    def remove(self,trans):
        self.__application.remove(trans)
        
    def getEtat(self,etatSrc,label):
        return [ x[2] for x in self.__application if etatSrc==x[0] and label==x[1]]

    
    def getTransitionByLabel(self,label):
        return [ x for x in self.__application if label==x[1]]
    
    def getTransitionByScr(self,etatScr):
        return [ x for x in self.__application if x[0] == etatScr]
    
    def exist(self,start,symbol,end):
        return (start,symbol,end) in self.__application
    
    def __str__(self):
        return str(self.__application)
    
    def __iter__(self):
        return iter(self.__application)
    

