import InputData as D
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Figs
import SimPy.StatisticalClasses as Stat
import SimPy.EconEvalClasses as Econ
import matplotlib.pyplot as plt


def print_outcomes(sim_outcomes, diagnostic_name):
    """ prints the outcomes of a simulated cohort
    :param sim_outcomes: outcomes of a simulated cohort
    :param diagnostic_name: the name of the selected diagnostic strategiy
    """
    # mean and confidence interval of patient survival time
    survival_mean_CI_text = sim_outcomes.statSurvivalTime\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=2)

    # # mean and confidence interval of event rates
    # time_INFECTEDtoHOSP_TBD_text = sim_outcomes.statTimeINFECTEDtoHOSP_TBD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_INFECTEDtoHOSP_TBM_text = sim_outcomes.statTimeINFECTEDtoHOSP_TBM\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_INFECTEDtoDX_TBD_text = sim_outcomes.statTimeINFECTEDtoDX_TBD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_INFECTEDtoCLEARED_text = sim_outcomes.statTimeINFECTEDtoCLEARED\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_CLEAREDtoDEAD_text = sim_outcomes.statTimeCLEAREDtoDEAD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_HOSP_TBDtoDEAD_text = sim_outcomes.statTimeHOSP_TBDtoDEAD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_HOSP_TBDtoDX_TBD_text = sim_outcomes.statTimeHOSP_TBDtoDX_TBD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_HOSP_TBMtoDEAD_text = sim_outcomes.statTimeHOSP_TBMtoDEAD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_HOSP_TBMtoDX_TBM_text = sim_outcomes.statTimeHOSP_TBMtoDX_TBM\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_DX_TBDtoDEAD_text = sim_outcomes.statTimeDX_TBDtoDEAD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_DX_TBDtoCLEARED_text = sim_outcomes.statTimeDX_TBDtoCLEARED\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_DX_TBMtoDEAD_text = sim_outcomes.statTimeDX_TBMtoDEAD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_DX_TBMtoCLEARED_text = sim_outcomes.statTimeDX_TBMtoCLEARED\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # # time spent in each state
    # time_INFECTED_text = sim_outcomes.statTimesINFECTED\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_HOSP_TBM_text = sim_outcomes.statTimesHOSP_TBM\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_HOSP_TBD_text = sim_outcomes.statTimesHOSP_TBD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_DX_TBD_text = sim_outcomes.statTimesDX_TBD\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_DX_TBM_text = sim_outcomes.statTimesDX_TBM\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)
    #
    # time_CLEARED_text = sim_outcomes.statTimesCLEARED\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)

    # mean and confidence interval text of discounted total cost
    cost_mean_CI_text = sim_outcomes.statCost\
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    costPresenting_mean_CI_text = sim_outcomes.statCostPresenting \
        .get_formatted_mean_and_interval(interval_type='c',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # # mean and confidence interval text of discounted total utility
    # utility_mean_CI_text = sim_outcomes.statUtility\
    #     .get_formatted_mean_and_interval(interval_type='c',
    #                                      alpha=D.ALPHA,
    #                                      deci=2)

    # print outcomes
    print(diagnostic_name)
    print("  Number of individuals hospitalized:", sim_outcomes.nHospitalized)
    print("  Total Years of Life Lost:", sim_outcomes.totalYLL)
    print("  56-day mortality after presenting:", sim_outcomes.nMortality56Day/D.POP_SIZE)
    print("  2-month mortality:", sim_outcomes.nMortality2Months/D.POP_SIZE)
    print("  1-year mortality:", sim_outcomes.nMortality1Year/D.POP_SIZE)
    print("  2-year mortality:", sim_outcomes.nMortality2Years/D.POP_SIZE)
    print("  5-year mortality:", sim_outcomes.nMortality5Years/D.POP_SIZE)

    print("  Number of individuals passing through state HOSP_TBM:", sim_outcomes.nHOSP_TBM)
    print("  Number of individuals passing through state HOSP_TBD:", sim_outcomes.nHOSP_TBD)
    print("  Number of individuals passing through state DX_TBM:", sim_outcomes.nDX_TBM)
    print("  Number of individuals passing through state DX_TBD:", sim_outcomes.nDX_TBD)
    print("  Number of individuals passing through state CLEARED:", sim_outcomes.nCLEARED)
    print("  Number of individuals passing through state DEAD:", sim_outcomes.nDEAD)

    print("  Estimate of mean survival time and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_CI_text)

    # print("  Estimate of mean time in state INFECTED and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_INFECTED_text)
    # print("  Estimate of mean time in state HOSP_TBD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_HOSP_TBD_text)
    # print("  Estimate of mean time in state HOSP_TBM and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_HOSP_TBM_text)
    # print("  Estimate of mean time in state DX_TBD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_DX_TBD_text)
    # print("  Estimate of mean time in state DX_TBM and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_DX_TBM_text)
    # print("  Estimate of mean time in state CLEARED and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_CLEARED_text)
    #
    # print("  Estimate of mean time from INFECTED to HOSP_TBD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_INFECTEDtoHOSP_TBD_text)
    # print("  Estimate of mean time from INFECTED to HOSP_TBM and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_INFECTEDtoHOSP_TBM_text)
    # print("  Estimate of mean time from INFECTED to DX_TBD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_INFECTEDtoDX_TBD_text)
    # print("  Estimate of mean time from INFECTED to CLEARED and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_INFECTEDtoCLEARED_text)
    # print("  Estimate of mean time from HOSP_TBD to DX_TBD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_HOSP_TBDtoDX_TBD_text)
    # print("  Estimate of mean time from HOSP_TBD to DEAD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_HOSP_TBDtoDEAD_text)
    # print("  Estimate of mean time from HOSP_TBM to DX_TBM and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_HOSP_TBMtoDX_TBM_text)
    # print("  Estimate of mean time from HOSP_TBM to DEAD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_HOSP_TBMtoDEAD_text)
    # print("  Estimate of mean time from DX_TBD to CLEARED and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_DX_TBDtoCLEARED_text)
    # print("  Estimate of mean time from DX_TBD to DEAD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_DX_TBDtoDEAD_text)
    # print("  Estimate of mean time from DX_TBM to CLEARED and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_DX_TBMtoCLEARED_text)
    # print("  Estimate of mean time from DX_TBM to DEAD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_DX_TBMtoDEAD_text)
    # print("  Estimate of mean time from CLEARED to DEAD and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       time_CLEAREDtoDEAD_text)

    print("  Estimate of discounted cost and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_CI_text)
    print("  Estimate of discounted cost among patients presenting and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
          costPresenting_mean_CI_text)
    # print("  Estimate of discounted utility and {:.{prec}%} confidence interval:".format(1 - D.ALPHA, prec=0),
    #       utility_mean_CI_text)
    print("")


def print_histograms(sim_outcomes, diagnostic_name):
    # plot the sample path (survival curve)
    PathCls.graph_sample_path(
        sample_path=sim_outcomes.nLivingPatients,
        title=f'Survival Curve {diagnostic_name}',
        x_label='Time-Step (Week)',
        y_label='Number Survived')

    # plot the histogram of survival times
    Figs.graph_histogram(
        data=sim_outcomes.survivalTimes,
        title=f'Histogram of Patient Survival Time {diagnostic_name}',
        x_label='Survival Time (Week)',
        y_label='Count',
        bin_width=1)

    # Figs.graph_histogram(
    #     data=sim_outcomes.timesINFECTEDtoHOSP_TBD,
    #     title=f'Histogram of INFECTED to HOSP_TBD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesINFECTEDtoHOSP_TBM,
    #     title=f'Histogram of INFECTED to HOSP_TBM {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesINFECTEDtoDX_TBD,
    #     title=f'Histogram of INFECTED to DX_TBD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesINFECTEDtoCLEARED,
    #     title=f'Histogram of INFECTED to CLEARED {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesCLEAREDtoDEAD,
    #     title=f'Histogram of CLEARED to DEAD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesHOSP_TBDtoDEAD,
    #     title=f'Histogram of HOSP_TBD to DEAD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesHOSP_TBDtoDX_TBD,
    #     title=f'Histogram of HOSP_TBD to DX_TBD {diagnostic_name}',
    #     x_label='Survival Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesHOSP_TBMtoDEAD,
    #     title=f'Histogram of HOSP_TBM to DEAD {diagnostic_name}',
    #     x_label='Survival Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesHOSP_TBMtoDX_TBM,
    #     title=f'Histogram of HOSP_TBM to DX_TBM {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesDX_TBDtoDEAD,
    #     title=f'Histogram of DX_TBD to DEAD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesDX_TBDtoCLEARED,
    #     title=f'Histogram of DX_TBD to CLEARED {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesDX_TBMtoDEAD,
    #     title=f'Histogram of DX_TBM to DEAD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesDX_TBMtoCLEARED,
    #     title=f'Histogram of DX_TBM to CLEARED {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesINFECTED,
    #     title=f'Histogram of INFECTED {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesHOSP_TBM,
    #     title=f'Histogram of HOSP_TBM {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesHOSP_TBD,
    #     title=f'Histogram of HOSP_TBD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesDX_TBD,
    #     title=f'Histogram of DX_TBD {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesDX_TBM,
    #     title=f'Histogram of DX_TBM {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)
    #
    # Figs.graph_histogram(
    #     data=sim_outcomes.timesCLEARED,
    #     title=f'Histogram of CLEARED {diagnostic_name}',
    #     x_label='Time (Week)',
    #     y_label='Count',
    #     bin_width=1)

    # Figs.graph_histogram(
    #     data=sim_outcomes.costs,
    #     title=f'Histogram of Cost {diagnostic_name}',
    #     x_label='Cost (Dollars)',
    #     y_label='Count',
    #     bin_width=1)

    Figs.graph_histogram(
        data=sim_outcomes.costsPresenting,
        title=f'Histogram of Cost (Patients Presenting) {diagnostic_name}',
        x_label='Cost (Dollars)',
        y_label='Count',
        bin_width=1)

def plot_survival_curves_and_histograms(sim_outcomes_mono, sim_outcomes_combo):
    """ draws the survival curves and the histograms of time until HIV deaths
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    survival_curves = [
        sim_outcomes_mono.nLivingPatients,
        sim_outcomes_combo.nLivingPatients
    ]

    # graph survival curve
    PathCls.graph_sample_paths(
        sample_paths=survival_curves,
        title='Survival curve',
        x_label='Simulation time step (year)',
        y_label='Number of alive patients',
        legends=['Mono Therapy', 'Combination Therapy']
    )

    # histograms of survival times
    set_of_survival_times = [
        sim_outcomes_mono.survivalTimes,
        sim_outcomes_combo.survivalTimes
    ]

    # graph histograms
    Figs.graph_histograms(
        data_sets=set_of_survival_times,
        title='Histogram of patient survival time',
        x_label='Survival time (year)',
        y_label='Counts',
        bin_width=1,
        legends=['Mono Therapy', 'Combination Therapy'],
        transparency=0.6
    )


def print_comparative_outcomes(sim_outcomes_mono, sim_outcomes_combo):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_survival_time = Stat.DifferenceStatIndp(
        name='Increase in mean survival time',
        x=sim_outcomes_combo.survivalTimes,
        y_ref=sim_outcomes_mono.survivalTimes)

    # estimate and CI
    estimate_CI = increase_survival_time.get_formatted_mean_and_interval(interval_type='c',
                                                                         alpha=D.ALPHA,
                                                                         deci=2)
    print("Increase in mean survival time and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_discounted_cost = Stat.DifferenceStatIndp(
        name='Increase in mean discounted cost',
        x=sim_outcomes_combo.costs,
        y_ref=sim_outcomes_mono.costs)

    # estimate and CI
    estimate_CI = increase_discounted_cost.get_formatted_mean_and_interval(interval_type='c',
                                                                           alpha=D.ALPHA,
                                                                           deci=2,
                                                                           form=',')
    print("Increase in mean discounted cost and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)

    # increase in mean discounted utility under combination therapy with respect to mono therapy
    increase_discounted_utility = Stat.DifferenceStatIndp(
        name='Increase in mean discounted utility',
        x=sim_outcomes_combo.utilities,
        y_ref=sim_outcomes_mono.utilities)

    # estimate and CI
    estimate_CI = increase_discounted_utility.get_formatted_mean_and_interval(interval_type='c',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean discounted utility and {:.{prec}%} confidence interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_CI)


def report_CEA_CBA(sim_outcomes_mono, sim_outcomes_combo):
    """ performs cost-effectiveness and cost-benefit analyses
    :param sim_outcomes_mono: outcomes of a cohort simulated under mono therapy
    :param sim_outcomes_combo: outcomes of a cohort simulated under combination therapy
    """

    # define two strategies
    mono_therapy_strategy = Econ.Strategy(
        name='Mono Therapy',
        cost_obs=sim_outcomes_mono.costs,
        effect_obs=sim_outcomes_mono.utilities,
        color='green'
    )
    combo_therapy_strategy = Econ.Strategy(
        name='Combination Therapy',
        cost_obs=sim_outcomes_combo.costs,
        effect_obs=sim_outcomes_combo.utilities,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[mono_therapy_strategy, combo_therapy_strategy],
        if_paired=False
    )

    # show the cost-effectiveness plane
    show_ce_figure(CEA=CEA)

    # report the CE table
    CEA.build_CE_table(
        interval_type='c',
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2)

    # CBA
    NBA = Econ.CBA(
        strategies=[mono_therapy_strategy, combo_therapy_strategy],
        if_paired=False
    )
    # show the net monetary benefit figure
    NBA.graph_incremental_NMBs(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-to-pay for one additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='c',
        show_legend=True,
        figure_size=(6, 5)
    )


def show_ce_figure(CEA):

    # create a cost-effectiveness plot
    plt.figure(figsize=(5, 5))

    # find the frontier (x, y)'s
    frontier_utilities = []
    frontier_costs = []
    for s in CEA.get_shifted_strategies_on_frontier():
        frontier_utilities.append(s.aveEffect)
        frontier_costs.append(s.aveCost)

    # draw the frontier line
    plt.plot(frontier_utilities, frontier_costs,
             c='k',  # color
             alpha=0.6,  # transparency
             linewidth=2,  # line width
             label="Frontier")  # label to show in the legend

    # add the strategies
    for s in CEA.get_shifted_strategies():
        # add the center of the cloud
        plt.scatter(s.aveEffect, s.aveCost,
                    c=s.color,      # color
                    alpha=1,        # transparency
                    marker='o',     # markers
                    s=75,          # marker size
                    label=s.name    # name to show in the legend
                    )

    plt.legend()        # show the legend
    plt.axhline(y=0, c='k', linewidth=0.5)  # horizontal line at y = 0
    plt.axvline(x=0, c='k', linewidth=0.5)  # vertical line at x = 0
    plt.xlim([-2.5, 10])              # x-axis range
    plt.ylim([-50000, 200000])     # y-axis range
    plt.title('Cost-Effectiveness Analysis')
    plt.xlabel('Additional discounted utility')
    plt.ylabel('Additional discounted cost')
    plt.show()

