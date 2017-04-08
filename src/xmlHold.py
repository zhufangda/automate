# -*- coding: utf-8 -*-
"""
This class of automate
"""


tree = ET.parse('../res/jeu0.xml')
root = tree.getroot()

for child in root.iter('etat'):
    print(child.tag, child.attrib)
    