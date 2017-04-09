#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 15:06:26 2017

@author: zhufangda
"""

import unittest
import transition
import automate


class TestAutomate(unittest.TestCase):
    def setUp(self):
        self.automate = automate.Automate()
        self.automate.import_XML('../res/jeu0.xml')
        
    def test_add_import_XML(self):
        pass
    
    def test_getNFA(self):
        self.automate.getNFA()
        self.assertFalse('' in self.automate.alphabet)
    
    def test_isComplet(self):
        self.assertFalse(self.automate.isComplet())
        
    def test_isDeterministe(self):
        self.assertTrue(self.automate.isDeterministe())
        self.automate.getNFA()
        self.assertFalse(self.automate.isDeterministe())
    
    def tearDown(self):
        self.automate = None
        
class TestTransition(unittest.TestCase):
    def setUp(self):
        self.trans = transition.Transition({('0','a','1')})
        self.trans.put('0','b','1')
        self.trans.put('1','b','0')
        self.trans.put('0','c','1')
        self.trans.put('0','a','2')
        self.trans.put('0','e','1')
        
    def test_put(self):

        self.assertTrue(('0','b','1') in self.trans)

    def test_getEtat(self):
        self.assertTrue(self.trans.getEtat('0','a') == {'1','2'} \
                        or self.trans.getEtat('0','a') == {'1','2'})
        self.assertEqual(self.trans.getEtat('0','f'),set())
        
    def test_getTransition(self):
        self.assertEqual(self.trans.getTransition(symbol = 'a')
                        ,{('0','a','1'),('0','a','2')})
        self.assertEqual(self.trans.getTransition(start = '1')
                        ,{('1','b','0')})
        self.assertEqual(self.trans.getTransition(end = '1')
                        ,{('0','a','1'),('0','b','1'),('0','c','1'),('0','e','1')})
        self.assertEqual(self.trans.getTransition(symbol = ('a','b'))
                        ,{('0','a','1'),('0','a','2'),('0','b','1'),('1','b','0')})
        
    def test_removeTransitionByState(self):
        self.trans.removeTransitionByState('1')
        self.assertFalse(('0','b','1') in self.trans)
        self.assertFalse(('1','b','1') in self.trans)
        self.assertFalse(('0','c','1') in self.trans)
        self.assertTrue(('0','a','2') in self.trans)
        
        
    def test_exist(self):
        self.assertTrue(self.trans.exist('0','b','1'))
        self.assertFalse(self.trans.exist('0','f','2'))

#suite = unittest.TestLoader().loadTestsFromTestCase(TestTransition)
#unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestAutomate)
unittest.TextTestRunner(verbosity=2).run(suite)