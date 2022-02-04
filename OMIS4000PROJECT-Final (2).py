#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 15:55:03 2021

@author: danielsydorenko
"""

import pulp as pulp

# Formulating physician scheduling optimization problem.
model = pulp.LpProblem("PhysicianScheduling", pulp.LpMaximize)

# Constructing dictionary variable for physicians.
x = {}

# Number of physicians.
P = 28

# Number of shifts.
S = 3

# Number of days.
D = 7

# Defining the x variable (whether or not physician i is assigned to shift j on day k).
for i in range(P):
    for j in range(S):
        for k in range(D):
            x[i,j,k] = pulp.LpVariable("x(%s,%s,%s)" % (i,j,k), cat = "Binary")
            
# Formulating the objective function for the optimization problem.
model += 26*x[19,j,k] + 23*x[13,j,k] + 20.5*x[4,j,k] + 20*x[12,j,k] + 19*x[23,j,k] + 18.5*x[2,j,k] + 17*x[5,j,k] + 16.5*x[8,j,k] \
    + 16*x[18,j,k] + 15.5*x[20,j,k] + 15*x[21,j,k] + 15*x[22,j,k] + 15*x[25,j,k] + 14.5*x[24,j,k] + 14*x[16,j,k] + 14*x[26,j,k] \
    + 13.5*x[15,j,k] + 13.5*x[17,j,k] + 13*x[6,j,k] + 12.5*x[27,j,k] + 12*x[1,j,k] + 12*x[9,j,k] + 11*x[10,j,k] + 10.5*x[14,j,k] \
    + 8.5*x[0,j,k] + 8.5*x[3,j,k] + 8*x[11,j,k] + 3.5*x[7,j,k]

# CONSTRAINTS

#for k in range(D) and if loop that runs through the physicians and compares them to an average per shift 
#sum of all physicians assigned as per the prf metric should be greater than equal to a number 
    
# Amount of physicians 

#lesser assignment of physicians on weekends 

for r in range(0,1):
    model += pulp.lpSum([x[i,0,r]] for i in range(P)) >= 2  
    model += pulp.lpSum([x[i,0,r]] for i in range(P)) <= 4

   
    model += pulp.lpSum([x[i,1,r]] for i in range(P)) >= 1
    model += pulp.lpSum([x[i,1,r]] for i in range(P)) <= 4

 
    model += pulp.lpSum([x[i,2,r]] for i in range(P)) >= 1
    model += pulp.lpSum([x[i,2,r]] for i in range(P)) <= 3  

for r in range(1,7):
    model += pulp.lpSum([x[i,0,r]] for i in range(P)) >= 3
    model += pulp.lpSum([x[i,0,r]] for i in range(P)) <= 5
   
    model += pulp.lpSum([x[i,1,r]] for i in range(P)) >= 2
    model += pulp.lpSum([x[i,1,r]] for i in range(P)) <= 5

    model += pulp.lpSum([x[i,2,r]] for i in range(P)) >= 2
    model += pulp.lpSum([x[i,2,r]] for i in range(P)) <= 4



# Physician preference constraint.
for k in range(D):
    model += x[2,0,k] == 0
for k in range(D):
    model += x[17,1,k] == 0
for k in range(D):
    model += x[18,1,k] == 0
for k in range(D):
    model += x[18,2,k] == 0
for k in range(D):
    model += x[19,1,k] == 0
for k in range(D):
    model += x[19,2,k] == 0
for k in range(D):
    model += x[6,2,k] == 0
for k in range(D):
    model += x[12,2,k] == 0
for k in range(D):
    model += x[15,2,k] == 0
for k in range(D):
    model += x[17,2,k] == 0

# Next day constraint. (how to code for same i?)
for i in range(P):
      model += x[i,2,0] + x[i,0,1] <= 1

for i in range(P):
      model += x[i,2,1] + x[i,0,2] <= 1    

for i in range(P):
      model += x[i,2,2] + x[i,0,3] <= 1 
     
for i in range(P):
      model += x[i,2,3] + x[i,0,4] <= 1

for i in range(P):
      model += x[i,2,4] + x[i,0,5] <= 1    

for i in range(P):
    model += x[i,2,5] + x[i,0,6] <= 1 
    
for i in range(P):
      model += x[i,2,6] + x[i,0,0] <= 1
    
# Consecutive shift constraint. 
for i in range(P):
      for k in range(D):
         model += x[i,0,k] + x[i,1,k] <= 1

for i in range(P):
     for k in range(D):
        model += x[i,1,k] + x[i,2,k] <= 1

# Every physician must work at least once.

for w in range(P):
    model += pulp.lpSum([x[w,j,k]] for j in range(S) for k in range(D)) >= 1 



# Solve our model.
model.solve()

# Display variable values.
    
for variable in model.variables():
    if variable.varValue > 0: 
        print ("{} = {}".format(variable.name, variable.varValue))
        
    
print(pulp.LpStatus[model.status])
print(pulp.value(model.objective))



