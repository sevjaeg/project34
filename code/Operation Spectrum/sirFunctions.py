"""Provides functions to run SIR simulations"""

import EoN  # library providing tools to run fast SIR simulations using the Gillespie algorithm
import random
import scipy
import multiprocessing as mp
import matplotlib.pyplot as plt
from calculateLambda import obtainMaxEig
from joblib import Parallel, delayed


def s_SIR(eig, beta, delta, digits):  # Effective virus strength
    """Returns the effective virus strength of a SIR model on a graph

    Arguments:
        eig -- the largest eigenvalue of the adjacency matrix belonging to the respective network
        beta -- the transmission probability in the SIR model
        delta -- the healing probability once infected in the SIR model
        digits -- the rounding accuracy of the returned result
    """

    return round(eig*beta/delta, digits)


def time_evolution(G, beta, delta, initial_size, start_time, end_time, iterations, label, opt = 'Plot', initial_nodes = []):
    """Calculates the time evolution of a SIR model using the Gillespie algorithm by averaging over several independent simulations

    Arguments:
        G -- a networkX graph object describing the system topology
        beta -- the transmission probability in the SIR model
        delta -- the healing probability once infected in the SIR model
        initial_size -- the initial size of the infected population
        start_time -- the simulation start time
        end_time -- the simulation end time
        iterations -- the number of independent simulations (the average value is returned)
        label -- the label of the curve in the crated graph
        opt -- determines what is returned (default: 'Plot'):
            'Plot' -- a double logarithmic plot (using matplotlib) is created
            'number_of_cured_nodes' --
        initial_nodes -- the indices of the initially infected nodes, randomly chosen if empty list (default: [])
    """

    report_times = scipy.linspace(start_time, end_time, 1000)
    Isum = scipy.zeros(len(report_times))
    Rsum = scipy.zeros(len(report_times))
    for i in range(iterations):
        if not initial_nodes:
            initial_nodes = random.sample(G.nodes, initial_size)
        else:
            initial_nodes = initial_nodes
        t, S, I, R = EoN.Gillespie_SIR(G, beta, delta, initial_infecteds=initial_nodes)
        _, newI, newR = EoN.subsample(report_times, t, S, I, R)
        Isum += newI
        Rsum += newR
    I_average = Isum / float(iterations)
    R_average = Rsum / float(iterations)
    if (opt == 'Plot'):
        plt.loglog(report_times, I_average/(len(G)), label = label, linewidth = 2)
    elif (opt == 'number_of_cured_nodes'):
        return R_average[-1]
    else:
        print("Invalid 'opt' parameter passed!")


def fig_5_left(G, initial_size, iterations, initial_nodes  = [], beta = [0.15, 0.05, 0.02, 0.01], delta =[1, 1, 1, 1]):
    """Plots the infective fraction of a population vs time using an SIR simulation on a graph with multiple iterations and averaging

        Arguments:
            G -- a networkX graph object describing the system topology
            initial_size -- the initial size of the infected population
            iterations -- the number of independent simulations (the average value is returned)
            initial_nodes -- the indices of the initially infected nodes, randomly chosen if empty list (default: [])
            beta -- array of SIR beta values, same length as delta (default: [1, 1, 1, 1])
            delta -- array of SIR delta values, same length as beta (default: [0.15, 0.05, 0.02, 0.01])
    """

    eig = obtainMaxEig(G)
    digits = 3
    start_time = 0
    end_time = 1000

    label1 = r's = ' + str(s_SIR(eig, beta[0], delta[0], digits))
    label2 = r's = ' + str(s_SIR(eig, beta[1], delta[1], digits))
    label3 = r's = ' + str(s_SIR(eig, beta[2], delta[2], digits))
    label4 = r's = ' + str(s_SIR(eig, beta[3], delta[3], digits))
    time_evolution(G, beta[0], delta[0], initial_size, start_time, end_time,
                   iterations, label1, initial_nodes = initial_nodes)
    time_evolution(G, beta[1], delta[1], initial_size, start_time, end_time,
                   iterations, label2, initial_nodes = initial_nodes)
    time_evolution(G, beta[2], delta[2], initial_size, start_time, end_time,
                   iterations, label3, initial_nodes = initial_nodes)
    time_evolution(G, beta[3], delta[3], initial_size, start_time, end_time,
                   iterations, label4, initial_nodes = initial_nodes)
    plt.legend()
    plt.xlabel("Time ticks")
    plt.ylabel("Fraction of Infected People")
    plt.grid()
    if initial_nodes:
        plt.savefig('build/fig_5_left_crucial.png')
    else:
        plt.savefig('build/fig_5_left_random.png')
    plt.show()


