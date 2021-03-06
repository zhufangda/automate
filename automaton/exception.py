#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class AutomatonException(Exception):
    """Base class for *most* exceptions emitted from this library."""
class StateNotFound(AutomatonException):
    """Raised when stat in automate doesn't exist."""
class TransitionNotFound(AutomatonException):
    """Raised when transition doesn't exist."""
class SymbolNotFound(AutomatonException):
    """Raised when symbol in alphabet doesn't exist."""
class Duplicate(AutomatonException):
    """Raised when a duplicate entry is found."""
    
    