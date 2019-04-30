import CalibrationClasses as Cls
import CalibrationSettings as CalibSets
import SimPy.FigureSupport as Fig
import SimPy.SamplePathClasses as Path
import MultiCohortSupport as Support
import CalibrationParameterClasses as P


# initialize a calibrated model
calibrated_model_SOC = Cls.CalibratedModel(csv_file_name='CalibrationResults.csv')
calibrated_model_NSB = Cls.CalibratedModel(csv_file_name='CalibrationResults.csv')

# simulate the calibrated model
calibrated_model_SOC.simulate(num_of_simulated_cohorts=CalibSets.NUM_SIM_COHORTS,
                              cohort_size=CalibSets.SIM_POP_SIZE,
                              sim_length=CalibSets.SIM_LENGTH,
                              diagnostic=P.Diagnostic.SOC)

calibrated_model_NSB.simulate(num_of_simulated_cohorts=CalibSets.NUM_SIM_COHORTS,
                              cohort_size=CalibSets.SIM_POP_SIZE,
                              sim_length=CalibSets.SIM_LENGTH,
                              diagnostic=P.Diagnostic.NSB)


# plot the sample paths
Path.graph_sample_paths(
    sample_paths=calibrated_model_SOC.multiCohorts.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time (Week)',
    y_label='Number Survived',
    transparency=0.5)

Path.graph_sample_paths(
    sample_paths=calibrated_model_NSB.multiCohorts.multiCohortOutcomes.survivalCurves,
    title='Survival Curves',
    x_label='Time (Week)',
    y_label='Number Survived',
    transparency=0.5)

# plot the histogram of mean survival time
# Fig.graph_histogram(
#     data=calibrated_model.multiCohorts.multiCohortOutcomes.meanSurvivalTimes,
#     title='Histogram of Mean Survival Time',
#     x_label='Mean Survival Time (Week)',
#     y_label='Count',
#     bin_width=0.25,
#     x_range=[2.5, 21.5])

Support.print_outcomes(multi_cohort_outcomes=calibrated_model_SOC.multiCohorts.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.SOC)

Support.print_outcomes(multi_cohort_outcomes=calibrated_model_NSB.multiCohorts.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.NSB)

# print the estimates for the mean survival time and mean time to AIDS
Support.print_outcomes(multi_cohort_outcomes=calibrated_model_SOC.multiCohorts.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.SOC)
Support.print_outcomes(multi_cohort_outcomes=calibrated_model_NSB.multiCohorts.multiCohortOutcomes,
                       diagnostic=P.Diagnostic.NSB)

# draw survival curves and histograms
Support.plot_survival_curves_and_histograms(multi_cohort_outcomes_SOC=calibrated_model_SOC.multiCohorts.multiCohortOutcomes,
                                            multi_cohort_outcomes_NSB=calibrated_model_NSB.multiCohorts.multiCohortOutcomes)

# print comparative outcomes
Support.print_comparative_outcomes(multi_cohort_outcomes_SOC=calibrated_model_SOC.multiCohorts.multiCohortOutcomes,
                                   multi_cohort_outcomes_NSB=calibrated_model_NSB.multiCohorts.multiCohortOutcomes)

# report the CEA results
Support.report_CEA_CBA(multi_cohort_outcomes_SOC=calibrated_model_SOC.multiCohorts.multiCohortOutcomes,
                       multi_cohort_outcomes_NSB=calibrated_model_NSB.multiCohorts.multiCohortOutcomes)

# # report mean and projection interval
# print('Mean survival time and {:.{prec}%} projection interval:'.format(1 - CalibSets.ALPHA, prec=0),
#       calibrated_model.get_mean_survival_time_proj_interval(alpha=CalibSets.ALPHA))
