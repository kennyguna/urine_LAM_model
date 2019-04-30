import MultiCohortClasses as Cls
import ParameterClasses as P
import InputData as D
import MultiCohortSupport as Support
import SimPy.RandomVariantGenerators as RVGs
import SimPy.SamplePathClasses as Path
import SimPy.FigureSupport as Fig

# create multiple cohort
multiCohort = Cls.MultiCohort(
    ids=range(D.N_COHORTS),
    pop_size=D.POP_SIZE,
    parameters=P.ParametersFixed(diagnostic=P.Diagnostic.SOC))

multiCohort.simulate(sim_length=D.SIM_LENGTH)

# plot the sample paths
Path.graph_sample_paths(
    sample_paths=multiCohort.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time-Step (Week)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Fig.graph_histogram(
    data=multiCohort.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time',
    x_label='Mean Survival Time (Week)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.SOC)

# create multiple cohort
multiCohort_NSB = Cls.MultiCohort(
    ids=range(D.N_COHORTS, 2*D.N_COHORTS),
    pop_size=D.POP_SIZE,
    parameters=P.ParametersFixed(diagnostic=P.Diagnostic.NSB))

multiCohort_NSB.simulate(sim_length=D.SIM_LENGTH)

# plot the sample paths
Path.graph_sample_paths(
    sample_paths=multiCohort_NSB.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time-Step (Week)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of average survival time
Fig.graph_histogram(
    data=multiCohort_NSB.multiCohortOutcomes.meanSurvivalTimes,
    title='Histogram of Mean Survival Time',
    x_label='Mean Survival Time (Week)',
    y_label='Count')

# print the outcomes of this simulated cohort
Support.print_outcomes(multi_cohort_outcomes=multiCohort_NSB.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.NSB)
