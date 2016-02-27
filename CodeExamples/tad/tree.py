#!/usr/bin/env python3
# tree.py
# author: Sébastien Combéfis
# version: February 27, 2016

import copy

class Tree:
    def __init__(self, value, children=[]):
        self.__value = value
        self.__children = copy.deepcopy(children)
    
    @property
    def size(self):
        result = 1
        for child in self.__children:
            result += child.size
        return result
    
    @property
    def value(self):
        return self.__value
    
    @property
    def children(self):
        return copy.deepcopy(self.__children)
    
    def addChild(self, tree):
        self.__children.append(tree)
    
    def __str__(self):
        def _str(tree, level):
            result = '[{}]\n'.format(tree.__value)
            for child in tree.children:
                result += '{}|--{}'.format('   ' * level, _str(child, level + 1))
            return result
        return _str(self, 0)

if __name__ == '__main__':
    t = Tree(12, [Tree(7, [Tree(13), Tree(2, [Tree(-61)]), Tree(99)]), Tree(-1), Tree(4, [Tree(3), Tree(8)]), Tree(9)])
    print(t)
    print('Size:', t.size)
    print('Value:', t.value)
    print('Children:', [t.value for t in t.children])
    t.addChild(Tree(911, [Tree(1), Tree(2), Tree(3)]))
    print(t)