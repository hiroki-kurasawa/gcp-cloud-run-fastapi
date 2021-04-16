import numpy as np
from lib.reach_simulator import ReachSimulator


class GraphDataUtils:

    @staticmethod
    def line_graph_data(budget: int, media_name: str):
        x = np.arange(0, 100, 1)
        reach_simulator = ReachSimulator(budget, media_name)
        return [
            dict(
                data=[
                    dict(
                        x=x,
                        y=reach_simulator.unique_reach_function(x)
                    )
                ],
                layout=dict(
                    xaxis=dict(title='コスト(円) × 1,000,000'),
                    yaxis=dict(title='ユニークリーチ × 1,000,000'),
                    margin=dict(t=0),
                    annotations=[
                        dict(
                            x=budget/1_000_000,
                            y=reach_simulator.execute(),
                            text="推定結果"
                        )
                    ]
                )
            )
        ]

    @staticmethod
    def waterfall_graph_data(allocated_budgets):
        measure_list = ["relative" for _ in range(len(allocated_budgets))]
        media_names_list = [name for name in allocated_budgets.keys()]
        return [
            dict(
                data=[
                    dict(
                        type="waterfall",
                        orientation="v",
                        measure=measure_list + ["total"],
                        x=media_names_list + ["TotalBudget"],
                        textposition="outside",
                        text=[
                            str(budget) for budget in allocated_budgets.values()
                        ] + ["Total"],
                        y=[
                            budget for budget in allocated_budgets.values()
                        ] + [0]
                        )
                ],
                layout=dict(
                    margin=dict(t=0),
                    xaxis=dict(title="媒体名", type="category"),
                    yaxis=dict(title="予算(円) × 1,000,000", type="linear"),
                    autosize=True,
                    showlegend=False
                )
            ),
        ]

