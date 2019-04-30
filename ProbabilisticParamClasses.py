from ParameterClasses import *  # import everything from the ParameterClass module
import InputData as Data
import SimPy.RandomVariantGenerators as RVGs
import SimPy.FittingProbDist_MM as MM
import math
import scipy.stats as stat


class Parameters:

    def __init__(self, diagnostic):

        self.diagnostic = diagnostic           # selected therapy
        self.initialHealthState = HealthStates.INFECTED     # initial health state
        self.rateMatrix = []                # transition probability matrix of the selected therapy
        self.weeklyStateCosts = []          # weekly state costs
        self.discountRate = Data.DISCOUNT   # discount rate
        self.singleCosts = []

        # NEED TO DO SOMETHING TO CONSIDER THE SINGLE COSTS
        # if self.diagnostic == Diagnostic.SOC:
        #     self.singleCosts = Data.SOC_ONE_TIME_COST
        # else:
        #     self.singleCosts = Data.NSB_ONE_TIME_COST

        # need to consider that alpha probability is different


class ParameterGenerator:

    def __init__(self, diagnostic):

        self.diagnostic = diagnostic
        self.probInfectedRVG = None     # list of dirichlet distributions for moving out of the infected state
        self.probAlphaRVG = None        # list of beta distributions for the alpha probability if the diagnostic test is NSB
        self.weeklyStateCostRVG = []  # list of gamma distributions for the annual cost of states
        self.singleStateCostRVG = []         # list of gamma distributions for the single cost of states

        # create Dirichlet distributions for transition probabilities
        self.probInfectedRVG = RVGs.Dirichlet(a=[Data.P_INFECTED_CLEARED, Data.P_INFECTED_TBD, Data.P_INFECTED_TBM])

        # crate beta distribution for the alpha probability
        fit_output = MM.get_beta_params(mean=Data.P_DX_NSB, st_dev=Data.P_DX_NSB/5)
        self.probAlphaRVG = RVGs.Beta(a=fit_output["a"], b=fit_output["b"])

        # create gamma distributions for annual state cost
        for cost in Data.WEEKLY_STATE_COST:
            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.weeklyStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5
                fit_output = MM.get_gamma_params(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.weeklyStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                               loc=0,
                               scale=fit_output["scale"]))

        # create gamma distributions for single state cost
        if self.diagnostic == Diagnostic.SOC:
            single_cost = Data.SOC_ONE_TIME_COST
        else:
            single_cost = Data.NSB_ONE_TIME_COST

        for cost in single_cost:
            # if cost is zero, add a constant 0, otherwise add a gamma distribution
            if cost == 0:
                self.singleStateCostRVG.append(RVGs.Constant(value=0))
            else:
                # find shape and scale of the assumed gamma distribution
                # no data available to estimate the standard deviation, so we assumed st_dev=cost / 5
                fit_output = MM.get_gamma_params(mean=cost, st_dev=cost / 5)
                # append the distribution
                self.singleStateCostRVG.append(
                    RVGs.Gamma(a=fit_output["a"],
                               loc=0,
                               scale=fit_output["scale"]))

    def get_new_parameters(self, rng):
        """
        this method is called in the implementation of the class
        :param rng: random number generator
        :return: a new parameter set
        """

        # create a parameter set
        param = Parameters(diagnostic=self.diagnostic)

        # P1,P2,P3 are all changed by the dirchilet distribution
        # P_alpha is changed by the beta distribution (only if therapy)

        # calculate new rate matrix
        if self.diagnostic == Diagnostic.SOC:
            P_alpha = Data.P_DX_SOC
        else:
            P_alpha = self.probAlphaRVG.sample(rng)  # how to draw from a beta distribution

        P_beta = Data.P_DEATH_IN_HOSP

        dirichelet = self.probInfectedRVG.sample(rng)

        P_1 = dirichelet[0]
        P_2 = dirichelet[1] * (1 - P_alpha)
        P_3 = dirichelet[2] * (1 - P_alpha)


        # P_1 = Data.P_INFECTED_CLEARED
        # P_2 = Data.P_INFECTED_TBD * (1 - P_alpha)
        # P_3 = Data.P_INFECTED_TBM * (1 - P_alpha)

        P_4 = P_3 * P_alpha + P_2 * P_alpha
        P_5 = P_alpha * (1 - P_beta)
        P_6 = (1 - P_alpha) + (P_alpha * P_beta)
        P_7 = P_alpha * (1 - P_beta)
        P_8 = (1 - P_alpha) + (P_alpha * P_beta)
        P_9 = 1 - Data.P_DX_TBD_DEATH
        P_10 = 1
        P_11 = 1 - Data.P_DX_TBM_DEATH
        P_12 = Data.P_DX_TBM_DEATH
        P_13 = Data.P_DX_TBD_DEATH

        lambda_1 = P_1 / Data.T_INF
        lambda_2 = P_2 / Data.T_INF
        lambda_3 = P_3 / Data.T_INF
        lambda_4 = P_4 / Data.T_INF
        lambda_5 = P_5 / Data.T_HOSP_TBD
        lambda_6 = P_6 / Data.T_HOSP_TBD
        lambda_7 = P_7 / Data.T_HOSP_TBM
        lambda_8 = P_8 / Data.T_HOSP_TBM
        lambda_9 = P_9 / Data.T_DX_TBD
        lambda_10 = P_10 / Data.T_CLEARED
        lambda_11 = P_11 / Data.T_DX_TBM
        lambda_12 = P_12 / Data.T_DX_TBM
        lambda_13 = P_13 / Data.T_DX_TBD

        param.rateMatrix = [
            [0, lambda_2, lambda_3, lambda_4, 0, lambda_1, 0],  # INFECTED
            [0, 0, 0, lambda_5, lambda_6, 0, 0],  # HOSP_TBD
            [0, 0, 0, 0, lambda_8, 0, lambda_7],  # HOSP_TBM
            [0, 0, 0, 0, lambda_13, lambda_9, 0],  # DX_TBD
            [0, 0, 0, 0, 0, 0, 0],  # DEAD
            [0, 0, 0, 0, lambda_10, 0, 0],  # CLEARED
            [0, 0, 0, 0, lambda_12, lambda_11, 0]  # DX_TBM
        ]

        # sample from gamma distributions that are assumed for annual state costs
        for dist in self.weeklyStateCostRVG:
            param.weeklyStateCosts.append(dist.sample(rng))

        # sample from gamma distributions that are assumed for single state consts
        for dist in self.singleStateCostRVG:
            param.singleCosts.append(dist.sample(rng))

        # return the parameter set
        return param
