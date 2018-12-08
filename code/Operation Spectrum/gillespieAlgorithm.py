"""This file contains the Gillespie algorithm to simulate the SIR model and
the function subsample. All code is taken and modified from 
https://epidemicsonnetworks.readthedocs.io/en/latest/_modules/EoN/simulation.html
and
https://epidemicsonnetworks.readthedocs.io/en/latest/functions/EoN.subsample.html
license:


Copyright (c) 2016   Joel C Miller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS OR SPRINGER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import random
import scipy
from collections import defaultdict  # container data type


class _ListDict_(object):
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.item_to_position

    def add(self, item):
        if item in self: 
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items)-1

    def remove(self, choice):
        position = self.item_to_position.pop(choice)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position
            
    def choose_random(self):
        return random.choice(self.items)
        
    def random_removal(self):
        choice = self.choose_random()
        self.remove(choice)
        return choice

    def total_weight(self):
        return len(self)


def Gillespie_SIR(G, tau, gamma, initial_infecteds=None, tmin = 0, tmax=float('Inf')):
    r'''
    
    Performs SIR simulations for epidemics.
    
    :Arguments:
         
    **G** networkx Graph
        The underlying network
        
    **tau** positive float
        transmission rate per edge
       
    **gamma** number
        recovery rate per node
    
    **initial_infecteds** node or iterable of nodes
        
    **tmin** number (default 0)
        starting time
            
    **tmax** number (default Infinity)
        stop time
        
    :Returns: 
        
    **times, S, I, R** each a scipy array
        giving times and number in each status for corresponding time
    
    '''
    
    I = [len(initial_infecteds)]
    R = [0]
    S = [G.order()-I[0]]
    times = [tmin]
    
    t = tmin
    
    status = defaultdict(lambda : 'S')
    
    for node in initial_infecteds:
        status[node] = 'I'
    
    infecteds = _ListDict_() 
    
    IS_links = _ListDict_()

    for node in initial_infecteds:
        infecteds.add(node) 
        for nbr in G.neighbors(node):  
            if status[nbr] == 'S':
                IS_links.add((node, nbr))
    
    total_recovery_rate = gamma*infecteds.total_weight() #gamma*I_weight_sum
    
    total_transmission_rate = tau*IS_links.total_weight()
        
    total_rate = total_recovery_rate + total_transmission_rate
    delay = random.expovariate(total_rate)
    t += delay
    
    while infecteds and t<tmax:
        if random.random()<total_recovery_rate/total_rate: #recover
            recovering_node = infecteds.random_removal()
            status[recovering_node]='R'

            for nbr in G.neighbors(recovering_node):
                if status[nbr] == 'S':
                    IS_links.remove((recovering_node, nbr))
            times.append(t)
            S.append(S[-1])
            I.append(I[-1]-1)
            R.append(R[-1]+1)
        else: #transmit
            transmitter, recipient = IS_links.choose_random()
            status[recipient]='I'

            infecteds.add(recipient)

            for nbr in G.neighbors(recipient):
                if status[nbr] == 'S':
                    IS_links.add((recipient, nbr))
                elif status[nbr] == 'I' and nbr != recipient:
                    IS_links.remove((nbr, recipient))
                     
            times.append(t)
            S.append(S[-1]-1)
            I.append(I[-1]+1)
            R.append(R[-1])
            
        total_recovery_rate = gamma*len(infecteds) #.total_weight()
        total_transmission_rate = tau*IS_links.total_weight()

        total_rate = total_recovery_rate + total_transmission_rate
        if total_rate>0:
            delay = random.expovariate(total_rate)
        else:
            delay = float('Inf')
        t += delay

    return scipy.array(times), scipy.array(S), scipy.array(I), scipy.array(R)


def subsample(report_times, times, status1, status2=None, 
                status3 = None):
    r'''
    Given 
      S, I, and/or R as lists of numbers of nodes of the given status
      at given times

    returns them 
      subsampled at specific report_times.
    

    :Arguments: 

    **report_times** iterable (ordered)
        times at which we want to know state of system
                   
    **times** : iterable (ordered)
        times at which we have the system state (assumed no change 
        between these times)
            
    **status1**  iterable 
        generally S, I, or R
        
        number of nodes in given status at corresponding time in times.
        

    **status2**  iterable  (optional, default None)
        generally S, I, or R
        
        number of nodes in given status at corresponding time in times.

    **status3**  iterable (optional, default None)
        generally S, I, or R
        
        number of nodes in given status at corresponding time in times.
                                
    :Returns:

    If only status1 is defined
        **report_status1** scipy array 
        gives status1 subsampled just at report_times.
                     
    If more are defined then it returns a list, either
        **[report_status1, report_status2]**
    or
        **[report_status1, report_status2, report_status3]**
    In each case, these are subsampled just at report_times.

    '''
    report_status1 = []
    next_report_index = 0
    next_observation_index = 0
    while next_report_index < len(report_times):
        while next_observation_index < len(times) and times[next_observation_index]<= report_times[next_report_index]:
            candidate = status1[next_observation_index]
            next_observation_index += 1
        report_status1.append(candidate)
        next_report_index +=1
        
    report_status1 = scipy.array(report_status1)
    
    if status2 is not None:
        if status3 is not None:
            report_status2, report_status3 = subsample(report_times, times, status2, status3)
            return report_status1, report_status2, report_status3
        else:
            report_status2 = subsample(report_times, times, status2)
            return report_status1, report_status2
    else:
        return report_status1
