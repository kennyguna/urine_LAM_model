import ParameterClasses as P
import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as Path
import SimPy.EconEvalClasses as Econ
import SimPy.StatisticalClasses as Stat
import SimPy.MarkovClasses as Markov


class Patient:
    def __init__(self, id, parameters):
        """ initiates a patient
        :param id: ID of the patient
        :param parameters: an instance of the parameters class
        """
        self.id = id
        self.rng = RVGs.RNG(seed=id)  # random number generator for this patient
        self.params = parameters
        # gillespie algorithm
        self.gillespie = Markov.Gillespie(transition_rate_matrix=parameters.rateMatrix)
        self.stateMonitor = PatientStateMonitor(parameters=parameters)  # patient state monitor

    def simulate(self, sim_length):
        """ simulate the patient over the specified simulation length """

        t = 0  # simulation time
        if_stop = False

        while not if_stop:

            # find time to next event, and next state
            dt, new_state_index = self.gillespie.get_next_state(
                current_state_index=self.stateMonitor.currentState.value,
                rng=self.rng)

            # stop if time to next event (dt) is None
            if dt is None:
                if_stop = True

            # else if  the next event occurs beyond simulation length
            elif dt + t > sim_length:
                if_stop = True
                # collect cost and health outcomes
                self.stateMonitor.costUtilityMonitor.update(time=sim_length,
                                                            current_state=self.stateMonitor.currentState,
                                                            next_state=self.stateMonitor.currentState)

                # CONSIDER WRITING A NEW METHOD TO INCLUDE THE TIME SPENT IN WHATEVER STATE THE
                # INDIVIDUAL IS AFTER THE END OF THE SIMULATION

            else:
                # advance time to the time of next event
                t += dt
                # update health state
                # t passed in corresponds to the time at the end of the health state
                # dt corresponds to the time spent in the next health state
                # current_state corresponds to the current state
                # new_state corresponds to the new state
                self.stateMonitor.update(time=t, dt=dt, current_state=self.stateMonitor.currentState,
                                         new_state=P.HealthStates(new_state_index))


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState   # initial health state

        # Important Outcomes
        self.survivalTime = None                # survival time

        # If patient enters any of these states
        self.ifHOSP_TBM = False
        self.ifHOSP_TBD = False
        self.ifDX_TBM = False
        self.ifDX_TBD = False
        self.ifCLEARED = False
        self.ifDEAD = False

        # time until each event
        # infected
        self.timeINFECTEDtoHOSP_TBD = None
        self.timeINFECTEDtoHOSP_TBM = None
        self.timeINFECTEDtoDX_TBD = None
        self.timeINFECTEDtoCLEARED = None
        # cleared
        self.timeCLEAREDtoDEAD = None
        # hosp TBD
        self.timeHOSP_TBDtoDEAD = None
        self.timeHOSP_TBDtoDX_TBD = None
        # hosp TBM
        self.timeHOSP_TBMtoDEAD = None
        self.timeHOSP_TBMtoDX_TBM = None
        # dx tbd
        self.timeDX_TBDtoDEAD = None
        self.timeDX_TBDtoCLEARED = None
        # dx tbm
        self.timeDX_TBMtoDEAD = None
        self.timeDX_TBMtoCLEARED = None

        # NEED TO DO THIS SECTION
        # patient's cost and utility monitor
        self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time, dt, current_state, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state

        # time passed in corresponds to the time at the end of the health state (time at the end of new_state)
        # dt corresponds to the time spent in the next health state (time spent in new_state)
        # current_state corresponds to the current state (current state ended at time time-dt)
        # new_state corresponds to the new state (ending at time time)
        """

        # update survival time
        if new_state == P.HealthStates.DEAD:
            self.survivalTime = time
            self.ifDEAD = True
            if current_state == P.HealthStates.HOSP_TBM:
                self.timeHOSP_TBMtoDEAD = dt
            if current_state == P.HealthStates.DX_TBD:
                self.timeDX_TBDtoDEAD = dt
            if current_state == P.HealthStates.DX_TBM:
                self.timeDX_TBMtoDEAD = dt
            if current_state == P.HealthStates.CLEARED:
                self.timeCLEAREDtoDEAD = dt
            if current_state == P.HealthStates.HOSP_TBD:
                self.timeHOSP_TBDtoDEAD = dt

        # update if patient develops TBD
        if new_state == P.HealthStates.HOSP_TBD:
            self.ifHOSP_TBD = True
            self.timeINFECTEDtoHOSP_TBD = time

        # update if patient develops TBM
        if new_state == P.HealthStates.HOSP_TBM:
            self.ifHOSP_TBM = True
            self.timeINFECTEDtoHOSP_TBM = time

        if new_state == P.HealthStates.CLEARED:
            self.ifCLEARED = True
            if current_state == P.HealthStates.INFECTED:
                self.timeINFECTEDtoCLEARED = dt
            if current_state == P.HealthStates.DX_TBM:
                self.timeDX_TBMtoCLEARED = dt
            if current_state == P.HealthStates.DX_TBD:
                self.timeDX_TBDtoCLEARED = dt

        if new_state == P.HealthStates.DX_TBD:
            self.ifDX_TBD = True
            if current_state == P.HealthStates.INFECTED:
                self.timeINFECTEDtoDX_TBD = dt
            if current_state == P.HealthStates.HOSP_TBD:
                self.timeHOSP_TBDtoDX_TBD = dt

        if new_state == P.HealthStates.DX_TBM:
            self.ifDX_TBM = True
            if current_state == P.HealthStates.HOSP_TBM:
                self.timeHOSP_TBMtoDX_TBM = dt

        # NEED TO WORK ON THIS SECTION
        # update cost and utility
        self.costUtilityMonitor.update(time=time,
                                       current_state=self.currentState,
                                       next_state=new_state)

        # update current health state
        self.currentState = new_state

class PatientCostUtilityMonitor:

    def __init__(self, parameters):

        self.tLastRecorded = 0  # time when the last cost and outcomes got recorded

        # model parameters for this patient
        self.params = parameters

        # total cost and utility
        self.totalDiscountedCost = 0
        self.totalDiscountedUtility = 0

    def update(self, time, current_state, next_state):
        """ updates the discounted total cost and health utility
        :param time: simulation time
        :param current_state: current health state
        :param next_state: next health state
        """

        # cost and utility (per unit of time) during the period since the last recording until now
        cost = self.params.weeklyStateCosts[current_state.value]

        if (current_state is P.HealthStates.INFECTED and next_state is P.HealthStates.DX_TBD) or \
                (current_state != P.HealthStates.INFECTED):
            single_cost = self.params.singleCosts[current_state.value]

        # utility = self.params.weeklyStateUtilities[current_state.value]

        # discounted cost and utility (continuously compounded)
        discounted_cost = Econ.pv_continuous_payment(payment=cost,
                                                     discount_rate=self.params.discountRate,
                                                     discount_period=(self.tLastRecorded, time))
        # discounted_utility = Econ.pv_continuous_payment(payment=utility,
        #                                                 discount_rate=self.params.discountRate,
        #                                                 discount_period=(self.tLastRecorded, time))

        # discounted cost (single payment)
        if (current_state is P.HealthStates.INFECTED and next_state is P.HealthStates.DX_TBD) or \
                (current_state != P.HealthStates.INFECTED):
            discounted_cost += Econ.pv_single_payment(payment=single_cost,
                                                      discount_rate=self.params.discountRate,
                                                      discount_period=time,
                                                      discount_continuously=True)

        # update total discounted cost and utility
        self.totalDiscountedCost += discounted_cost
        # self.totalDiscountedUtility += discounted_utility

        # update the time since last recording to the current time
        self.tLastRecorded = time


class Cohort:
    def __init__(self, id, pop_size, parameters):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param parameters: parameters
        """
        self.id = id
        self.popSize = pop_size
        self.params = parameters
        self.patients = []  # list of patients
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, sim_length):
        """ simulate the cohort of patients over the specified number of time-steps
        :param sim_length: simulation length
        """

        # populate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i, parameters=self.params)
            # add the patient to the cohort
            self.patients.append(patient)

        # simulate all patients
        for patient in self.patients:
            # simulate
            patient.simulate(sim_length)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(self.patients)

        # clear patients
        self.patients.clear()


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []         # patients' survival times

        self.nLivingPatients = None     # survival curve (sample path of number of alive patients over time)
        self.statSurvivalTime = None    # summary statistics for survival time

        self.nHOSP_TBM = 0
        self.nHOSP_TBD = 0
        self.nDX_TBD = 0
        self.nDX_TBM = 0
        self.nCLEARED = 0
        self.nDEAD = 0

        self.timesINFECTEDtoHOSP_TBD = []
        self.timesINFECTEDtoHOSP_TBM = []
        self.timesINFECTEDtoDX_TBD = []
        self.timesINFECTEDtoCLEARED = []
        self.timesCLEAREDtoDEAD = []
        self.timesHOSP_TBDtoDEAD = []
        self.timesHOSP_TBDtoDX_TBD = []
        self.timesHOSP_TBMtoDEAD = []
        self.timesHOSP_TBMtoDX_TBM = []
        self.timesDX_TBDtoDEAD = []
        self.timesDX_TBDtoCLEARED = []
        self.timesDX_TBMtoDEAD = []
        self.timesDX_TBMtoCLEARED = []

        self.timesINFECTED = []
        self.timesHOSP_TBM = []
        self.timesHOSP_TBD = []
        self.timesDX_TBD = []
        self.timesDX_TBM = []
        self.timesCLEARED = []
        self.timesDEAD = []

        self.costs = []                 # patients' discounted costs
        self.costsPresenting = []
        # self.utilities =[]              # patients' discounted utilities

        self.nHospitalized = 0

        self.statTimeINFECTEDtoHOSP_TBD = None
        self.statTimeINFECTEDtoHOSP_TBM = None
        self.statTimeINFECTEDtoDX_TBD = None
        self.statTimeINFECTEDtoCLEARED = None
        self.statTimeCLEAREDtoDEAD = None
        self.statTimeHOSP_TBDtoDEAD = None
        self.statTimeHOSP_TBDtoDX_TBD = None
        self.statTimeHOSP_TBMtoDEAD = None
        self.statTimeHOSP_TBMtoDX_TBM = None
        self.statTimeDX_TBDtoDEAD = None
        self.statTimeDX_TBDtoCLEARED = None
        self.statTimeDX_TBMtoDEAD = None
        self.statTimeDX_TBMtoCLEARED = None

        self.statTimesINFECTED = None
        self.statTimesHOSP_TBM = None
        self.statTimesHOSP_TBD = None
        self.statTimesDX_TBD = None
        self.statTimesDX_TBM = None
        self.statTimesCLEARED = None
        self.statCost = None            # summary statistics for discounted cost
        self.statCostPresenting = None
        # self.statUtility = None         # summary statistics for discounted utility

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: a list of simulated patients"""

        # record survival time
        for patient in simulated_patients:
            # survival time
            if not (patient.stateMonitor.survivalTime is None):
                self.survivalTimes.append(patient.stateMonitor.survivalTime)

            # record time patient spends in each transition:
            if patient.stateMonitor.ifHOSP_TBM:
                self.timesINFECTEDtoHOSP_TBM.append(patient.stateMonitor.timeINFECTEDtoHOSP_TBM)
                self.nHOSP_TBM += 1
            if patient.stateMonitor.ifHOSP_TBD:
                self.timesINFECTEDtoHOSP_TBD.append(patient.stateMonitor.timeINFECTEDtoHOSP_TBD)
                self.nHOSP_TBD += 1
            if patient.stateMonitor.ifDX_TBM:
                self.timesHOSP_TBMtoDX_TBM.append(patient.stateMonitor.timeHOSP_TBMtoDX_TBM)
                self.nDX_TBM += 1
            if patient.stateMonitor.ifDX_TBD and patient.stateMonitor.ifHOSP_TBD:
                self.timesHOSP_TBDtoDX_TBD.append(patient.stateMonitor.timeHOSP_TBDtoDX_TBD)
                self.nDX_TBD += 1
            if patient.stateMonitor.ifDX_TBD and (patient.stateMonitor.ifHOSP_TBD is False):  # and \
                    # (patient.stateMonitor.ifHOSP_TBD is False) and (patient.stateMonitor.ifDEAD is False):
                self.timesINFECTEDtoDX_TBD.append(patient.stateMonitor.timeINFECTEDtoDX_TBD)
                self.nDX_TBD += 1
            if patient.stateMonitor.ifCLEARED and patient.stateMonitor.ifDX_TBD:
                self.timesDX_TBDtoCLEARED.append(patient.stateMonitor.timeDX_TBDtoCLEARED)
                self.nCLEARED += 1
            if patient.stateMonitor.ifCLEARED and patient.stateMonitor.ifDX_TBM:
                self.timesDX_TBMtoCLEARED.append(patient.stateMonitor.timeDX_TBMtoCLEARED)
                self.nCLEARED += 1
            if patient.stateMonitor.ifCLEARED and (patient.stateMonitor.ifDX_TBD is False) and \
                    (patient.stateMonitor.ifDX_TBM is False):
                self.timesINFECTEDtoCLEARED.append(patient.stateMonitor.timeINFECTEDtoCLEARED)
                self.nCLEARED += 1
            # times from HOSP_TBM to DEAD
            if patient.stateMonitor.ifDEAD and patient.stateMonitor.ifHOSP_TBM and \
                    (patient.stateMonitor.ifCLEARED is False) and (patient.stateMonitor.ifHOSP_TBD is False) and \
                    (patient.stateMonitor.ifDX_TBD is False) and (patient.stateMonitor.ifDX_TBM is False):
                self.timesHOSP_TBMtoDEAD.append(patient.stateMonitor.timeHOSP_TBMtoDEAD)
                self.nDEAD += 1
            # times from HOSP_TBD to DEAD
            if patient.stateMonitor.ifDEAD and patient.stateMonitor.ifHOSP_TBD and \
                    (patient.stateMonitor.ifCLEARED is False) and (patient.stateMonitor.ifHOSP_TBM is False) and \
                    (patient.stateMonitor.ifDX_TBM is False) and (patient.stateMonitor.ifDX_TBD is False):
                self.timesHOSP_TBDtoDEAD.append(patient.stateMonitor.timeHOSP_TBDtoDEAD)
                self.nDEAD += 1
            # get rid of cleared and the two hosps
            if patient.stateMonitor.ifDEAD and patient.stateMonitor.ifDX_TBM and \
                    (patient.stateMonitor.ifCLEARED is False) and (patient.stateMonitor.timeHOSP_TBMtoDEAD is None) and\
                    (patient.stateMonitor.ifHOSP_TBD is False) and (patient.stateMonitor.ifDX_TBD is False):
                self.timesDX_TBMtoDEAD.append(patient.stateMonitor.timeDX_TBMtoDEAD)
                self.nDEAD += 1
            if patient.stateMonitor.ifDEAD and patient.stateMonitor.ifDX_TBD and \
                    (patient.stateMonitor.ifCLEARED is False) and (patient.stateMonitor.timeHOSP_TBDtoDEAD is None) and\
                    (patient.stateMonitor.ifHOSP_TBM is False) and (patient.stateMonitor.ifDX_TBM is False):
                self.timesDX_TBDtoDEAD.append(patient.stateMonitor.timeDX_TBDtoDEAD)
                self.nDEAD += 1
            if patient.stateMonitor.ifDEAD and patient.stateMonitor.ifCLEARED and \
                    (patient.stateMonitor.timeHOSP_TBMtoDEAD is None) and (patient.stateMonitor.timeHOSP_TBDtoDEAD is None) and \
                    (patient.stateMonitor.timeDX_TBMtoDEAD is None) and (patient.stateMonitor.timeDX_TBDtoDEAD is None):
                self.timesCLEAREDtoDEAD.append(patient.stateMonitor.timeCLEAREDtoDEAD)
                self.nDEAD += 1

            # if patient.stateMonitor.ifDEAD and patient.stateMonitor.ifCLEARED and \
            #         (patient.stateMonitor.ifDX_TBD is False) and (patient.stateMonitor.ifHOSP_TBD is False) and \
            #         (patient.stateMonitor.ifHOSP_TBM is False) and (patient.stateMonitor.ifDX_TBM is False):
            #     self.timesCLEAREDtoDEAD.append(patient.stateMonitor.timeCLEAREDtoDEAD)
            #     self.nDEAD += 1

            # discounted cost and discounted utility
            self.costs.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)
            # self.utilities.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedUtility)

            # discounted cost of all the patients who present to healthcare
            if patient.stateMonitor.timeINFECTEDtoCLEARED is None:
                self.costsPresenting.append(patient.stateMonitor.costUtilityMonitor.totalDiscountedCost)

        # Gather Data
        self.nHospitalized = self.nHOSP_TBD + self.nHOSP_TBM

        self.timesINFECTED = self.timesINFECTEDtoCLEARED + self.timesINFECTEDtoDX_TBD + self.timesINFECTEDtoHOSP_TBM + \
            self.timesINFECTEDtoHOSP_TBD
        self.timesHOSP_TBD = self.timesHOSP_TBDtoDEAD + self.timesHOSP_TBDtoDX_TBD
        self.timesHOSP_TBM = self.timesHOSP_TBMtoDEAD + self.timesHOSP_TBMtoDX_TBM
        self.timesDX_TBM = self.timesDX_TBMtoCLEARED + self.timesDX_TBMtoDEAD
        self.timesDX_TBD = self.timesDX_TBDtoCLEARED + self.timesDX_TBDtoDEAD
        self.timesCLEARED = self.timesCLEAREDtoDEAD

        # Summary Statistics
        self.statSurvivalTime = Stat.SummaryStat('Survival time', self.survivalTimes)

        self.statTimeINFECTEDtoHOSP_TBD = Stat.SummaryStat('Infected to HOSP_TBD', self.timesINFECTEDtoHOSP_TBD)
        self.statTimeINFECTEDtoHOSP_TBM = Stat.SummaryStat('Infected to HOSP_TBM', self.timesINFECTEDtoHOSP_TBM)
        self.statTimeINFECTEDtoDX_TBD = Stat.SummaryStat('Infected to DX_TBD', self.timesINFECTEDtoDX_TBD)
        self.statTimeINFECTEDtoCLEARED = Stat.SummaryStat('Infected to Cleared', self.timesINFECTEDtoCLEARED)
        self.statTimeCLEAREDtoDEAD = Stat.SummaryStat('Cleared to Dead', self.timesCLEAREDtoDEAD)
        self.statTimeHOSP_TBDtoDEAD = Stat.SummaryStat('HOSP_TBD to Dead', self.timesHOSP_TBDtoDEAD)
        self.statTimeHOSP_TBDtoDX_TBD = Stat.SummaryStat('HOSP_TBD to DX_TBD', self.timesHOSP_TBDtoDX_TBD)
        self.statTimeHOSP_TBMtoDEAD = Stat.SummaryStat('HOSP_TBM to DEAD', self.timesHOSP_TBMtoDEAD)
        self.statTimeHOSP_TBMtoDX_TBM = Stat.SummaryStat('HOSP_TBM to DX_TBM', self.timesHOSP_TBMtoDX_TBM)
        self.statTimeDX_TBDtoDEAD = Stat.SummaryStat('DX_TBD to Dead', self.timesDX_TBDtoDEAD)
        self.statTimeDX_TBDtoCLEARED = Stat.SummaryStat('DX_TBD to Cleared', self.timesDX_TBDtoCLEARED)
        self.statTimeDX_TBMtoDEAD = Stat.SummaryStat('DX_TBM to Dead', self.timesDX_TBMtoDEAD)
        self.statTimeDX_TBMtoCLEARED = Stat.SummaryStat('DX_TBM to Cleared', self.timesDX_TBMtoCLEARED)

        self.statTimesINFECTED = Stat.SummaryStat('Infected', self.timesINFECTED)
        self.statTimesHOSP_TBM = Stat.SummaryStat('HOSP_TBM', self.timesHOSP_TBM)
        self.statTimesHOSP_TBD = Stat.SummaryStat('HOSP_TBD', self.timesHOSP_TBD)
        self.statTimesDX_TBD = Stat.SummaryStat('DX_TBD', self.timesDX_TBD)
        self.statTimesDX_TBM = Stat.SummaryStat('DX_TBM', self.timesDX_TBM)
        self.statTimesCLEARED = Stat.SummaryStat('Cleared', self.timesCLEARED)

        self.statCost = Stat.SummaryStat('Discounted cost', self.costs)
        self.statCostPresenting = Stat.SummaryStat('Discounted cost (Presenting)', self.costsPresenting)
        # self.statUtility = Stat.SummaryStat('Discounted utility', self.utilities)

        # survival curve
        self.nLivingPatients = Path.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )

        print("Number of transitions from DX_TBD to DEAD", len(self.timesDX_TBDtoDEAD))
        print("Number of transitions from DX_TBM to DEAD", len(self.timesDX_TBMtoDEAD))