def fig_5_right(G, initial_size, iterations, number_of_steps, initial_nodes = [], parallel = False, show = True):
    """Plots the virus footprint vs effective virus strength using an SIR simulation on a graph with multiple iterations and averaging

        Arguments:
            G -- a networkX graph object describing the system topology
            initial_size -- the initial size of the infected population
            iterations -- the number of independent simulations (the average value is returned)
            number_of_steps -- number of different virus strenghts (along x-axis)
            initial_nodes -- the indices of the initially infected nodes, randomly chosen if empty list (default: [])
            parallel -- states whether parallelized for loops from joblib are used, potentially causing problems (default: False)
            show -- determines whether the plot is shown
    """

    start_time = 0
    end_time = 100
    eig = obtainMaxEig(G)
    beta_range = scipy.logspace(-2, 2, number_of_steps)
    final_number_of_cured_nodes = scipy.zeros_like(beta_range)
    if parallel:
        final_number_of_cured_nodes = Parallel(n_jobs=mp.cpu_count())(
            delayed(time_evolution)(G, beta, eig, initial_size, start_time, end_time, iterations, "Hi",
                                    opt='number_of_cured_nodes', initial_nodes=initial_nodes) for i, beta in enumerate(beta_range))
    else:
        for i, beta in enumerate(beta_range):
            final_number_of_cured_nodes[i] = time_evolution(G, beta, eig, initial_size, start_time, end_time, iterations, "Hi", opt ='number_of_cured_nodes', initial_nodes = initial_nodes)
    plt.semilogx(beta_range, final_number_of_cured_nodes, linewidth = 2)
    plt.grid()
    plt.xlabel(r'Effective Strength of Virus $\lambda_1\beta/\delta$')
    plt.ylabel("Final Number of Cured Nodes")
    if initial_nodes:
        plt.savefig('build/fig_5_right_crucial.png')
    else:
        plt.savefig('build/fig_5_right_random.png')
    if(show):
        plt.show()


def fig_5_right_initial(G, initial_sizes, iterations, number_of_steps, initial_nodes = [], parallel = False, show = True):
    """Plots multple virus footprint vs effective virus strength graphs with different initial infected populations
       using an SIR simulation on a graph with multiple iterations and averaging

        Arguments:
            G -- a networkX graph object describing the system topology
            initial_sizes -- list of initial sizes of infected population, each leading to curve in the plot
            iterations -- the number of independent simulations (the average value is returned)
            number_of_steps -- number of different virus strenghts (along x-axis)
            initial_nodes -- the indices of the initially infected nodes, randomly chosen if empty list (default: [])
            parallel -- states whether parallelized for loops from joblib are used, potentially causing problems (default: False)
            show -- determines whether the plot is shown
    """

    start_time = 0
    end_time = 10
    eig = obtainMaxEig(G)
    beta_range = scipy.logspace(-2, 2, number_of_steps)
    final_number_of_cured_nodes = scipy.zeros_like(beta_range)
    for j in range(len(initial_sizes)):
        if parallel:
            if not initial_nodes:
                final_number_of_cured_nodes = Parallel(n_jobs=mp.cpu_count())(
                    delayed(time_evolution)(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "",
                                            opt='number_of_cured_nodes') for i, beta in enumerate(beta_range))
            else:
                final_number_of_cured_nodes = Parallel(n_jobs=mp.cpu_count())(
                    delayed(time_evolution)(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "",
                                            opt='number_of_cured_nodes', initial_nodes=initial_nodes[j]) for i, beta in enumerate(beta_range))
        else:
            for i, beta in enumerate(beta_range):
                if not initial_nodes:
                    final_number_of_cured_nodes[i] = time_evolution(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "", opt='number_of_cured_nodes')
                else:
                   final_number_of_cured_nodes[i] = time_evolution(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "", opt='number_of_cured_nodes',
                                                                    initial_nodes=initial_nodes[j])
        plt.semilogx(beta_range, final_number_of_cured_nodes, label = str(initial_sizes[j]) + " nodes", linewidth = 2)
    plt.grid()
    plt.legend()
    plt.xlabel(r'Effective Strength of Virus $\lambda_1\beta/\delta$')
    plt.ylabel("Final Number of Cured Nodes")
    plt.grid()
    if initial_nodes:
        plt.savefig('build/fig_5_right_initial_crucial.png')
    else:
        plt.savefig('build/fig_5_right_initial_random.png')
    if(show):
        plt.show()
