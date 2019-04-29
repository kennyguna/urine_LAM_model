import InputData as D
import ParameterClasses as P
import MarkovModelClasses as Cls
import Support as Support
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Fig

# selected therapy
diagnostic = P.Diagnostic.SOC

# create a cohort
myCohort = Cls.Cohort(id=1,
                      pop_size=D.POP_SIZE,
                      parameters=P.ParametersFixed(diagnostic=diagnostic))

# simulate the cohort over the specified time steps
myCohort.simulate(sim_length=D.SIM_LENGTH)

# print(myCohort.cohortOutcomes.nDX_TBM)
# print(myCohort.cohortOutcomes.timesDX_TBMtoDEAD)
# print(myCohort.cohortOutcomes.nDX_TBD)
# print(myCohort.cohortOutcomes.timesDX_TBDtoDEAD)
# print(myCohort.cohortOutcomes.timesDX_TBDtoCLEARED)

# print the outcomes of this simulated cohort
Support.print_outcomes(sim_outcomes=myCohort.cohortOutcomes,
                       diagnostic_name=diagnostic)

# histograms of the simulated cohort
# Support.print_histograms(sim_outcomes=myCohort.cohortOutcomes,
#                          diagnostic_name=diagnostic)

PathCls.graph_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title=f'Survival Curve {diagnostic}',
    x_label='Time-Step (Week)',
    y_label='Number Survived')

Fig.graph_histogram(
    data=myCohort.cohortOutcomes.costs,
    title=f'Histogram of Cost {diagnostic}',
    x_label='Cost (Dollars)',
    y_label='Count',
    bin_width=1)

Fig.graph_histogram(
    data=myCohort.cohortOutcomes.costsPresenting,
    title=f'Histogram of Cost for Patients who Present {diagnostic}',
    x_label='Cost (Dollars)',
    y_label='Count',
    bin_width=1)
