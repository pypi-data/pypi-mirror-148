import itertools
import math
from typing import Dict, List, Tuple

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from webviz_config import WebvizConfigTheme

from .._ensemble_well_analysis_data import EnsembleWellAnalysisData


class WellOverviewFigure:
    def __init__(
        self,
        ensembles: List[str],
        data_models: Dict[str, EnsembleWellAnalysisData],
        sumvec: str,
        charttype: str,  # bar, pie, area
        wells_selected: List[str],
        theme: WebvizConfigTheme,
    ) -> None:

        self._ensembles = ensembles
        self._data_models = data_models
        self._sumvec = sumvec
        self._charttype = charttype
        self._wells_selected = wells_selected
        self._colors = theme.plotly_theme["layout"]["colorway"]
        self._rows, self._cols = self.get_subplot_dim()
        spec_type = "scatter" if self._charttype == "area" else self._charttype
        subplot_titles = None if self._charttype == "bar" else self._ensembles

        self._figure = make_subplots(
            rows=self._rows,
            cols=self._cols,
            specs=[
                [{"type": spec_type} for _ in range(self._cols)]
                for _ in range(self._rows)
            ],
            subplot_titles=subplot_titles,
        )

        self._add_traces()

    @property
    def figure(self) -> go.Figure:
        return self._figure

    def get_subplot_dim(self) -> Tuple[int, int]:
        """Returns the subplot dimensions of the currently selected chart type.
        Pie charts have two columns, while the other has one. Area charts have one
        row per ensemble.
        """
        number_of_ens = len(self._ensembles)
        if self._charttype == "bar":
            return 2, 1
        if self._charttype == "pie":
            return max(math.ceil(number_of_ens / 2), 2), 2
        if self._charttype == "area":
            return number_of_ens, 1
        raise ValueError(f"Chart type: {self._charttype} not implemented")

    def _get_ensemble_charttype_data(self, ensemble: str) -> pd.DataFrame:
        """Returns a dataframe with summary data on the form needed for the
        different chart types.
        """
        if self._charttype in ["pie", "bar"]:
            df = self._data_models[ensemble].get_dataframe_melted(self._sumvec)
            df = df[df["WELL"].isin(self._wells_selected)]
            df_mean = df.groupby("WELL").mean().reset_index()
            return df_mean[df_mean[self._sumvec] > 0]

        # else chart type = are
        return (
            self._data_models[ensemble]
            .summary_data.groupby("DATE")
            .mean()
            .reset_index()
        )

    def _add_traces(self) -> None:
        """Add all traces for the currently selected chart type."""
        wells_in_legend = []

        for i, ensemble in enumerate(self._ensembles):
            df = self._get_ensemble_charttype_data(ensemble)

            if self._charttype == "pie":
                self._figure.add_trace(
                    go.Pie(
                        values=df[self._sumvec],
                        labels=df["WELL"],
                        marker_colors=self._colors,
                        textposition="inside",
                        texttemplate="%{label}",
                    ),
                    row=i // 2 + 1,
                    col=i % 2 + 1,
                )

            elif self._charttype == "bar":
                trace = {
                    "x": df["WELL"],
                    "y": df[self._sumvec],
                    "orientation": "v",
                    "type": "bar",
                    "name": ensemble,
                    "marker": {"color": self._colors[i]},
                    "text": df[self._sumvec],
                    "textposition": "none",
                    "texttemplate": "%{text:.2s}",
                }

                self._figure.add_trace(
                    trace,
                    row=1,
                    col=1,
                )
            elif self._charttype == "area":
                color_iterator = itertools.cycle(self._colors)

                for well in self._data_models[ensemble].wells:
                    if well in self._wells_selected:
                        showlegend = False
                        if well not in wells_in_legend:
                            showlegend = True
                            wells_in_legend.append(well)

                        self._figure.add_trace(
                            go.Scatter(
                                x=df["DATE"],
                                y=df[f"{self._sumvec}:{well}"],
                                hoverinfo="text+x+y",
                                hoveron="fills",
                                mode="lines",
                                stackgroup="one",
                                name=well,
                                line=dict(width=0.1, color=next(color_iterator)),
                                legendgroup="Wells",
                                showlegend=showlegend,
                            ),
                            row=i + 1,
                            col=1,
                        )


def format_well_overview_figure(
    figure: go.Figure, charttype: str, settings: List[str], sumvec: str
) -> go.Figure:
    """This function formate the well overview figure. The reason for keeping this
    function outside the figure class is that we can update the figure formatting
    without generating a new WellOverviewFigure object and reloading the data. It can
    be applied directly to the current state of the figure dict if only formatting
    settings are changed. See in the well_overview_callbacks how it is used.
    """

    if charttype == "pie":
        figure.update_traces(
            texttemplate=(
                "%{label}<br>%{value:.2s}"
                if "show_prod_text" in settings
                else "%{label}"
            )
        )

    elif charttype == "bar":
        figure.update_layout(
            barmode=("overlay" if "overlay_bars" in settings else "group")
        )
        figure.update_traces(
            textposition=("auto" if "show_prod_text" in settings else "none")
        )

    # These are valid for all chart types
    figure.update_layout(
        template=("plotly_white" if "white_background" in settings else "plotly")
    )

    phase = {"WOPT": "Oil", "WGPT": "Gas", "WWPT": "Water"}[sumvec]

    figure.update(
        layout_title_text=f"Cumulative Well {phase} Production (Sm3)",
        layout_showlegend=("legend" in settings),
    )
    return figure
