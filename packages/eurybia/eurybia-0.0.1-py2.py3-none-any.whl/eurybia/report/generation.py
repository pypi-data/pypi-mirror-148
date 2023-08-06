"""
Report generation helper module.
"""
from datetime import datetime

# import papermill as pm
from typing import Optional

import datapane as dp
import pandas as pd
from shapash.explainer.smart_explainer import SmartExplainer
from eurybia import SmartDrift
from eurybia.report.project_report import DriftReport


def _get_summary(dr: DriftReport, project_info_file: str, config: Optional[dict]) -> dp.Page:
    """
    This function generates and returns a Datapane page containing the Eurybia report summary

    Parameters
    ----------
    dr : DriftReport
        DriftReport object
    project_info_file : str
        Path to the file used to display some information about the project in the report.
    config : dict, optional
        Report configuration options.
    Returns
    ----------
    datapane.Page
    """
    # Summary
    report_update = dp.BigNumber(heading="Report last updated", value=datetime.now().strftime("%Y-%m-%d %H:%M"))

    title_block = []
    title_block += [dp.HTML(dr.display_title_description())]
    if config is not None:
        if "title_description" in config.keys() and config["title_description"] != "":
            title_block += [dp.Text(config["title_description"])]

    contents_block = []
    contents_block += [dp.Text("## Eurybia Report contents")]
    if project_info_file is not None:
        contents_block += [dp.Text("Project information : information and context of the report")]
    contents_block += [
        dp.Text("Consistency Analysis : checking features and their modalities"),
        dp.Text("Data drift : display of all data drift analyses"),
    ]
    if dr.smartdrift.data_modeldrift is not None:
        contents_block += [dp.Text("Model drift : display of all model drift analyses")]

    auc_block = dp.BigNumber(heading="AUC", value=round(dr.smartdrift.auc, 2))

    page_summary = dp.Page(
        title="Summary",
        blocks=[
            dp.Group(blocks=title_block, columns=1),
            dp.Group(
                dp.Text("![](https://raw.githubusercontent.com/MAIF/shapash/master/docs/_static/shapash-resize.png)"),
                dp.Group(auc_block, report_update, columns=2),
                columns=2,
            ),
            dp.Group(blocks=contents_block, columns=1),
        ],
    )
    return page_summary


def _dict_to_text_blocks(text_dict, level=1):
    """
    This function recursively explores the dict and returns a Datapane Group containing other groups and text blocks fed with the dict
    Parameters
    ----------
    text_dict: dict
        This dict must contain string as keys, and dicts or strings as values
    level: int = 1
        Recursion level, starting at 1 to allow for direct string manipulation
    Returns
    ----------
    datapane.Group
        Group of blocks
    """
    blocks = []
    left_text, right_text = "", ""
    for k, v in text_dict.items():
        if isinstance(v, (str, int, float)) or v is None:
            if k.lower() == "date" and v.lower() == "auto":
                v = str(datetime.now())[:-7]
            left_text += "#" * 4 + " " + k + " :  \n"
            right_text += "#" * 4 + " " + str(v) + "  \n"
        elif isinstance(v, dict):
            if left_text != "" and right_text != "":
                blocks.append(dp.Group(dp.Text(left_text), dp.Text(right_text), columns=2))
                left_text, right_text = "", ""
            blocks.append(
                dp.Group(dp.Text("#" * min(level, 6) + " " + str(k)), _dict_to_text_blocks(v, level + 1), columns=1)
            )
    if left_text != "" and right_text != "":
        blocks.append(dp.Group(dp.Text(left_text), dp.Text(right_text), columns=2))
    return dp.Group(blocks=blocks, columns=1)


def _get_project_info(dr: DriftReport) -> dp.Page:
    """
    This function generates and returns a Datapane page from a dict containing dicts and strings

    Parameters
    ----------
    dr : DriftReport
        DriftReport object

    Returns
    ----------
    datapane.Page
    """
    if dr.metadata is None:
        return None
    page_info = dp.Page(
        title="Project information",
        blocks=[_dict_to_text_blocks(dr.metadata)],
    )
    return page_info


