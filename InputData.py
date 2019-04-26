
# simulation settings
POP_SIZE = 1000     # cohort population size
SIM_LENGTH = 1000   # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate
# annual probability of background mortality (number per year per 1,000 population)
ANNUAL_PROB_BACKGROUND_MORT = 8.15 / 1000

# rate transition matrix
SOC_RATE_TRANS_MATRIX = [
    [0,  XXX,   XXX,    XXX, 0, XXX],   # INFECTED
    [0,0,0, XXX, XXX, 0],               # HOSP_TBD
    [0, 0, 0, XXX, XXX, 0],             # HOSP_TBM
    [0, 0,0,0, XXX, XXX],               # DX_TB
    [0,     0,   0,0,0,0],              # DEAD
    [0, 0, 0, 0, XXX, 0]                # CLEARED
    ]

NSB_RATE_TRANS_MATRIX = [
    [0, XXX, XXX, XXX, 0, XXX],  # INFECTED
    [0, 0, 0, XXX, XXX, 0],  # HOSP_TBD
    [0, 0, 0, XXX, XXX, 0],  # HOSP_TBM
    [0, 0, 0, 0, XXX, XXX],  # DX_TB
    [0, 0, 0, 0, 0, 0],  # DEAD
    [0, 0, 0, 0, XXX, 0]  # CLEARED
]

# annual cost of each health state
WEEKLY_STATE_COST = [
    0,  # INFECTED
    0,  # HOSP_TBD
    0,  # HOSP_TBM
    0,  # DEAD
    0   # CLEARED
]

# annual health utility of each health state
WEEKLY_STATE_UTILITY = [
    0,  # INFECTED      # cost of medicines, doctors appointments, etc
    0,  # HOSP_TBD      # costs associated with hospitalization associated with TBD
    0,  # HOSP_TBM      # costs associated with hospitalization for TBM
    0,  # DEAD          # no costs
    0   # CLEARED       # no costs
]

# Diagnostic Costs associated with SOC vs. NSB
# one time costs associated with the diagnosis of TB at the infected, hosp_tbd, hosp_tbm states
SOC_ONE_TIME_COST = [
    0,  # INFECTED      # cost of medicines, doctors appointments, etc
    0,  # HOSP_TBD      # costs associated with hospitalization associated with TBD
    0,  # HOSP_TBM      # costs associated with hospitalization for TBM
    0,  # DEAD          # no costs
    0   # CLEARED       # no costs
]

NSB_ONE_TIME_COST = [
    0,  # INFECTED      # cost of medicines, doctors appointments, etc
    0,  # HOSP_TBD      # costs associated with hospitalization associated with TBD
    0,  # HOSP_TBM      # costs associated with hospitalization for TBM
    0,  # DEAD          # no costs
    0   # CLEARED       # no costs
]

# CONSIDER THE ONE TIME COSTS ASSOCIATED WITH EACH STATE
# NEED TO FINALIZE THE RATES AND THE COSTS
