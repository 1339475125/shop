# -*- coding:utf-8 -*-


class Root(object):
    def __init__(self):
        print "this is Root"


class B(Root):
    def __init__(self):
        print "enter B"
        super(B, self).__init__()
        print "leave B"


class C(Root):
    def __init__(self):
        print "enter C"
        super(C, self).__init__()
        print "leave C"


class D(B, C):
    pass


import pdb
pdb.set_trace()
d = D()
