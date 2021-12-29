#!/usr/bin/python
from collections import defaultdict


# class VariableSymbol(Symbol):
#
#     def __init__(self, name, type):
#         pass
#     #
#
#
# class SymbolTable(object):
#
#     def __init__(self, parent, name): # parent scope and symbol table name
#         pass
#     #
#
#     def put(self, name, symbol): # put variable symbol or fundef under <name> entry
#         pass
#     #
#
#     def get(self, name): # get variable symbol or fundef from <name> entry
#         pass
#     #
#
#     def getParentScope(self):
#         pass
#     #
#
#     def pushScope(self, name):
#         pass
#     #
#
#     def popScope(self):
#         pass
#     #
#


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
        if name in self:
            return self.dict[name]

        if self.parent:
            return self.parent.get(name)

        return None

    def __contains__(self, item):
        return item in self.dict