# Introduction
The code in this repository server as a simple tool to periodically compute a portfolio that approximates Vanguard's VWCE etf using ishares' SWDA etf and Xtrackers' XMME etf.

The main reasons behind this exercise are mainly two:

    1. since I recently began eanring a salary, I wanted to periodically invest some of it in the VWCE fund, however my broker charges a small commission when purchasing this title, whilst some other titles (including SWDA and XMME) are free of charge. The commission charged is small, however, I took the opportunity to carry out this small project.

    2. I am trying to improve some skills about my interests, including programming, data analysis and understanding of the financial markets. Consequently, this small project allowed me to tackle all these topics learning small interesting things (e.g. i never had to interact with GitHub's actions for cloud batch deployment neither had I had the need to understand how to connect to Google cloud's API services).

Moreover, I was happy to solve this problem with an optimization algorithm, which reminds me of my student career as a mathematician!
A small viable development of this small project is to add some notebooks with some backlog tests of the obtained portfolio, so as to learn something about financial quantitative analysis and risk analysis applied to something that interests me in first person: my own savings!

In the following you can find a description of the structure of the repo, an explanation of its modules and a brief mathematical formulation of the optimization problem this whole project can be reduced to.

## File structure

## VWCE approximation as a linear programming problem
Let $\alpha, \beta$ be the vectors of allocation of the SWDA and of the XMME etfs, and let $\gamma$ be the vector of allocation of the VWCE etf. Here we interpret the geographical allocations of the three funds as $d$-dimensional vectors, where $d$ is the common support of the three funds (e.g. the union of the geographical countries that compose the three titles).
We want to minimize the following function

$$
f\colon \mathbb R^2 \to \mathbb R\\
(x,y)\mapsto ||(\alpha, \beta)\cdot (x,y)^\top - \gamma||^2
$$

which is convex. This is a simple convex linear programming problem, where the unknown parameters $\alpha, \beta$ must satisfy the linear constraint $\alpha + \beta = 1$. 
We use a standard optimizator from the library scipy/optimize for this problem.

## Batching

The source code inside src is meant to be periodically run (once every month)