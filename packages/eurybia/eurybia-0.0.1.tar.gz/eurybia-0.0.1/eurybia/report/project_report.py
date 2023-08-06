"""
Module used in the base_report notebook to generate report
"""
import copy
import logging
import os
from typing import Dict, Optional, Tuple, Union

import jinja2
import pandas as pd
import plotly
from shapash.explainer.smart_explainer import SmartExplainer

from eurybia.core.smartdrift import SmartDrift
from eurybia.report.common import compute_col_types, series_dtype

# from eurybia.smartdrift.smartdrift import SmartDrift
from eurybia.report.data_analysis import perform_global_dataframe_analysis, perform_univariate_dataframe_analysis
from eurybia.utils.io import load_yml
from eurybia.utils.utils import get_project_root

logging.basicConfig(level=logging.INFO)

template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(get_project_root(), "report", "html"))
template_env = jinja2.Environment(loader=template_loader)


dict_font = dict(family="Arial Black", size=18)


class DriftReport:
    """
    The DriftReport class allows to generate compare two datasets.
    One used to train the model the other build for production purposes.
    It analyzes the data and the model used in order to provide interesting
    insights that can be shared with non technical person.
    Parameters
    ----------
    explainer : shapash.explainer.smart_explainer.SmartExplainer
        A shapash SmartExplainer object that has already be compiled.
    project_info_file : str
        Path to the yml file containing information about the project (author, description, ...).
    config : dict, optional
        Contains configuration options for the report.
    df_baseline, df_current : pd.DataFrame
        Dataframes used for training session and production one.
    dataset_names : pd.DataFrame
        DataFrame used to specify names to display in report.
    Attributes
    ----------
    explainer : shapash.explainer.smart_explainer.SmartExplainer
         A shapash SmartExplainer object that has already be compiled.
    metadata : dict
        Information about the project (author, description, ...).
    df_predict : pd.DataFrame
        Dataframe of predicted values computed on both df_baseline and df_current.
    feature_importance : pd.DataFrame, optional (default: None)
        Dataframe of feature importance from production model and drift model.
    config : dict, optional
        Configuration options for the report.
    """

    def __init__(
        self,
        smartdrift: SmartDrift,
        explainer: SmartExplainer,
        project_info_file: Optional[str] = None,
        config: Optional[Dict] = None,
    ):
        self.smartdrift = smartdrift
        self.explainer = explainer
        if self.explainer.features_imp is None:
            self.explainer.compute_features_import(force=True)
        self.features_imp_list = self.explainer.features_imp[0].sort_values(ascending=False).index.to_list()  # type: ignore
        self.config = config if config is not None else dict()

        self.data_concat = self._create_data_drift(
            df_current=self.smartdrift.df_current,
            df_baseline=self.smartdrift.df_baseline,
            dataset_names=self.smartdrift.dataset_names,
        )
        self.dict_color_palette = {
            "true": (74 / 255, 99 / 255, 138 / 255, 0.7),
            "pred": (244 / 255, 192 / 255, 0),
            "train": (74 / 255, 99 / 255, 138 / 255, 0.7),
            "test": (244 / 255, 192 / 255, 0),
        }
        self.dict_color_palette[self.smartdrift.dataset_names["df_current"].values[0]] = (244 / 255, 192 / 255, 0)
        self.dict_color_palette[self.smartdrift.dataset_names["df_baseline"].values[0]] = (
            74 / 255,
            99 / 255,
            138 / 255,
            0.7,
        )

        if project_info_file is None:
            self.metadata = {"Tip": "You can add custom information here. Check our documentation !"}
        else:
            self.metadata = load_yml(path=project_info_file)

        if "title_story" in self.config.keys():
            self.title_story = self.config["title_story"]
        elif self.explainer.title_story != "":
            self.title_story = self.explainer.title_story
        else:
            self.title_story = "Eurybia report"

    @staticmethod
    def _get_values_and_name(
        y: Optional[Union[pd.DataFrame, pd.Series, list]], default_name: str
    ) -> Union[Tuple[list, str], Tuple[None, None]]:
        """
        Extracts vales and column name from a Pandas Series, DataFrame, or assign a default
        name if y is a list of values.
        Parameters
        ----------
        y : list or pd.Series or pd.DataFrame
            Column we want to extract the name and values
        default_name :
            Name assigned if no name was found for y
        Returns
        -------
        values : list
            list of values of y
        name : str
            name of y
        """
        if y is None:
            return None, None
        elif isinstance(y, pd.DataFrame):
            assert len(y.columns) == 1, "Number of columns found is greater than 1"
            name = y.columns[0]
            values = y.values[:, 0]
        elif isinstance(y, pd.Series):
            name = y.name
            values = y.values
        elif isinstance(y, list):
            name = default_name
            values = y
        else:
            raise ValueError(f"Cannot process following type : {type(y)}")
        return values, name

    @staticmethod
    def _create_data_drift(
        df_current: Optional[pd.DataFrame], df_baseline: Optional[pd.DataFrame], dataset_names: pd.DataFrame
    ) -> Union[pd.DataFrame, None]:
        """
        Creates a DataFrame that contains dataset used for
        training part and dataset used for production with the column 'data_drift_split'
        allowing to distinguish the values.
        Parameters
        ----------
        df_current : pd.DataFrame, optional
            dataset used for production, dataframe
        df_baseline : pd.DataFrame, optional
            dataset used for traning part, dataframe
        dataset_names : pd.DataFrame
            DataFrame used to specify names to display in report
        Returns
        -------
        pd.DataFrame
            The concatenation of df_baseline and df_current as a dataframe containing df_baseline and df_current values with
            a new 'data_train_test' column allowing to distinguish the values.
        """
        if (df_current is not None and "data_drift_split" in df_current.columns) or (
            df_baseline is not None and "data_drift_split" in df_baseline.columns
        ):
            raise ValueError('"data_drift_split" column must be renamed as it is used in ProjectReport')
        if df_current is None and df_baseline is None:
            return None
        return pd.concat(
            [
                df_current.assign(data_drift_split=dataset_names["df_current"].values[0])
                if df_current is not None
                else None,
                df_baseline.assign(data_drift_split=dataset_names["df_baseline"].values[0])
                if df_baseline is not None
                else None,
            ]
        ).reset_index(drop=True)

    def display_title_description(self):
        """
        Displays title of the report and its description if defined.
        """
        content = f"""<font size="+3"><p align="center"><b>{self.title_story}</b></p></font>"""
        return content

    def display_dataset_analysis(self, global_analysis: bool = True, univariate_analysis: bool = True):
        """
        This method performs and displays an exploration of the data given.
        It allows to compare train and test values for each part of the analysis.
        The parameters of the method allow to filter which part to display or not.
        Parameters
        ----------
        global_analysis : bool
            Whether or not to display the global analysis part
        univariate_analysis : bool
            Whether or not to display the univariate analysis part
        target_analysis : bool
            Whether or not to display the target analysis part that plots
            the distribution of the target variable
        multivariate_analysis : bool
            Whether or not to display the multivariate analysis part
        """
        res = {}
        if global_analysis:
            res["global"] = self._display_dataset_analysis_global()

        if univariate_analysis:
            plot_list, labels, table_list = self._perform_and_display_analysis_univariate(
                df=self.data_concat,
                col_splitter="data_drift_split",
                split_values=[
                    self.smartdrift.dataset_names["df_current"].values[0],
                    self.smartdrift.dataset_names["df_baseline"].values[0],
                ],
                names=[
                    self.smartdrift.dataset_names["df_current"].values[0],
                    self.smartdrift.dataset_names["df_baseline"].values[0],
                ],
                group_id="univariate",
                dict_color_palette=self.dict_color_palette,
            )
            res["univariate"] = (plot_list, labels, table_list)

        return res

    def _display_dataset_analysis_global(self):
        df_stats_global = self._stats_to_table(
            test_stats=perform_global_dataframe_analysis(self.smartdrift.df_current),
            train_stats=perform_global_dataframe_analysis(self.smartdrift.df_baseline),
            names=[
                self.smartdrift.dataset_names["df_current"].values[0],
                self.smartdrift.dataset_names["df_baseline"].values[0],
            ],
        )
        return df_stats_global

    def _perform_and_display_analysis_univariate(
        self,
        df: pd.DataFrame,
        col_splitter: str,
        split_values: list,
        names: list,
        group_id: str,
        dict_color_palette: dict,
    ):
        col_types = compute_col_types(df)
        n_splits = df[col_splitter].nunique()
        test_stats_univariate = perform_univariate_dataframe_analysis(
            df.loc[df[col_splitter] == split_values[0]], col_types=col_types
        )
        if n_splits > 1:
            train_stats_univariate = perform_univariate_dataframe_analysis(
                df.loc[df[col_splitter] == split_values[1]], col_types=col_types
            )

        univariate_features_desc = list()

        plot_list = []
        labels = []
        table_list = []
        for col in df.drop(col_splitter, axis=1)[self.features_imp_list].columns:
            try:
                fig = self.smartdrift.plot.generate_fig_univariate(
                    df_all=df, col=col, hue=col_splitter, dict_color_palette=dict_color_palette
                )
                plot_list.append(fig)
                labels.append(col)
                df_col_stats = self._stats_to_table(
                    test_stats=test_stats_univariate[col],
                    train_stats=train_stats_univariate[col] if n_splits > 1 else None,
                    names=names,
                )
                table_list.append(df_col_stats)
                inv_columns_dict = {v: k for k, v in self.explainer.columns_dict.items()}
                univariate_features_desc.append(
                    {
                        "feature_index": int(inv_columns_dict.get(col, 0)),
                        "name": col,
                        "type": str(series_dtype(df[col])),
                        "description": self.explainer.features_dict.get(col, ""),
                        "table": df_col_stats.to_html(classes="greyGridTable"),
                        "image": plotly.io.to_html(fig, include_plotlyjs=False, full_html=False),
                        "separator": "---",
                    }
                )
            except BaseException as e:
                raise Exception(
                    """
                There is a problem with the format of {} column between the two datasets.
                Error:
                """.format(
                        str(col)
                    )
                    + str(e)
                )
        return plot_list, labels, table_list

    @staticmethod
    def _stats_to_table(
        test_stats: dict,
        names: list,
        train_stats: Optional[dict] = None,
    ) -> pd.DataFrame:
        if train_stats is not None:
            return pd.DataFrame({names[1]: pd.Series(train_stats), names[0]: pd.Series(test_stats)})
        else:
            return pd.DataFrame({names[0]: pd.Series(test_stats)})

    def display_model_contribution(self):
        """
        Displays explainability of the model as computed in SmartPlotter object
        """
        explain_data = list()
        multiclass = True if (self.explainer._classes and len(self.explainer._classes) > 2) else False
        c_list = self.explainer._classes if multiclass else [0, 1]  # list just used for multiclass
        plot_list = []
        labels = []
        for index_label, label in enumerate(c_list):  # Iterating over all labels in multiclass case
            label_value = (
                self.smartdrift.dataset_names["df_baseline"].values[0]
                if label == 0
                else self.smartdrift.dataset_names["df_current"].values[0]
            )
            fig_features_importance = self.explainer.plot.features_importance(label=label)

            explain_contrib_data = list()
            for feature in self.features_imp_list:
                fig = self.explainer.plot.contribution_plot(feature, label=label, max_points=200)
                plot_list.append(fig)
                labels.append(feature)
                inv_columns_dict = {v: k for k, v in self.explainer.columns_dict.items()}
                explain_contrib_data.append(
                    {
                        "feature_index": int(inv_columns_dict[feature]),
                        "name": feature,
                        "description": self.explainer.features_dict[feature],
                        "plot": plotly.io.to_html(fig, include_plotlyjs=False, full_html=False),
                    }
                )
            explain_data.append(
                {
                    "index": index_label,
                    "name": label_value,
                    "feature_importance_plot": plotly.io.to_html(
                        fig_features_importance, include_plotlyjs=False, full_html=False
                    ),
                    "features": explain_contrib_data,
                }
            )
        return plot_list, labels

    def display_data_modeldrift(self):
        """
        Display modeldrift computed metrics when method 'drift' is used
        """
        if self.smartdrift.data_modeldrift is not None:
            plot_list = []
            labels = []
            # If you don't have reference_columns
            if self.smartdrift.data_modeldrift.iloc[:, 1:-1].shape[1] == 0:
                reference_columns = list(self.smartdrift.data_modeldrift.iloc[:, 1:-1].columns)
                metric = "".join(list(self.smartdrift.data_modeldrift.iloc[:, -1:].columns))
                fig = self.smartdrift.plot.generate_modeldrift_data(
                    self.smartdrift.data_modeldrift, metric=metric, reference_columns=reference_columns
                )
                plot_list.append(fig)
            # If you have reference_columns
            else:
                agg_columns = list(self.smartdrift.data_modeldrift.iloc[:, 1:-1].columns)
                for indice, row in self.smartdrift.data_modeldrift[agg_columns].drop_duplicates().iterrows():
                    df = copy.deepcopy(self.smartdrift.data_modeldrift)
                    description = ""
                    for column in agg_columns:
                        df = df[df[column] == row[column]]
                        description += str(row[column]) + ", "

                    reference_columns = list(df.iloc[:, 1:-1].columns)
                    metric = "".join(list(df.iloc[:, -1:].columns))

                    fig = self.smartdrift.plot.generate_modeldrift_data(
                        df, metric=metric, reference_columns=reference_columns
                    )
                    plot_list.append(fig)
                    labels.append(str(description)[:-2])
        return plot_list, labels
