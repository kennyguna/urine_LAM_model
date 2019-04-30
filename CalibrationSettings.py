import scipy.stats as stat

SIM_POP_SIZE = 5000      # population size of simulated cohorts
SIM_LENGTH = 10*52        # length of simulation
ALPHA = 0.05             # significance level for calculating confidence intervals
NUM_SIM_COHORTS = 500    # number of simulated cohorts used to calculate prediction intervals

# details of a clinical study estimating the CFR
# OBS_N = 10239	        # number of patients involved in the study
# OBS_DEAD = 4685    # estimated mean survival time
# OBS_ALPHA = 0.05   # significance level

# TEST
OBS_N = 651	        # number of patients involved in the study
OBS_DEAD = 102    # estimated mean survival time
OBS_ALPHA = 0.05   # significance level


# how to sample the posterior distribution of annual mortality probability
# minimum, maximum and the number of samples for the annual mortality probability
POST_L, POST_U, POST_N = 0.5, 1, 10