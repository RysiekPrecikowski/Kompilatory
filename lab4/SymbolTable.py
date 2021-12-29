#!/usr/bin/python
from collections import defaultdict


class VariableSymbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class SymbolTable(object):
    class Scope:
        def __init__(self, parent=None):
            self.dict = {}
            self.parent = parent

    def __init__(self):
        self.current_scope = SymbolTable.Scope()

    def put(self, name, symbol):# put variable symbol or fundef under <name> entry
        self.current_scope.dict[name] = symbol

    def get(self, name):
        scope = self.current_scope

        while scope:
            if name in scope.dict:
                return scope.dict[name]

            scope = scope.parent

        return None

    def pushScope(self):
        self.current_scope = SymbolTable.Scope(self.current_scope)

    def popScope(self):
        pass

