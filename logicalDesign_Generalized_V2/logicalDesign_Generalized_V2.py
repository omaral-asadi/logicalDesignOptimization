# Author: Omar Al-Asadi
# Date: Sept. 16, 2024
# Description: This program solves for the optimal circuit arrangement for performing specific logic operations.
# This new version works for multiple external outputs.
# Inspired by problem 12 of "Model Building in Mathematical Programming"

from gurobipy import*

# Defines number of AND, OR, and NOT gates
gateNum_AND = 2
gateNum_OR = 2
gateNum_NOT = 2

# Creates sets of logic gates based on initial numbers
logicGates_AND = []
logicGates_OR = []
logicGates_NOT = []
for i in range(gateNum_AND):
    logicGates_AND.append("AND_"+str(i+1))
for i in range(gateNum_OR):
    logicGates_OR.append("OR_"+str(i+1))
for i in range(gateNum_NOT):
    logicGates_NOT.append("NOT_"+str(i+1))

# Defines union of all logic gates
logicGates = logicGates_AND + logicGates_OR + logicGates_NOT

# Defines set of external inputs
externalInputs = ["A","B"]

# Defines set of external outputs
externalOutputs = ["Digit_1","Digit_2"]

# Defines set of inputs for each gate
gateInputs = {}
for i in logicGates:
    # 2 inputs for AND gates
    if i in logicGates_AND:
        gateInputs[i] = ["GateInput_1","GateInput_2"]
    # 2 inputs for OR gates
    elif i in logicGates_OR:
        gateInputs[i] = ["GateInput_1","GateInput_2"]
    # 1 input for NOT gates
    elif i in logicGates_NOT:
        gateInputs[i] = ["GateInput_1"]

# Defines set of scenarios
scenarios = range(4)

# Defines set of external input values for each input, for each scenario
externalInputValues = {
    "A": [0,0,1,1],
    "B": [0,1,0,1],
}

# Defines set of external output values for each output, for each scenario
externalOutputValues = {
    "Digit_1": [0,1,1,0],
    "Digit_2": [0,0,0,1],
}

# Defines size of logic gate set
logicGateNum = len(logicGates)

