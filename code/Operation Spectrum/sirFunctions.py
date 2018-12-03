"""Provides functions to run the SIR simulation in sirSimulation.py"""

import EoN  # library providing tools to run fast SIR simulations using the Gillespie algorithm
import random
import scipy
import multiprocessing as mp
import matplotlib.pyplot as plt
from calculateLambda import obtainMaxEig
from joblib import Parallel, delayed


def s_SIR(eig, beta, delta, digits):  # Effective virus strength
    return round(eig*beta/delta, digits)


def time_evolution(G, beta, delta, initial_size, start_time, end_time, iterations, label, opt = 'Plot', initial_nodes = []):
    report_times = scipy.linspace(start_time, end_time, 1000)
    Isum = scipy.zeros(len(report_times))
    Rsum = scipy.zeros(len(report_times))
    for i in range(iterations):
        if not initial_nodes:
            initial_nodes = random.sample(G.nodes, initial_size)
        else:
            initial_nodes = initial_nodes
        t, S, I, R = EoN.fast_SIR(G, beta, delta, initial_infecteds=initial_nodes)
        _, newI, newR = EoN.subsample(report_times, t, S, I, R)
        Isum += newI
        Rsum += newR
    I_average = Isum / float(iterations)
    R_average = Rsum / float(iterations)
    if (opt == 'Plot'):
        plt.loglog(report_times, I_average/(len(G)), label = label, linewidth = 5)
    if (opt == 'number_of_cured_nodes'):
        return R_average[-1]


def fig_5_left(G, initial_size, iterations, initial_nodes  = []):
    eig = obtainMaxEig(G)
    digits = 2
    start_time = 0
    end_time = 100
    beta1, beta2, beta3, beta4 = 0.15, 0.05, 0.02, 0.01
    delta1, delta2, delta3, delta4 = 1, 1, 1, 1
    label1 = r'over-1, $\beta$ = '+ str(beta1)+', $\delta$ = ' + str(delta1) + ', s = ' + str(s_SIR(eig, beta1, delta1, digits))
    label2 = r'over-2, $\beta$ = '+ str(beta2)+', $\delta = $' + str(delta2)+ ', s = ' + str(s_SIR(eig, beta2, delta2, digits))
    label3 = r'under-1, $\beta$ = '+ str(beta3)+', $\delta = $' + str(delta3)+ ', s = ' + str(s_SIR(eig, beta3, delta3, digits))
    label4 = r'under-2, $\beta$ = '+ str(beta4)+', $\delta = $' + str(delta4)+ ', s = ' + str(s_SIR(eig, beta4, delta4, digits))
    time_evolution(G, beta1, delta1, initial_size, start_time, end_time,
                   iterations, label1, initial_nodes = initial_nodes)
    time_evolution(G, beta2, delta2, initial_size, start_time, end_time,
                   iterations, label2, initial_nodes = initial_nodes)
    time_evolution(G, beta3, delta3, initial_size, start_time, end_time,
                   iterations, label3, initial_nodes = initial_nodes)
    time_evolution(G, beta4, delta4, initial_size, start_time, end_time,
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


def fig_5_right(G, initial_size, iterations, number_of_steps, initial_nodes = [], parallel = False):
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
    plt.semilogx(beta_range, final_number_of_cured_nodes)
    plt.grid()
    plt.xlabel(r'Effective Strength of Virus $\lambda_1\beta/\delta$')
    plt.ylabel("Final Number of Cured Nodes")
    plt.grid()
    if initial_nodes:
        plt.savefig('build/fig_5_right_crucial.png')
    else:
        plt.savefig('build/fig_5_right_random.png')
    plt.show()


def fig_5_right_initial(G, initial_sizes, iterations, number_of_steps, initial_nodes = [], parallel = False):
    start_time = 0
    end_time = 10
    eig = obtainMaxEig(G)
    beta_range = scipy.logspace(-2, 2, number_of_steps)
    final_number_of_cured_nodes = scipy.zeros_like(beta_range)
    for j in range(0, len(initial_sizes)):
        if parallel:
            if not initial_nodes:
                final_number_of_cured_nodes = Parallel(n_jobs=mp.cpu_count())(
                    delayed(time_evolution)(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "",
                                            opt='number_of_cured_nodes') for i, beta in enumerate(beta_range))
            else:
                final_number_of_cured_nodes = Parallel(n_jobs=mp.cpu_count())(
                    delayed(time_evolution)(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "",
                                            opt='number_of_cured_nodes') for i, beta in enumerate(beta_range))
        else:
            for i, beta in enumerate(beta_range):
                if not initial_nodes:
                    final_number_of_cured_nodes[i] = time_evolution(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "", opt='number_of_cured_nodes',
                                                                    initial_nodes=initial_nodes[j])
                else:
                   final_number_of_cured_nodes[i] = time_evolution(G, beta, eig, initial_sizes[j], start_time, end_time, iterations, "", opt='number_of_cured_nodes',
                                                                    initial_nodes=initial_nodes[j])
        plt.semilogx(beta_range, final_number_of_cured_nodes, label = str(initial_sizes[j]) + " nodes")
    plt.grid()
    plt.legend()
    plt.xlabel(r'Effective Strength of Virus $\lambda_1\beta/\delta$')
    plt.ylabel("Final Number of Cured Nodes")
    plt.grid()
    if initial_nodes:
        plt.savefig('build/fig_5_right_initial_crucial.png')
    else:
        plt.savefig('build/fig_5_right_initial_random.png')
    plt.show()
