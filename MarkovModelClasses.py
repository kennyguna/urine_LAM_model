import ParameterClasses as P
import SimPy.RandomVariantGenerators as RVGs
import Simpy.SamplePathClasses as Path
import Simpy.EconEvalClasses as Econ
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
            else:
                # advance time to the time of next event
                t += dt
                # update health state
                self.stateMonitor.update(time=t, new_state=P.HealthStates(new_state_index))


class PatientStateMonitor:
    """ to update patient outcomes (years survived, cost, etc.) throughout the simulation """
    def __init__(self, parameters):

        self.currentState = parameters.initialHealthState   # initial health state

        # Important Outcomes
        self.survivalTime = None                # survival time

        # Important Outcomes
        self.ifHospitalized = False             # if the patient was hospitalized
        self.ifDevelopedTBM = False             # if the patient developed TBM
        self.ifDead = False                     # if patient dies

        # Important Outcomes
        self.timeToHospitalization = None       # time to hospitalization
        self.timeInHospital = None              # duration of patient stay in hospital
        self.timeToCure = None                  # time to cure
        self.timeToDiagnosePreHosp = None       # time to detect TB outpatient (no hospitalization)
        self.timeToDevelopTBD                   # time to develop TBD
        self.timeToDevelopTBM                   # time to develop TBM

        # Time spent in each state
        self.timeInOutpatient = None
        self.timeInHospitalTBM = None
        self.timeInHospitalTBD = None
        self.timeOnTherapy = None
        self.timeCleared = None

        # patient's cost and utility monitor
        # self.costUtilityMonitor = PatientCostUtilityMonitor(parameters=parameters)

    def update(self, time, new_state):
        """
        update the current health state to the new health state
        :param time: current time
        :param new_state: new state
        """

        # update survival time
        if new_state == P.HealthStates.DEAD:
            self.survivalTime = time

        # update time until AIDS
        if self.currentState != P.HealthStates.AIDS and new_state == P.HealthStates.AIDS:
            self.ifDevelopedAIDS = True
            self.timeToAIDS = time

        # update cost and utility
        self.costUtilityMonitor.update(time=time,
                                       current_state=self.currentState,
                                       next_state=new_state)

        ################################### THE STUFF AFTER THIS IS ME

        # update current health state
        self.currentState = new_state

        # Important Outcomes
        self.survivalTime = None                # survival time

        # Important Outcomes
        self.ifHospitalized = False             # if the patient was hospitalized
        self.ifDevelopedTBM = False             # if the patient developed TBM
        self.ifDead = False                     # if patient dies

        # Important Outcomes
        self.timeToHospitalization = None       # time to hospitalization
        self.timeInHospital = None              # duration of patient stay in hospital
        self.timeToCure = None                  # time to cure
        self.timeToDiagnosePreHosp = None       # time to detect TB outpatient (no hospitalization)
        self.timeToDevelopTBD                   # time to develop TBD
        self.timeToDevelopTBM                   # time to develop TBM

        # Time spent in each state
        self.timeInOutpatient = None
        self.timeInHospitalTBM = None
        self.timeInHospitalTBD = None
        self.timeOnTherapy = None
        self.timeCleared = None