# Defines function for solving model
def solveModel():
    model = Model("logicalDesign_Generalized")

    # Adds logic gate usage and external output connection  variables to model respectively
    x = model.addVars(logicGates, vtype=GRB.BINARY, name="x")
    t = model.addVars(logicGates, externalOutputs, vtype=GRB.BINARY, name="t")

    # Adds variables for possible direct connection of external inputs to outputs
    r = model.addVars(externalInputs, externalOutputs, vtype=GRB.BINARY, name="r")

    # Adds intergate connection variables to model
    v = {}
    for i in logicGates:
        for k in logicGates:
            for n in gateInputs[k]:
                # Avoids variables for which the gate is connected to itself
                if k != i:
                    v[i, k, n] = model.addVar(vtype=GRB.BINARY, name="v[%s,%s,%s]"%(i,k,n))

    # Adds external input connection variables to model
    u = {}
    for l in externalInputs:
        for i in logicGates:
            for n in gateInputs[i]:
                u[l,i,n] = model.addVar(vtype=GRB.BINARY, name="u[%s,%s,%s]"%(l,i,n))

    # Adds gate output value variables to model
    y = model.addVars(logicGates, scenarios, vtype=GRB.BINARY, name="y")

    # Adds gate input value variables to model
    w = {}
    for i in logicGates:
        for j in scenarios:
            for n in gateInputs[i]:
                w[i,j,n] = model.addVar(vtype=GRB.BINARY, name="w[%s,%s,%s]"%(i,j,n))

    # Adds gate ordering variables to model
    s = model.addVars(logicGates, lb=0, vtype=GRB.INTEGER, name="s")

    # Sets objective to minimize utilized gates
    model.setObjective(
        quicksum(x[i] for i in logicGates),
        GRB.MINIMIZE
    )

    # Adds constraints for correspondance of external output from gate connections
    for i in logicGates:
        for j in scenarios:
            for p in externalOutputs:
                model.addConstr(y[i,j] <= externalOutputValues[p][j] + (1 - t[i,p]), "externalOutputCorrespondanceFromGateConnection_1[%s,%s,%s]"%(i,j,p))
                model.addConstr(y[i,j] >= externalOutputValues[p][j] - (1 - t[i,p]), "externalOutputCorrespondanceFromGateConnection_2[%s,%s,%s]"%(i,j,p))

    # Adds constraints for correspondance of external output from external input connections
    for l in externalInputs:
        for j in scenarios:
            for p in externalOutputs:
                model.addConstr(externalInputValues[l][j] <= externalOutputValues[p][j] + (1 - r[l,p]), "externalOutputCorrespondenceFromExternalInputConnection_1[%s,%s,%s]"%(l,j,p))
                model.addConstr(externalInputValues[l][j] >= externalOutputValues[p][j] - (1 - r[l,p]), "externalOutputCorrespondenceFromExternalInputConnection_2[%s,%s,%s]"%(l,j,p))

    # Requires connection of at least one gate or one external input to each external output
    for p in externalOutputs:
        model.addConstr(
            quicksum(t[i,p] for i in logicGates)
            + quicksum(r[l,p] for l in externalInputs)
            == 1, "externalOutputConnectionRequirement[%s]"%p
        )

    # Creates functionality of AND gates
    for i in logicGates_AND:
        for j in scenarios:
            # (A ^ B) --> C
            model.addConstr(quicksum(1 - w[i,j,n] for n in gateInputs[i]) + y[i,j] >= 1,"ANDGateFunctionality_1[%s,%s]"%(i,j))

            # C --> (A ^ B)
            for n in gateInputs[i]:
                model.addConstr(y[i,j] <= w[i,j,n], "ANDGateFunctionality_2[%s,%s,%s]"%(i,j,n))

    # Creates functionality of OR gates
    for i in logicGates_OR:
        for j in scenarios:
            # (A v B) --> C
            for n in gateInputs[i]:
                model.addConstr(w[i,j,n] <= y[i,j], "ORGateFunctionality_1[%s,%s,%s]"%(i,j,n))

            # C --> (A v B)
            model.addConstr((1 - y[i,j]) + quicksum(w[i,j,n] for n in gateInputs[i]) >= 1, "ORGateFunctionality_2[%s,%s]"%(i,j))

    # Creates functionality of NOT gates
    for i in logicGates_NOT:
        for j in scenarios:
            # A <--> ~B
            model.addConstr(y[i,j] == 1 - w[i,j,gateInputs[i][0]], "NOTGateFunctionality[%s,%s]"%(i,j))

    # Adds constraints for logical correspondance from intergate connections
    for i in logicGates:
        for k in logicGates:
            # Avoids constraints for which both gates are the same
            if k != i:
                for j in scenarios:
                    for n in gateInputs[k]:
                        model.addConstr(y[i,j] >= w[k,j,n] - (1 - v[i,k,n]), "gateConnectionCorrespondance_1[%s,%s,%s,%s]"%(i,k,j,n))
                        model.addConstr(y[i,j] <= w[k,j,n] + (1 - v[i,k,n]), "gateConnectionCorrespondance_2[%s,%s,%s,%s]"%(i,k,j,n))

    # Adds constraints for logical correspondance from external input connection
    for i in logicGates:
        for j in scenarios:
            for l in externalInputs:
                for n in gateInputs[i]:
                    model.addConstr(w[i,j,n] <= externalInputValues[l][j] + (1 - u[l,i,n]), "externalInputCorrespondance_1[%s,%s,%s,%s]"%(i,j,l,n))
                    model.addConstr(w[i,j,n] >= externalInputValues[l][j] - (1 - u[l,i,n]), "externalInputCorrespondance_2[%s,%s,%s,%s]"%(i,j,l,n))

    # Adds constraints for implication of gate usage from external or intergate connections
    for i in logicGates:
        # Implication from intergate connection
        for k in logicGates:
            # Avoids constraints for which the gate is connected to itself
            if k!=i:
                # Implication from outgoing connection
                for n in gateInputs[k]:
                    model.addConstr(x[i] >= 1 - (1 - v[i,k,n]), "gateUsageImplication_1[%s,%s,%s]"%(i,k,n))

                # Implication from incoming connection
                for n in gateInputs[i]:
                    model.addConstr(x[i] >= 1 - (1 - v[k,i,n]), "gateUsageImplication_2[%s,%s,%s]"%(k,i,n))
        # Implication from external input connection
        for l in externalInputs:
            for n in gateInputs[i]:
                model.addConstr(x[i] >= 1 - (1 - u[l,i,n]), "gateUsageImplication_3[%s,%s,%s]"%(i,k,n))

        # Implication from external output connection
        for p in externalOutputs:
            model.addConstr(x[i] >= 1 - (1 - t[i,p]), "gateUsageImplication_4[%s,%s]"%(i,p))

    # Adds constraints for requirement of gate input and output decisions from gate usage
    for i in logicGates:
        # Requirement for input decisions
        for n in gateInputs[i]:
            model.addConstr(
                quicksum(v[k,i,n] for k in logicGates if k != i)
                + quicksum(u[l,i,n] for l in externalInputs)
                >= 1 - (1 - x[i]), "gateInputDecisionRequirement[%s,%s]"%(i,n)
            )

        # Requirement for output decisions
        model.addConstr(
            quicksum(
                quicksum(v[i,k,n] for n in gateInputs[k])
                for k in logicGates if k != i
            ) + quicksum(t[i,p] for p in externalOutputs)
            >= 1 - (1 - x[i]),
            "gateOutputDecisionRequirement[%s]"%i
        )

    # Adds constraints to prevent circular dependency
    for i in logicGates:
        for k in logicGates:
            # Avoids constraint for when gate is connected to itself
            if k != i:
                for n in gateInputs[k]:
                    model.addConstr(s[k] >= 1 + s[i] - logicGateNum*(1 - v[i,k,n]), "circularDependencyBreakage[%s,%s,%s]"%(i,k,n))

    # Optimize and return results
    model.optimize()
    return model, x, t, r, v, u, y, w, s