def _get_consistency_analysis(dr: DriftReport) -> dp.Page:
    """
    This function generates and returns a Datapane page containing the Eurybia consistency analysis

    Parameters
    ----------
    dr : DriftReport
        DriftReport object

    Returns
    ----------
    datapane.Page
    """
    # Title
    blocks = [dp.Text("# Consistency Analysis")]

    # Manually ignored coluumns
    ignore_cols = pd.DataFrame({"ignore_cols": dr.smartdrift.ignore_cols}).rename(
        columns={"ignore_cols": "Ignored columns"}
    )
    blocks += [
        dp.Text("## Columns ignored in the report"),
        dp.Text(
            """
            This section will display the columns that have been manually excluded from the analysis.
            """
        ),
    ]
    if len(ignore_cols) > 0:
        blocks += [dp.Table(data=ignore_cols)]
    else:
        blocks += [dp.Text("No columns are set to be ignored.")]

    # Column mismatches
    blocks += [
        dp.Text("## Consistency checks allowing to detect if the columns match between the 2 datasets."),
        dp.Text(
            """
            The columns identified in this section have been removed from the analysis displayed in the report,
            as their mere presence would always be sufficient for the discriminator model to perfectly tell which dataset is which (maximal data drift, AUC=1).
            """
        ),
    ]
    for k, v in dr.smartdrift.pb_cols.items():
        if len(v) > 0:
            blocks += [dp.Table(data=pd.DataFrame(v).transpose())]
        else:
            blocks += [dp.Text(f"No {k.lower()} have been detected.")]

    blocks += [
        dp.Text("### Distinct values identified"),
        dp.Text(
            """
            This section will display the columns where they are differences between
            df_baseline and df_current in terms of modalities in
            categorical features.
            This part of Consistency Analysis has been done on a sample of both df_baseline
            and df_current. It's possible that the identified missing or added modalities
            where just not in the samples.
            The identified columns in this section have been kept for the analysis
            displayed in the report.
            """
        ),
    ]
    if len(dr.smartdrift.err_mods) > 0:
        blocks += [
            dp.Table(
                data=pd.DataFrame(dr.smartdrift.err_mods)
                .rename(columns={"err_mods": "Modalities present in one dataset and absent in the other :"})
                .transpose()
            )
        ]
    else:
        blocks += [dp.Text("No modalities have been detected as present in one dataset and absent in the other.")]

    page_consistency = dp.Page(title="Consistency Analysis", blocks=blocks)
    return page_consistency


def _get_datadrift(dr: DriftReport) -> dp.Page:
    """
    This function generates and returns a Datapane page containing the Eurybia data drift analysis

    Parameters
    ----------
    dr : DriftReport
        DriftReport object

    Returns
    ----------
    datapane.Page
    """
    # Loop for save in list plots of display analysis
    plot_dataset_analysis = []
    table_dataset_analysis = []
    fig_list, labels, table_list = dr.display_dataset_analysis(global_analysis=False)["univariate"]
    for i in range(len(labels)):
        plot_dataset_analysis.append(dp.Plot(fig_list[i], label=labels[i]))
        table_dataset_analysis.append(dp.Table(table_list[i], label=labels[i]))

    # Loop for save in list plots of display analysis
    plot_datadrift_contribution = []
    fig_list, labels = dr.display_model_contribution()
    for i in range(len(labels)):
        plot_datadrift_contribution.append(dp.Plot(fig_list[i], label=labels[i]))
    blocks = [
        dp.Text("# Data drift"),
        dp.Text(
            """The data drift detection methodology is based on the ability of a model to discriminate whether
        an individual belongs to one of the two datasets.
        For this purpose a target 0 is assigned to the baseline dataset and a target 1 to the current dataset.
        Then a classification model (catboost) is learned to predict this target.
        The level of capacity of the data drift classifier to detect if an individual belongs to one of the 2 datasets represents
        the level of difference between the 2 datasets."""
        ),
        dp.Text("## Detection data drift performance"),
        dp.Text("### Performance of detection drift model"),
        dp.Text(
            """The closer your AUC is from 0.5 the less your data drifted.
             The closer your AUC is from 1 the more your data drifted"""
        ),
        dp.BigNumber(heading="AUC", value=round(dr.smartdrift.auc, 2)),
        dp.Plot(dr.smartdrift.plot.generate_fig_auc()),
        dp.Text("## Importance of features in data drift"),
        dp.Text("### Global feature importance plot"),
        dp.Text(
            """This graph represents the variables in the data drift classification
         model that are most important to differentiate between the two datasets."""
        ),
        dp.Plot(dr.explainer.plot.features_importance()),
    ]
    if dr.smartdrift.deployed_model is not None:
        blocks += [
            dp.Text("### Feature importance overview"),
            dp.Text(
                """This graph compares the importance of variables between the data drift classifier model and the deployed model.
        This allows us to put into perspective the importance of data drift in relation to the impacts to be expected on the deployed model.
        If the variable is at the top left, it means that the variable is very important for data drift classification, but that the variable
        has little influence on the deployed model. If the variable is at the bottom right, it means that the variable has
        little importance for data drift classification, and that the variable has a lot of influence on the deployed model."""
            ),
            dp.Plot(dr.smartdrift.plot.scatter_feature_importance()),
        ]
    blocks += [
        dp.Text("## Dataset analysis"),
        dp.Text(
            """This section provides numerical summaries of the 2 datasets, and graphical analyses of the distributions between
        the 2 datasets.
        This allows the analysis of variables that are important for drift detection."""
        ),
        dp.Text("### Global analysis"),
        dp.Table(dr._display_dataset_analysis_global()),
        dp.Text("### Univariate analysis"),
        dp.Text(
            """This graphs shows a particular feature's distribution over its possible values. In the drop-down menu, the variables
        are sorted by importance of the variables in the data drift classification. For categorical features,
        the possible values are sorted by descending difference between the two datasets."""
        ),
        # TBD
        dp.Select(blocks=plot_dataset_analysis),
        dp.Select(blocks=table_dataset_analysis),
    ]
    if dr.smartdrift.deployed_model is not None:
        blocks += [
            dp.Text("### Distribution of predicted values"),
            dp.Text(
                "This graph shows distributions of the production model outputs on both historical and current datasets."
            ),
            dp.Plot(
                dr.smartdrift.plot.generate_fig_univariate(
                    df_all=dr.smartdrift.df_predict,
                    col="Score",
                    hue="dataset",
                    dict_color_palette=dr.dict_color_palette,
                )
            ),
        ]
    blocks += [
        dp.Text("## Feature contribution on data drift's detection"),
        dp.Text(
            """This graph represents the contribution of a variable to the data drift detection.
        This graph can help to understand the drift when the analysis of the dataset, either numerical or graphical,
        does not allow a clear understanding. In the drop-down menu, the variables are sorted by importance of the variables
        in the data drift detection."""
        ),
        dp.Select(blocks=plot_datadrift_contribution),
    ]
    if dr.smartdrift.historical_auc is not None:
        blocks += [
            dp.Text("## Historical Data drift"),
            dp.Text("This graph displays performance history of datadrift classifier"),
            dp.Plot(dr.smartdrift.plot.generate_auc_historical()),
        ]
    page_datadrift = dp.Page(title="Data drift", blocks=blocks)
    return page_datadrift


