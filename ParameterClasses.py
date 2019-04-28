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
            self.singleDiagnosticCost = Data.SOC_ONE_TIME_COST
        else:
            self.singleDiagnosticCost = Data.SOC_ONE_TIME_COST + Data.NSB_ONE_TIME_COST

        # rate matrix
        if self.diagnostic == Diagnostic.SOC:
            self.rateMatrix = Data.SOC_RATE_TRANS_MATRIX
        else:
            self.rateMatrix = Data.NSB_RATE_TRANS_MATRIX

        # weekly cost at each health state
        self.weeklyCost = Data.WEEKLY_STATE_COST

        # weekly utility at each health state
        self.weeklyUtility = Data.WEEKLY_STATE_UTILITY

        # discount rate
        self.discountRate = Data.DISCOUNT
