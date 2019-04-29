
# simulation settings
N_COHORTS = 20  # number of cohorts
POP_SIZE = 5000     # cohort population size
SIM_LENGTH = 10*52   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

# # annual probability of background mortality (number per year per 1,000 population)
# ANNUAL_PROB_BACKGROUND_MORT = 8.15 / 1000

# rate transition matrix
# CONSIDER MAKING CLEARED_TBM WITH A LOWER HEALTH UTILITY GIVEN ADVERSE SEQUELAE OF TBM
# SOC_RATE_TRANS_MATRIX = [
#     [0, 1/160,  7/480,     1/48,          0,      1/24,       0],   # INFECTED
#     [0,     0,      0,  141/250,    109/250,         0,       0],   # HOSP_TBD
#     [0,     0,      0,        0,    109/250,         0, 141/250],   # HOSP_TBM
#     [0,     0,      0,        0,     3/8000, 991/24000,       0],   # DX_TBD
#     [0,     0,      0,        0,          0,         0,       0],   # DEAD
#     [0,     0,      0,        0,1/(62.77*52),        0,       0],   # CLEARED
#     [0,     0,      0,        0,  193/24000,  269/8000,       0]    # DX_TBM
#     ]

# average time spent in each state (given in the unit weeks)
T_INF = 12
T_HOSP_TBD = 1
T_HOSP_TBM = 2
T_DX_TBD = 24
T_DX_TBM = 24
T_CLEARED = 62.77*52

# probability of input parameters to determine the rate_transition_matrix
# assumptions that diagnostic yield is the most important piece of information
P_DX_SOC = 0.29                     # (alpha) diagnostic yield of investigations
P_DX_NSB = 0.52                     # (.4-.9) (alpha) diagnostic yield of investigations (NSB)

# assumptions that death in the hospital is the same for both states
P_DEATH_IN_HOSP = 0.436         # (0.368-0.506) (beta) probability of death in the hospital (relationship w/ alpha)
                                # from Jenkins; probability of dying within 1 year of diagnosis

P_INFECTED_CLEARED = 0.5
P_INFECTED_TBM = 0.15       # (0.1-0.2)
P_INFECTED_TBD = 0.35       # (0.3-0.4)

P_DX_TBD_DEATH = 0.009      # (0.5-1.6) probability of death in DX_TBD state (on treatment with TBD)
P_DX_TBM_DEATH = 0.193      # (0.14-0.261) probability of death in DX_TBM state (on treatment with TBM)

# NEED TO UPDATE NSB RATE TRANS MATRIX
# NSB_RATE_TRANS_MATRIX = [
#     [0, XXX, XXX, XXX, 0, XXX],  # INFECTED
#     [0, 0, 0, XXX, XXX, 0],  # HOSP_TBD
#     [0, 0, 0, XXX, XXX, 0],  # HOSP_TBM
#     [0, 0, 0, 0, XXX, XXX],  # DX_TB
#     [0, 0, 0, 0, 0, 0],  # DEAD
#     [0, 0, 0, 0, XXX, 0],  # CLEARED
#     [0, 0, 0, 0, XXX, 0]
# ]

# NEED TO INPUT WEEKLY COST OF EACH HEALTH STATE
# annual cost of each health state
WEEKLY_STATE_COST = [
    0,  # INFECTED
    392,  # HOSP_TBD
    392,  # HOSP_TBM
    1.75,  # DX_TBD
    0,   # DEAD
    0,   # CLEARED
    1.75    # DX_TBM
]
# NEED TO INPUT HEALTH UTILITY OF EACH HEALTH STATE????
# annual health utility of each health state
# WEEKLY_STATE_UTILITY = [
#     0,  # INFECTED      # cost of medicines, doctors appointments, etc
#     0,  # HOSP_TBD      # costs associated with hospitalization associated with TBD
#     0,  # HOSP_TBM      # costs associated with hospitalization for TBM
#     0,  # DEAD          # no costs
#     0,   # CLEARED       # no costs
#     0
# ]

# Diagnostic Costs associated with SOC vs. NSB
# one time costs associated with the diagnosis of TB at the infected, hosp_tbd, hosp_tbm states
SOC_ONE_TIME_COST = [
    0,  # INFECTED (charged only when the patient goes from INFECTED to DX)
    98,  # HOSP_TBD
    98,  # HOSP_TBM
    15,  # DX_TBD
    0,   # DEAD
    0,   # CLEARED
    15    # DX_TBM
]

NSB_ONE_TIME_COST = [
    0,  # INFECTED (charged only when the patient goes from INFECTED to DX)
    98,  # HOSP_TBD
    98,  # HOSP_TBM
    15 + 3,  # DX_TBD
    0,  # DEAD
    0,  # CLEARED
    15 + 3  # DX_TBM
]