def _get_modeldrift(dr: DriftReport) -> dp.Page:
    """
    This function generates and returns a Datapane page containing the Eurybia model drift analysis

    Parameters
    ----------
    dr : DriftReport
        DriftReport object

    Returns
    ----------
    datapane.Page
    """
    # Loop for save in list plots of display model drift
    if dr.smartdrift.data_modeldrift is not None:
        plot_modeldrift = []
        fig_list, labels = dr.display_data_modeldrift()
        if labels == []:
            plot_modeldrift = dp.Plot(fig_list[0])
            modeldrift_plot = plot_modeldrift
        else:
            for i in range(len(labels)):
                plot_modeldrift.append(dp.Plot(fig_list[i], label=labels[i]))
            modeldrift_plot = dp.Select(blocks=plot_modeldrift, label="reference_columns")
    else:
        modeldrift_plot = dp.Text("## Smartdrift.data_modeldrift is None")
    blocks = [
        dp.Text("# Model drift"),
        dp.Text(
            """This section allows you to add monitoring of the production model's performance over time.
    This is done by adding the performance history as input"""
        ),
        dp.Text("## Performance's Evolution on production Model"),
        dp.Text("This graph displays performance history of model in production"),
        modeldrift_plot,
    ]
    page_modeldrift = dp.Page(title="Model drift", blocks=blocks)
    return page_modeldrift


def execute_report(
    smartdrift: SmartDrift,
    explainer: SmartExplainer,
    project_info_file: str,
    output_file: str,
    config: Optional[dict] = None,
):
    """
    Creates the report

    Parameters
    ----------
    smartdrift : eurybia.core.smartdrift.SmartDrift object
        Compiled SmartDrift class
    explainer : shapash.explainer.smart_explainer.SmartExplainer object
        Compiled shapash explainer.
    project_info_file : str
        Path to the file used to display some information about the project in the report.
    config : dict, optional
        Report configuration options.
    output_file : str
            Path to the HTML file to write
    """

    if config is None:
        config = {}

    dr = DriftReport(
        smartdrift=smartdrift,
        explainer=explainer,  # rename to match kwarg
        project_info_file=project_info_file,
        config=config,
    )
    pages = []
    pages.append(_get_summary(dr, project_info_file, config))
    if project_info_file is not None:
        pages.append(_get_project_info(dr))
    pages.append(_get_consistency_analysis(dr))
    pages.append(_get_datadrift(dr))
    if dr.smartdrift.data_modeldrift is not None:
        pages.append(_get_modeldrift(dr))

    report = dp.Report(blocks=pages)
    report._save(
        path=output_file, open=False, formatting=dp.ReportFormatting(light_prose=False, width=dp.ReportWidth.MEDIUM)
    )