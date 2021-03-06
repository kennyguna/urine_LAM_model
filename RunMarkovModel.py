import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Fig

# create a cohort
myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      parameters=P.ParametersFixed(diagnostic=P.Diagnostic.SOC))

# simulate the cohort over the specified time steps
myCohort.simulate(sim_length=D.SIM_LENGTH)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort.cohortOutcomes,
                       diagnostic_name=P.Diagnostic.SOC)

# histograms of the simulated cohort
Support.print_histograms(sim_outcomes=myCohort.cohortOutcomes,
                         diagnostic_name=P.Diagnostic.SOC)

# create a cohort
myCohort_NSB = Cls.Cohort(id=2,
                      pop_size=D.POP_SIZE,
                      parameters=P.ParametersFixed(diagnostic=P.Diagnostic.NSB))

# simulate the cohort over the specified time steps
myCohort_NSB.simulate(sim_length=D.SIM_LENGTH)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort_NSB.cohortOutcomes,
                       diagnostic_name=P.Diagnostic.NSB)

# histograms of the simulated cohort
Support.print_histograms(sim_outcomes=myCohort_NSB.cohortOutcomes,
                         diagnostic_name=P.Diagnostic.NSB)

PathCls.graph_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve (Standard of Care Diagnostic)',
    x_label='Time-Step (Week)',
    y_label='Number Survived')

PathCls.graph_sample_path(
    sample_path=myCohort_NSB.cohortOutcomes.nLivingPatients,
    title='Survival Curve (SOC + Urine LAM)',
    x_label='Time-Step (Week)',
    y_label='Number Survived')

survival_curves = [
    myCohort.cohortOutcomes.nLivingPatients,
    myCohort_NSB.cohortOutcomes.nLivingPatients
]

# graph survival curve
# graph survival curve
PathCls.graph_sample_paths(
    sample_paths=survival_curves,
    title='Survival curve',
    x_label='Simulation time step (year)',
    y_label='Number of alive patients',
    legends=['SOC Diagnostic', 'NSB Diagnostic']
)

# Fig.graph_histogram(
#     data=myCohort.cohortOutcomes.costs,
#     title=f'Histogram of Cost {diagnostic}',
#     x_label='Cost (Dollars)',
#     y_label='Count',
#     bin_width=1)
#
# Fig.graph_histogram(
#     data=myCohort.cohortOutcomes.costsPresenting,
#     title=f'Histogram of Cost for Patients who Present {diagnostic}',
#     x_label='Cost (Dollars)',
#     y_label='Count',
#     bin_width=1)

# report the CEA results
Support.report_CEA_CBA(sim_outcomes_SOC=myCohort.cohortOutcomes,
                       sim_outcomes_NSB=myCohort_NSB.cohortOutcomes)
