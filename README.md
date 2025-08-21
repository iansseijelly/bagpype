# Bagpipe: Better Academic Graphs for Processor Pipelines

This repo implements a python library for describing and visualizing processor pipeline diagrams. 

## Components

### Instructions
An instruction is visualized as one row in the view. It can contain an arbitrary number of nodes. 

### Nodes
A node is an event, represented as a single square in the view. Its x-axis position is determined by its time, and its y-axis position is determined by its parent instruction.
One should be able to address a node by I0.Issue, for example.

### Edges
An edge connecting nodes. One should be able to use a special operator, `>>` to specify this dependency. I should be able to chain arbitrary number of dependencies in a single line. 