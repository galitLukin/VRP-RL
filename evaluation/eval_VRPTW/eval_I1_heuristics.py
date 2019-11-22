
from evaluation.eval_VRPTW import evaluator,I1heuristics


class EvalI1Heuristics(evaluator.RoutingEvaluator):
    """Using google or tools, eval the VRP problem"""

    def __init__(self,args,env):
        super(EvalI1Heuristics,self).__init__(args,env)

        self._update_filename('I1_heuristic')


    def _route_creator(self, manager):
        """
        Route a manager and output the sequence in a specific file
        :param manager: the considered manager
        :return: a sequence of stop
        """
        solver_object = I1heuristics.I1heuristics(manager_stop=manager,
                                                                    env=self.env)
        return solver_object.solve()