# Defines function for displaying results
def displayOutput(model, x, t, r, v, u, y, w, s):
    print("\n_________________________________________________________________________________")
    print("Results:")

    # Outputs gates utilized
    print("_________________________________________________________________________________")
    print("Gates Utilized:")
    for i in x:
        if x[i].x >= 0.5:
            print(i)

    # Outputs external output gate connections
    print("_________________________________________________________________________________")
    print("Gate to External Outputs Connections:")
    for i, p in t:
        if t[i,p].x >= 0.5:
            print(f"Connect {i} to {p}")

    # Outputs direct connections from external inputs to external outputs
    print("_________________________________________________________________________________")
    print("External Inputs to External Outputs Connections:")
    for l, p in r:
        if r[l,p].x >= 0.5:
            print(f"Connect {l} to {p}")

    # Outputs intergate connections
    print("_________________________________________________________________________________")
    print("Intergate Connections:")
    for i, k, n in v:
        if v[i,k,n].x >= 0.5:
            print(f"Connect {i} to {k} via {n}")

    # Outputs external input connections
    print("_________________________________________________________________________________")
    print("External Inputs to Gate Connections:")
    for l, i, n in u:
        if u[l,i,n].x >= 0.5:
            print(f"Connect {l} to {i} via {n}")

    # Outputs gates utilized
    print("_________________________________________________________________________________")
    print("Total Gates:",model.objVal)

# Defines function for outputing analysis of each gate under each scenario
def scenarioAnalysis(model, x, t, v, u, y, w, s):
    # Outputs for each scenario
    for j in scenarios:
        print("")
        print("Scenario",j+1)

        # Outputs desired input and output values for the scenario
        for l in externalInputs:
            print(l,"=",externalInputValues[l][j])
        for p in externalOutputs:
            print(p,"=",externalOutputValues[p][j])

        # Outputs input and output values for each logic gate under the scenario
        for i in logicGates:
            if x[i].x >= 0.5:
                print(i)
                for n in gateInputs[i]:
                    print(n,"=",w[i,j,n].x)
                print("Output =",y[i,j].x)

# Defines function for outputting analysis of logic gate ordering
def orderAnalysis(model, x, t, v, u, y, w, s):
    for i in x:
        if x[i].x >= 0.5:
            print(i, s[i].x)

def main():
    model, x, t, r, v, u, y, w, s = solveModel()
    displayOutput(model, x, t, r, v, u, y, w, s)

    # Asks user if they wish to do scenario analysis
    action = input("Do you wish to perform scenario analysis on the gates? (y/n): ")
    action = action.upper()
    if action=="Y":
        scenarioAnalysis(model, x, t, v, u, y, w, s)

    # Asks user if they wish to do order analysis
    action = input("Do you wish to perform order analysis on the gates? (y/n): ")
    action = action.upper()
    if action=="Y":
        orderAnalysis(model, x, t, v, u, y, w, s)
main()
