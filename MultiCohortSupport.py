import InputData as D
import SimPy.SamplePathClasses as PathCls
import SimPy.FigureSupport as Figs
import SimPy.StatisticalClasses as Stat
import SimPy.EconEvalClasses as Econ
import matplotlib.pyplot as plt


def print_outcomes(multi_cohort_outcomes, diagnostic):
    """ prints the outcomes of a simulated cohort
    :param multi_cohort_outcomes: outcomes of a simulated multi-cohort
    :param therapy_name: the name of the selected therapy
    """
    # mean and prediction interval of patient survival time
    survival_mean_PI_text = multi_cohort_outcomes.statMeanSurvivalTime\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=2)

    mortality56Day_mean_PI_text = multi_cohort_outcomes.statMortality56Day\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=3,
                                         form=',')

    mortality2Month_mean_PI_text = multi_cohort_outcomes.statMortality2Month\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=3,
                                         form=',')

    mortality1Year_mean_PI_text = multi_cohort_outcomes.statMortality1Year\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=3,
                                         form=',')

    mortality2Year_mean_PI_text = multi_cohort_outcomes.statMortality2Year\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=3,
                                         form=',')

    mortality5Year_mean_PI_text = multi_cohort_outcomes.statMortality5Year\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=3,
                                         form=',')

    nTBM_mean_PI_text = multi_cohort_outcomes.statNTBM\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    nHospitalized_mean_PI_text = multi_cohort_outcomes.statNHospitalized\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    TotalYLL_mean_PI_text = multi_cohort_outcomes.statTotalYLL\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and prediction interval text of discounted total cost
    cost_mean_PI_text = multi_cohort_outcomes.statMeanCost\
        .get_formatted_mean_and_interval(interval_type='p',
                                         alpha=D.ALPHA,
                                         deci=0,
                                         form=',')

    # mean and prediction interval text of discounted total cost
    # costPresenting_mean_PI_text = multi_cohort_outcomes.statMeanCostPresenting\
    #     .get_formatted_mean_and_interval(interval_type='p',
    #                                      alpha=D.ALPHA,
    #                                      deci=0,
    #                                      form=',')
    # print outcomes
    print(diagnostic)
    print("  Estimate of mean survival time and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          survival_mean_PI_text)

    print("  Estimate of 56-day mortality and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          mortality56Day_mean_PI_text)
    print("  Estimate of 2-month mortality and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          mortality2Month_mean_PI_text)
    print("  Estimate of 1-year mortality and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          mortality1Year_mean_PI_text)
    print("  Estimate of 2-year mortality and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          mortality2Year_mean_PI_text)
    print("  Estimate of 5-year mortality and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          mortality5Year_mean_PI_text)
    print("  Estimate of number of cases of TB meningitis and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          nTBM_mean_PI_text)
    print("  Estimate of number of hospitalizations and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          nHospitalized_mean_PI_text)
    print("  Estimate of total Years of Life Lost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          TotalYLL_mean_PI_text)
    print("  Estimate of mean discounted cost and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
          cost_mean_PI_text)
    # print("  Estimate of mean discounted cost (Patients Presenting) and {:.{prec}%} uncertainty interval:".format(1 - D.ALPHA, prec=0),
    #       costPresenting_mean_PI_text)
    print("")


def plot_survival_curves_and_histograms(multi_cohort_outcomes_SOC, multi_cohort_outcomes_NSB):
    """ plot the survival curves and the histograms of survival times
    :param multi_cohort_outcomes_SOC: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_NSB: outcomes of a multi-cohort simulated under combination therapy
    """

    # get survival curves of both treatments
    sets_of_survival_curves = [
        multi_cohort_outcomes_SOC.survivalCurves,
        multi_cohort_outcomes_NSB.survivalCurves
    ]

    # graph survival curve
    PathCls.graph_sets_of_sample_paths(
        sets_of_sample_paths=sets_of_survival_curves,
        title='Survival Curves',
        x_label='Simulation Time Step (week)',
        y_label='Number of Patients Alive',
        legends=['SOC Diagnostic', 'NSB Diagnostic'],
        transparency=0.4,
        color_codes=['green', 'blue']
    )

    # # histograms of survival times
    # set_of_survival_times = [
    #     multi_cohort_outcomes_SOC.meanSurvivalTimes,
    #     multi_cohort_outcomes_NSB.meanSurvivalTimes
    # ]
    #
    # # graph histograms
    # Figs.graph_histograms(
    #     data_sets=set_of_survival_times,
    #     title='Histograms of Average Patient Survival Time',
    #     x_label='Survival Time (year)',
    #     y_label='Counts',
    #     bin_width=0.25,
    #     x_range=[5.25, 17.75],
    #     legends=['SOC Diagnostic', 'NSB Diagnostic'],
    #     color_codes=['green', 'blue'],
    #     transparency=0.5
    # )


def print_comparative_outcomes(multi_cohort_outcomes_SOC, multi_cohort_outcomes_NSB):
    """ prints average increase in survival time, discounted cost, and discounted utility
    under combination therapy compared to mono therapy
    :param multi_cohort_outcomes_mono: outcomes of a multi-cohort simulated under mono therapy
    :param multi_cohort_outcomes_combo: outcomes of a multi-cohort simulated under combination therapy
    """

    # increase in mean survival time under combination therapy with respect to mono therapy
    increase_mean_survival_time = Stat.DifferenceStatPaired(
        name='Increase in mean survival time',
        x=multi_cohort_outcomes_NSB.meanSurvivalTimes,
        y_ref=multi_cohort_outcomes_SOC.meanSurvivalTimes)

    # estimate and PI
    estimate_PI = increase_mean_survival_time.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean survival time and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean number of hospitalizations
    increase_mean_nHosp = Stat.DifferenceStatPaired(
        name='Increase in mean number of kids hospitalized',
        x=multi_cohort_outcomes_NSB.nHospitalized,
        y_ref=multi_cohort_outcomes_SOC.nHospitalized)

    # estimate and PI
    estimate_PI = increase_mean_nHosp.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean number of hospitalizations and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean number of YLLs
    increase_mean_YLLs = Stat.DifferenceStatPaired(
        name='Increase in mean number of Years of Life Lost',
        x=multi_cohort_outcomes_NSB.totalYLL,
        y_ref=multi_cohort_outcomes_SOC.totalYLL)

    # estimate and PI
    estimate_PI = increase_mean_YLLs.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean number of Years of Life Lost and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean number of patients w/ TBM
    increase_mean_TBM = Stat.DifferenceStatPaired(
        name='Increase in mean number of cases of TB meningitis',
        x=multi_cohort_outcomes_NSB.nTBM,
        y_ref=multi_cohort_outcomes_SOC.nTBM)

    # estimate and PI
    estimate_PI = increase_mean_TBM.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean number of cases of TB meningitis and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean 2-month mortality
    increase_mean_mortality2Month = Stat.DifferenceStatPaired(
        name='Increase in mean 2-month mortality',
        x=multi_cohort_outcomes_NSB.mortality2Month,
        y_ref=multi_cohort_outcomes_SOC.mortality2Month)

    # estimate and PI
    estimate_PI = increase_mean_mortality2Month.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean 2-month mortality and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean 2-year mortality
    increase_mean_mortality2Year = Stat.DifferenceStatPaired(
        name='Increase in mean 2-year mortality',
        x=multi_cohort_outcomes_NSB.mortality2Years,
        y_ref=multi_cohort_outcomes_SOC.mortality2Years)

    # estimate and PI
    estimate_PI = increase_mean_mortality2Year.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean 2-year mortality and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean 5-year mortality
    increase_mean_mortality5Year = Stat.DifferenceStatPaired(
        name='Increase in mean 5-year mortality',
        x=multi_cohort_outcomes_NSB.mortality5Years,
        y_ref=multi_cohort_outcomes_SOC.mortality5Years)

    # estimate and PI
    estimate_PI = increase_mean_mortality5Year.get_formatted_mean_and_interval(interval_type='p',
                                                                              alpha=D.ALPHA,
                                                                              deci=2)
    print("Increase in mean 5-year mortality and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)

    # increase in mean discounted cost under combination therapy with respect to mono therapy
    increase_mean_discounted_cost = Stat.DifferenceStatPaired(
        name='Increase in mean discounted cost',
        x=multi_cohort_outcomes_NSB.meanCosts,
        y_ref=multi_cohort_outcomes_SOC.meanCosts)

    # estimate and PI
    estimate_PI = increase_mean_discounted_cost.get_formatted_mean_and_interval(interval_type='p',
                                                                                alpha=D.ALPHA,
                                                                                deci=2,
                                                                                form=',')
    print("Increase in mean discounted cost and {:.{prec}%} uncertainty interval:"
          .format(1 - D.ALPHA, prec=0),
          estimate_PI)


    # # increase in mean discounted cost under combination therapy with respect to mono therapy
    # increase_mean_discounted_cost_Presenting = Stat.DifferenceStatPaired(
    #     name='Increase in mean discounted cost (among patients presenting)',
    #     x=multi_cohort_outcomes_NSB.meanCostPresenting,
    #     y_ref=multi_cohort_outcomes_SOC.meanCostPresenting)
    #
    # # estimate and PI
    # estimate_PI = increase_mean_discounted_cost_Presenting.get_formatted_mean_and_interval(interval_type='p',
    #                                                                             alpha=D.ALPHA,
    #                                                                             deci=2,
    #                                                                             form=',')
    # print("Increase in mean discounted cost (among patients presenting) and {:.{prec}%} uncertainty interval:"
    #       .format(1 - D.ALPHA, prec=0),
    #       estimate_PI)

    # # increase in mean discounted QALY under combination therapy with respect to mono therapy
    # increase_mean_discounted_qaly = Stat.DifferenceStatPaired(
    #     name='Increase in mean discounted QALY',
    #     x=multi_cohort_outcomes_combo.meanQALYs,
    #     y_ref=multi_cohort_outcomes_mono.meanQALYs)
    #
    # # estimate and PI
    # estimate_PI = increase_mean_discounted_qaly.get_formatted_mean_and_interval(interval_type='p',
    #                                                                             alpha=D.ALPHA,
    #                                                                             deci=2)
    # print("Increase in mean discounted utility and {:.{prec}%} uncertainty interval:"
    #       .format(1 - D.ALPHA, prec=0),
    #       estimate_PI)
    #

def report_CEA_CBA(multi_cohort_outcomes_SOC, multi_cohort_outcomes_NSB):
    """ performs cost-effectiveness and cost-benefit analyses
    :param multi_cohort_outcomes_SOC: outcomes of a multi-cohort simulated under SOC diagnostic
    :param multi_cohort_outcomes_NSB: outcomes of a multi-cohort simulated under NSB diagnostic
    """

    # define two strategies
    SOC_diagnostic_strategy = Econ.Strategy(
        name='SOC Diagnostic',
        cost_obs=multi_cohort_outcomes_SOC.meanCosts,
        effect_obs=multi_cohort_outcomes_SOC.totalYLL,
        color='green'
    )
    NSB_diagnostic_strategy = Econ.Strategy(
        name='NSB Diagnostic',
        cost_obs=multi_cohort_outcomes_NSB.meanCosts,
        effect_obs=multi_cohort_outcomes_NSB.totalYLL,
        color='blue'
    )

    # do CEA
    CEA = Econ.CEA(
        strategies=[SOC_diagnostic_strategy, NSB_diagnostic_strategy],
        if_paired=True,
        health_measure='d'
    )

    # show the cost-effectiveness plane
    show_ce_figure(CEA=CEA)

    # report the CE table
    CEA.build_CE_table(
        interval_type='p',  # prediction intervals
        alpha=D.ALPHA,
        cost_digits=0,
        effect_digits=2,
        icer_digits=2)

    # CBA
    NBA = Econ.CBA(
        strategies=[SOC_diagnostic_strategy, NSB_diagnostic_strategy],
        if_paired=True,
        health_measure='d'
    )
    # show the net monetary benefit figure
    NBA.graph_incremental_NMBs(
        min_wtp=0,
        max_wtp=50000,
        title='Cost-Benefit Analysis',
        x_label='Willingness-To-Pay for One Additional QALY ($)',
        y_label='Incremental Net Monetary Benefit ($)',
        interval_type='p',
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
        # add the cloud
        plt.scatter(s.effectObs, s.costObs,
                    c=s.color,  # color of dots
                    alpha=0.15,  # transparency of dots
                    s=25,  # size of dots
                    )

    plt.legend()        # show the legend
    plt.axhline(y=0, c='k', linewidth=0.5)  # horizontal line at y = 0
    plt.axvline(x=0, c='k', linewidth=0.5)  # vertical line at x = 0
    plt.xlim([-2.5, 5])              # x-axis range
    plt.ylim([-50, 1000])     # y-axis range
    plt.title('Cost-Effectiveness Analysis')
    plt.xlabel('Additional YLL')
    plt.ylabel('Additional discounted cost')
    plt.show()
