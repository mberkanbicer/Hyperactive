# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

try:
    from progress_io import ProgressIO
except:
    from .progress_io import ProgressIO


color_scale = px.colors.sequential.Jet


class StreamlitBackend:
    def __init__(self, search_ids):
        self.search_ids = search_ids
        self.search_id_dict = {}

        _io_ = ProgressIO("./")

        for search_id in search_ids:
            self.search_id_dict[search_id] = {}

            self.search_id_dict[search_id]["prog_d"] = _io_.load_progress(search_id)
            self.search_id_dict[search_id]["filt_f"] = _io_.load_filter(search_id)

    def get_progress_data(self, search_id):
        progress_data = self.search_id_dict[search_id]["prog_d"]
        if progress_data is None:
            return

        return progress_data[~progress_data.isin([np.nan, np.inf, -np.inf]).any(1)]

    def pyplot(self, progress_data, search_id):
        nth_iter = progress_data["nth_iter"]
        score_best = progress_data["score_best"]
        nth_process = list(progress_data["nth_process"])

        if np.all(nth_process == nth_process[0]):
            fig, ax = plt.subplots()
            plt.plot(nth_iter, score_best)
        else:
            fig, ax = plt.subplots()
            ax.set_xlabel("nth iteration")
            ax.set_ylabel("score")

            for i in np.unique(nth_process):
                nth_iter_p = nth_iter[nth_process == i]
                score_best_p = score_best[nth_process == i]
                plt.plot(nth_iter_p, score_best_p, label=str(i) + ". process")
            plt.legend()

        return fig

    def filter_data(self, df, filter_df):
        prog_data_columns = list(df.columns)

        if len(df) > 1:
            for column in prog_data_columns:
                if column not in list(filter_df["parameter"]):
                    continue

                filter_ = filter_df[filter_df["parameter"] == column]
                lower, upper = (
                    filter_["lower bound"].values[0],
                    filter_["upper bound"].values[0],
                )

                col_data = df[column]

                if lower == "lower":
                    lower = np.min(col_data)
                else:
                    lower = float(lower)

                if upper == "upper":
                    upper = np.max(col_data)
                else:
                    upper = float(upper)

                df = df[(df[column] >= lower) & (df[column] <= upper)]

        return df

    def plotly(self, progress_data, search_id):
        filter_df = self.search_id_dict[search_id]["filt_f"]

        progress_data.drop(
            ["nth_iter", "score_best", "nth_process"], axis=1, inplace=True
        )

        if filter_df is not None:
            progress_data = self.filter_data(progress_data, filter_df)

        # remove score
        prog_data_columns = list(progress_data.columns)
        prog_data_columns.remove("score")

        fig = px.parallel_coordinates(
            progress_data,
            dimensions=prog_data_columns,
            color="score",
            color_continuous_scale=color_scale,
        )
        fig.update_layout(autosize=False, width=1200, height=540)

        return fig

    def create_plots(self, search_id):
        progress_data = self.get_progress_data(search_id)
        if progress_data is None:
            return None, None

        pyplot_fig = self.pyplot(progress_data, search_id)
        plotly_fig = self.plotly(progress_data, search_id)

        return pyplot_fig, plotly_fig
