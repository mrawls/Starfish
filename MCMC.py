#!/usr/bin/env python
"""
Sample the discretized grid using emcee.
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
import emcee
import sys
from model import lnprob
#from emcee.utils import MPIPool

def main():
    #11 dimensional model, 200 walkers
    ndim = 7
    nwalkers = 150

    # Choose an initial set of positions for the walkers, randomly distributed across a reasonable range of parameters.
    temp = np.random.uniform(low=5200, high = 6600, size=(nwalkers,))
    logg = np.random.uniform(low=2.5, high=4.2, size=(nwalkers,))
    #M = np.random.uniform(low=0.1, high = 10, size=(nwalkers,))
    #R = np.random.uniform(low=0.1, high = 10, size=(nwalkers,))
    #Av = np.random.uniform(low=0, high = 8, size=(nwalkers,))
    vsini = np.random.uniform(low=35, high = 55, size=(nwalkers,))
    vz = np.random.uniform(low=27, high = 29.5, size=(nwalkers,))
    flux_factor = np.random.uniform(low=1.e-28, high = 1.e-27, size=(nwalkers,))
    c1 = np.random.uniform(low=-0.1, high = 0.1, size=(nwalkers,))
    c2 = np.random.uniform(low=-0.1, high = 0.1, size=(nwalkers,))
    #c3 = np.random.uniform(low=-0.01, high = 0.01, size=(nwalkers,))
    #c4 = np.random.uniform(low=-0.01, high = 0.01, size=(nwalkers,))

    p0 = np.array([temp,logg,vsini,vz,flux_factor,c1,c2]).T

    # Initialize the MPI-based pool used for parallelization.
    #pool = MPIPool()
    #print("Running with MPI")

    #if not pool.is_master():
    #    # Wait for instructions from the master process.
    #    pool.wait()
    #    sys.exit(0)

    # Initialize the sampler with the chosen specs.
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob,threads=64)

    # Burn-in.
    pos, prob, state = sampler.run_mcmc(p0, 2000)

    print("Burned in chain")
    # Reset the chain to remove the burn-in samples.
    sampler.reset()

    # Starting from the final position in the burn-in chain, sample for 1000
    # steps.
    #f = open("chain.dat", "w")
    #f.close()
    sampler.run_mcmc(pos, 2000, rstate0=state)
    #    position = result[0]
    #    f = open("chain.dat", "a")
    #    for k in range(position.shape[0]):
    #        f.write("{0:4d} {1:s}\n".format(k, " ".join(position[k])))
    #    f.close()

    # Print out the mean acceptance fraction. In general, acceptance_fraction
    # has an entry for each walker so, in this case, it is a 250-dimensional
    # vector.
    print("Mean acceptance fraction:", np.mean(sampler.acceptance_fraction))

    #write chain to file
    np.save("output/chain.npy", sampler.chain)
    #write lnprob to file
    np.save("output/lnprobchain.npy", sampler.lnprobability)

if __name__=="__main__":
    main()
