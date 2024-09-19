# Logical Design Optimization

This repository contains a Gurobi implementation of a mathematical optimization problem, based on constructing a logical circuit in the most efficient way possible. This project was inspired by Problem 12 of "Model Building in Mathematical Programming" by H. Paul Williams

## Original Problem from the book
*"Logical circuits have a given number of inputs and one output. Impulses may
be applied to the inputs of a given logical circuit, and it will respond by giving
either an output (signal 1) or no output (signal 0). The input impulses are of the
same kind as the outputs, that is, 1 (positive input) or 0 (no input).
In this example, a logical circuit is to be built up of NOR gates. A NOR
gate is a device with two inputs and one output. It has the property that there
is positive output (signal 1) if and only if neither input is positive, that is, both
inputs have the value 0. By connecting such gates together with outputs from one
gate possibly being inputs into another gate, it is possible to construct a circuit
to perform any desired logical function. For example, the circuit illustrated in
Figure 12.1 will respond to the inputs A and B in the way indicated by the
truth table.*
![image](https://github.com/user-attachments/assets/307a3c87-aa8e-4be5-aee2-c687c1e8a78e)

*The problem here is to construct a circuit using the minimum number of NOR gates that will perform the logical function specified by the truth table in Figure 12.2.*

![image](https://github.com/user-attachments/assets/6c6cefe6-3682-4107-bc9d-5adb5c424302)

*This problem, together with further references to it, is discussed in
Williams (1974), ‘Fan-in’ and ‘fan-out’ are not permitted. That is, more than one output from
a NOR gate cannot lead into one input nor can one output lead into more than
one input.
It may be assumed throughout that the optimal design is a ‘subnet’ of the
‘maximal’ net shown in Figure 12.3.*
![image](https://github.com/user-attachments/assets/e71193f5-941b-445a-a718-5c3de55f3ea4)

## Interpretation
I decided to try solving a more generalized version of this problem. I first imagined a scenario where any number of external logical inputs would be involved with the circuit. I also wanted to consider more than one type of logic gate being utilized in the optimal circuit, specifically the 3 basic logic gates: AND, OR, and NOT. This lead me to work on making a mathematical model for my version of the problem, and to then implement it with the Gurobi solver. As I worked on the problem, I was fascinated by the hypothetical applications for improving various technological devices. After all, our entire understanding of computers is based on the idea of logic gates. I've decided to share my project so others can also have fun with testing the model, along with potentially being inspired to learn more about mathematical optimization

*‘Fan-in’ and ‘fan-out’ are not permitted. That is, more than one output from
a NOR gate cannot lead into one input nor can one output lead into more than
one input.
It may be assumed throughout that the optimal design is a ‘subnet’ of the
‘maximal’ net shown in Figure 12.3."*
![image](https://github.com/user-attachments/assets/5a5bb372-0c19-4b74-b834-e1436bc9193f)
