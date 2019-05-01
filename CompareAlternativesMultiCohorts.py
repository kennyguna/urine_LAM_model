import MultiCohortClasses as Cls
import ParameterClasses as P
import InputData as D
import MultiCohortSupport as Support


# ### initialization based on generating new parameters
multiCohort_SOC = Cls.MultiCohort(
    ids=range(D.N_COHORTS),
    pop_size=D.POP_SIZE,
    diagnostic=P.Diagnostic.SOC
)

## initialization based on generating fixed parameters
##create a multi-cohort to simulate under mono therapy
# multiCohort_SOC = Cls.MultiCohort(
#     ids=range(D.N_COHORTS),
#     pop_size=D.POP_SIZE,
#     parameters=P.ParametersFixed(diagnostic=P.Diagnostic.SOC)
# )

multiCohort_SOC.simulate(sim_length=D.SIM_LENGTH)

# ### initialization based on generating new parameters
multiCohort_NSB = Cls.MultiCohort(
    ids=range(D.N_COHORTS, 2*D.N_COHORTS),
    pop_size=D.POP_SIZE,
    diagnostic=P.Diagnostic.NSB
)

## initializatino based on generating fixed parameters
##create a multi-cohort to simulate under combo therapy
# multiCohort_NSB = Cls.MultiCohort(
#     ids=range(D.N_COHORTS, 2*D.N_COHORTS),
#     pop_size=D.POP_SIZE,
#     parameters=P.ParametersFixed(diagnostic=P.Diagnostic.NSB)
# )

multiCohort_NSB.simulate(sim_length=D.SIM_LENGTH)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=multiCohort_SOC.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.SOC)
Support.print_outcomes(multi_cohort_outcomes=multiCohort_NSB.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.NSB)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_SOC=multiCohort_SOC.multiCohortOutcomes,
                                            multi_cohort_outcomes_NSB=multiCohort_NSB.multiCohortOutcomes)

# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_SOC=multiCohort_SOC.multiCohortOutcomes,
                                   multi_cohort_outcomes_NSB=multiCohort_NSB.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_SOC=multiCohort_SOC.multiCohortOutcomes,
                       multi_cohort_outcomes_NSB=multiCohort_NSB.multiCohortOutcomes)
