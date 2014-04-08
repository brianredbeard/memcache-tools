#!/usr/bin/python

import sys
import memcache
import random

memcachehost=sys.argv[1]

print "sending values to %s" % memcachehost
client = memcache.Client([memcachehost])

for x in range(100,999):
    newrand = random.randint(100,999)
    testkey="mykey%s" % x
    sample_obj = {"lang": "python", "value": newrand}
    client.set(testkey, sample_obj, time=24800)

print "stored value to memcache"
newrand = random.randint(100,999)

print "mykey%s:" % newrand
print client.get("mykey%s" % newrand)
