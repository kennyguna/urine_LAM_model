from enum import Enum
import numpy as np
import InputData as Data


class HealthStates(Enum):
    """ health states of patients with TB """
    INFECTED = 0
    HOSP_TBD = 1
    HOSP_TBM = 2
    DX_TBD = 3
    DEAD = 4
    CLEARED = 5
    DX_TBM = 6


class Diagnostic(Enum):
    """ SOC vs. NSB Diagnostic (Urine LAM) """
    SOC = 0
    NSB = 1


class ParametersFixed:
    def __init__(self, diagnostic):

        # selected therapy
        self.diagnostic = diagnostic

        # initial health state
        self.initialHealthState = HealthStates.INFECTED

        # single cost at each health state
        # assume that the intervention diagnostic is going to be the original diagnostic + the NSB diagnostic
        if self.diagnostic == Diagnostic.SOC:
            self.singleCosts = Data.SOC_ONE_TIME_COST
        else:
            self.singleCosts = Data.NSB_ONE_TIME_COST

        # # rate matrix
        # if self.diagnostic == Diagnostic.SOC:
        #     self.rateMatrix = Data.SOC_RATE_TRANS_MATRIX
        # else:
        #     self.rateMatrix = Data.NSB_RATE_TRANS_MATRIX

        # get rate matrix
        self.rateMatrix = get_rate_matrix(self.diagnostic)

        # weekly cost at each health state
        self.weeklyStateCosts = Data.WEEKLY_STATE_COST

        # weekly utility at each health state
        # self.weeklyUtility = Data.WEEKLY_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT


def get_rate_matrix(diagnostic):

    if diagnostic == Diagnostic.SOC:
        P_alpha = Data.P_DX_SOC
    else:
        P_alpha = Data.P_DX_NSB

    P_beta = Data.P_DEATH_IN_HOSP

    P_1 = Data.P_INFECTED_CLEARED
    P_2 = Data.P_INFECTED_TBD*(1-P_alpha)
    P_3 = Data.P_INFECTED_TBM*(1-P_alpha)
    P_4 = P_3*P_alpha + P_2*P_alpha
    P_5 = P_alpha*(1-P_beta)
    P_6 = (1-P_alpha)+(P_alpha*P_beta)
    P_7 = P_alpha*(1-P_beta)
    P_8 = (1-P_alpha)+(P_alpha*P_beta)
    P_9 = 1-Data.P_DX_TBD_DEATH
    P_10 = 1
    P_11 = 1-Data.P_DX_TBM_DEATH
    P_12 = Data.P_DX_TBM_DEATH
    P_13 = Data.P_DX_TBD_DEATH

    lambda_1 = P_1/Data.T_INF
    lambda_2 = P_2/Data.T_INF
    lambda_3 = P_3/Data.T_INF
    lambda_4 = P_4/Data.T_INF
    lambda_5 = P_5/Data.T_HOSP_TBD
    lambda_6 = P_6/Data.T_HOSP_TBD
    lambda_7 = P_7/Data.T_HOSP_TBM
    lambda_8 = P_8/Data.T_HOSP_TBM
    lambda_9 = P_9/Data.T_DX_TBD
    lambda_10 = P_10/Data.T_CLEARED
    lambda_11 = P_11/Data.T_DX_TBM
    lambda_12 = P_12/Data.T_DX_TBM
    lambda_13 = P_13/Data.T_DX_TBD

    rate_matrix = [
        [0, lambda_2, lambda_3, lambda_4, 0, lambda_1, 0],  # INFECTED
        [0, 0, 0, lambda_5, lambda_6, 0, 0],  # HOSP_TBD
        [0, 0, 0, 0, lambda_8, 0, lambda_7],  # HOSP_TBM
        [0, 0, 0, 0, lambda_13, lambda_9, 0],  # DX_TBD
        [0, 0, 0, 0, 0, 0, 0],  # DEAD
        [0, 0, 0, 0, lambda_10, 0, 0],  # CLEARED
        [0, 0, 0, 0, lambda_12, lambda_11, 0]  # DX_TBM
    ]

    return rate_matrix


# tests
# matrix_SOC = get_rate_matrix(Diagnostic.SOC)
# matrix_NSB = get_rate_matrix(Diagnostic.NSB)
#
# print(Data.SOC_RATE_TRANS_MATRIX)
# print(matrix_SOC)
# print(matrix_NSB)
