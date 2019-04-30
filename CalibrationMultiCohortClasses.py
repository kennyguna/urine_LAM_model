from MarkovModelClasses import Cohort
import CalibrationParameterClasses as P
from ProbabilisticParamClasses import ParameterGenerator
import SimPy.StatisticalClasses as Stat
import SimPy.RandomVariantGenerators as RVGs


class MultiCohort:
    """ simulates multiple cohorts with different parameters """

    def __init__(self, ids, pop_sizes, mortality_probs, diagnostic):
        """
        :param ids: (list) of ids for cohorts to simulate
        :param pop_sizes: (list) of population sizes of cohorts to simulate
        :param mortality_probs: (list) of the mortality probabilities
        """
        self.ids = ids
        self.popSizes = pop_sizes
        self.multiCohortOutcomes = MultiCohortOutcomes()
        self.parameters = []
        self.cohorts = []
        for i in range(len(self.ids)):
            self.parameters.append(P.ParametersFixed(diagnostic=diagnostic[i], calibrate_mortality=mortality_probs[i]))

        # create cohorts
        for i in range(len(self.ids)):
            self.cohorts.append(Cohort(id=self.ids[i],
                                       pop_size=self.popSizes[i],
                                       parameters=self.parameters[i])
                                )

    def simulate(self, sim_length):
        """ simulates all cohorts
        :param sim_length: simulation length
        """

        for cohort in self.cohorts:

            # simulate the cohort
            cohort.simulate(sim_length=sim_length)

            # extract the outcomes of this simulated cohort
            self.multiCohortOutcomes.extract_outcomes(simulated_cohort=cohort)

        # calculate the summary statistics of outcomes from all cohorts
        self.multiCohortOutcomes.calculate_summary_stats()
        #
        # # clear cohorts (to free up the memory that was allocated to these cohorts)
        # self.cohorts.clear()


class MultiCohortOutcomes:
    def __init__(self):

        self.survivalCurves = []  # list of survival curves from all simulated cohorts

        self.meanSurvivalTimes = []  # list of average patient survival time from each simulated cohort
        self.mortality56Day = []
        self.mortality2Month = []
        self.mortality1Year = []
        self.mortality2Years = []
        self.mortality5Years = []
        self.nTBM = []
        self.nHospitalized = []
        self.totalYLL = []
        self.meanCosts = []          # list of average patient cost from each simulated cohort
        # self.meanCostPresenting = []

        self.statMeanSurvivalTime = None    # this is not a very useful statistic for this cohort
        self.statMortality56Day = None
        self.statMortality2Month = None
        self.statMortality1Year = None
        self.statMortality2Year = None
        self.statMortality5Year = None
        self.statNTBM = None
        self.statNHospitalized = None
        self.statTotalYLL = None
        self.statMeanCost = None            # summary statistics of average cost
        # self.statMeanCostPresenting = None

    def extract_outcomes(self, simulated_cohort):
        """ extracts outcomes of a simulated cohort
        :param simulated_cohort: a cohort after being simulated"""

        # append the survival curve of this cohort
        self.survivalCurves.append(simulated_cohort.cohortOutcomes.nLivingPatients)
        # store mean survival time from this cohort
        self.meanSurvivalTimes.append(simulated_cohort.cohortOutcomes.statSurvivalTime.get_mean())
        self.mortality56Day.append(simulated_cohort.cohortOutcomes.mortality56Day)
        self.mortality2Month.append(simulated_cohort.cohortOutcomes.mortality2Months)
        self.mortality1Year.append(simulated_cohort.cohortOutcomes.mortality1Year)
        self.mortality2Years.append(simulated_cohort.cohortOutcomes.mortality2Years)
        self.mortality5Years.append(simulated_cohort.cohortOutcomes.mortality5Years)
        self.nTBM.append(simulated_cohort.cohortOutcomes.nHOSP_TBM)
        self.nHospitalized.append(simulated_cohort.cohortOutcomes.nHospitalized)
        self.totalYLL.append(simulated_cohort.cohortOutcomes.totalYLL)
        # store mean cost from this cohort
        self.meanCosts.append(simulated_cohort.cohortOutcomes.statCost.get_mean())
        # store mean cost from this cohort
        # self.meanCostPresenting.append(simulated_cohort.cohortOutcomes.statCostPresenting.get_mean())

    def calculate_summary_stats(self):
        """
        calculate the summary statistics
        """
        # summary statistics of mean survival time
        self.statMeanSurvivalTime = Stat.SummaryStat(name='Average survival time',
                                                     data=self.meanSurvivalTimes)
        self.statMortality56Day = Stat.SummaryStat(name='Average 56-day mortality',
                                                   data=self.mortality56Day)
        self.statMortality2Month = Stat.SummaryStat(name='Average 2-month mortality',
                                                   data=self.mortality2Month)
        self.statMortality1Year = Stat.SummaryStat(name='Average 1-year mortality',
                                                   data=self.mortality1Year)
        self.statMortality2Year = Stat.SummaryStat(name='Average 2-year mortality',
                                                   data=self.mortality2Years)
        self.statMortality5Year = Stat.SummaryStat(name='Average 5-year mortality',
                                                   data=self.mortality5Years)
        self.statNTBM = Stat.SummaryStat(name='Average number TBM',
                                                  data=self.nTBM)
        self.statNHospitalized = Stat.SummaryStat(name='Average number hospitalized',
                                                   data=self.nHospitalized)
        self.statTotalYLL = Stat.SummaryStat(name='Average total years of life lost',
                                                   data=self.totalYLL)
        # summary statistics of mean cost
        self.statMeanCost = Stat.SummaryStat(name='Average cost',
                                             data=self.meanCosts)
        # # summary statistics of mean cost
        # self.statMeanCostPresenting = Stat.SummaryStat(name='Average cost presenting',
        #                                                data=self.meanCostPresenting)

