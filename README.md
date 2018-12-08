# Modeling and Simulation of Social Systems Fall 2018 – Research Plan

> * Group Name: Operation Spectrum
> * Group participants names: Hahn Thomas, Jäger Severin, Schubert Yannick
> * Project Title: Modeling and Simulation Disease Outbreaks for Arbitrary Topological Systems
> * Programming language: Python

## General Introduction

The social sciences have long tried to predict the time evolution propagation of viruses,
ideas, etc.  Obviously, a deep understanding of how and why diseases spread would allow
us to better come up with prevention measures. Their first attempt was to parametrize the
disease and analyze the spreading during short time-steps.  The topology of the system,
i.e.  a  structure  that  describes  the  connection  between all  players,  was
completely ignored.  It  was just  assumed that everyone  knew everyone.  More recently,
experts in this field have managed to not only create a theory that includes both aspects,
but also achieve a decoupling.  This, of course, is by no means trivial.
We  will  base  our  work  on  the  paper  ’Threshold  Conditions  for  Arbitrary  Cascade
Models  on  Arbitrary  Networks”  from  2012 .  They  claim  to  be  the  first  ones  to  de-
couple the virus propagation model form the topology of the network.  There, they define
a virus strength as the product of the largest eigenvalue of the connectivity matrix and a
constant, which only depends on the virus propagation model.


## The Model

The G2-Threshold Theorem, which is formulated and proven in the paper, states that
there exists a threshold for the effective strength below which a virus dies out quickly.  For
many “what-if”-scenarios this is already the necessary information.  Since there exist very
fast algorithms for computing the largest eigenvalue of a matrix, this information can be
obtained quickly for an arbitrary virus propagation model and an arbitrary topology.


## Fundamental Questions

In this paper,  we will investigate whether the G2-Theorem still applies for different
initial conditions. Thereto, we will vary the number of initially infected nodes in a network
and  infect  its  most  important  nodes.   Additionally,  we  will  figure  out,  whether  virus
propagation in very small networks can still be analyzed with this theorem.


## Expected Results

In general, we expect the model to work just fine, but we will try to figure out whether it fails for some initial conditions.


## References 

B.  Aditya  Prakash,  Deepayan  Chakrabarti,  Nicholas  Valler,  Michalis  Faloutsos,
Christos Faloutsos.  Threshold conditions for arbitrary cascade models on arbitrary
networks.   Knowledge  and  Information  Systems  manuscript  No.  KAIS-12-3483R1,
2012

Istvan Z. Kiss, Joel C. Miller, P ́eter L. Simon. Mathematics  of  Epidemics  on  Networks, volume 46.  Springer, Cham, 2017


## Research Methods

SIR simulations using the Gillespie Algorithm to reproduce and challenge the model.


## Data sets

AS-OREGON: Graph of Internet´s Autonomous Systems collected by University of Oregon Route Views Project

	as20000102.txt	data from January 02, 2000 downloaded from https://snap.stanford.edu/data/as-733.html
	
	as20010331.txt  data from March 31, 2001 downloaded from http://topology.eecs.umich.edu/data.html
	
facebook_ego.txt: Data from a survey on Facebook app usage. Downloaded from https://snap.stanford.edu/data/ego-Facebook.html

terrorists.txt: Social associations between terrorists involved in the 9/11 attacks. Downloaded from http://tuvalu.santafe.edu/~aaronc/datacode.htm
	

# Reproducibility

## Light test

Make sure you have the following libraries installled: scipy, matplotlib, networkx

The file lightTest.py contains the codes used to generate the plots in the results section of the report and can therefore be used for reproduction.


## Full test

Make sure you have the following libraries installled: scipy, matplotlib, networkx, EoN

The file fullTest.py contains the codes used to generate the plots in the results section of the report and can therefore be used for reproduction.

