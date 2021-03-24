import cvxpy

from lib.reach_simulator import MEDIA_COEFFICIENT
from models.fastapi_models import OptimizationSubmitBody


class BudgetOptimizer:

    def __init__(self, request_body: OptimizationSubmitBody):
        self.budget = request_body.budget / 1_000_000
        self.sum_reach = 0
        self.sum_cost = 0
        self.const_list = []
        self.ad_models = []
        if request_body.twitter:
            self.ad_models.append(
                {"media_name": "Twitter",
                 "coefficient": MEDIA_COEFFICIENT["Twitter"]}
            )
        if request_body.youtube:
            self.ad_models.append(
                {"media_name": "Youtube",
                 "coefficient": MEDIA_COEFFICIENT["Youtube"]}
            )
        if request_body.facebook:
            self.ad_models.append(
                {"media_name": "Facebook",
                 "coefficient": MEDIA_COEFFICIENT["Facebook"]}
            )
        self.allocated_budget = {}

    @staticmethod
    def reach_function(cost, coefficient):
        return coefficient * cvxpy.log(cost + 1)

    def object_function(self, costs):
        for cost, ad_model in zip(costs, self.ad_models):
            reach = self.reach_function(cost, ad_model["coefficient"])
            self.sum_reach += reach
        return self.sum_reach

    def constraint_function(self, costs):
        for cost, ad_model in zip(costs, self.ad_models):
            reach = self.reach_function(cost, ad_model["coefficient"])
            self.const_list.append(reach >= 0)
            self.const_list.append(cost >= 0)
            self.sum_cost += cost
        self.const_list.append(self.sum_cost <= self.budget)
        return self.const_list

    def execute(self):
        costs = cvxpy.Variable(len(self.ad_models))
        prob = cvxpy.Problem(cvxpy.Maximize(self.object_function(costs)),
                             self.constraint_function(costs))
        prob.solve(verbose=False)
        for cost, ad_model in zip(costs.value, self.ad_models):
            self.allocated_budget[ad_model["media_name"]] = cost
        return self.allocated_budget, prob.status
