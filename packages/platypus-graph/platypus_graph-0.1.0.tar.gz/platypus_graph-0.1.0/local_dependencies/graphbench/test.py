#!/usr/bin/env python3
import graphbench
from graphbench import EditGraph, OrdGraph

print(dir(graphbench))

H = EditGraph.from_file('resources/karate.txt.gz')
print(H)
print(H.vertices())

degs = H.degrees()
print(degs)
print(degs[1])