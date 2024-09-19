# Overview
This is the first version of the optimization model that I created:

Lets assume we have a generalized set of external logical inputs, along with a generalized set of logic gates. The logic gates can be further seperated into AND, OR, and NOT gates. Each possible scenario for the logical input values corresponds to a desired output value for the overall logical circuit. For example, we may wish to construct a circuit to fullfill the following truth table:

| A  | B | C | Output |
| :---: | :---: | :---: | :---: |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 |
