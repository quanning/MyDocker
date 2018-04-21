#!/usr/bin/env python
import os

if __name__=="__main__":
    print ("TOKEN: %s" % (os.environ["TOKEN"]))
    print ("SECRET: %s\n" % (os.environ["SECRET"]))
