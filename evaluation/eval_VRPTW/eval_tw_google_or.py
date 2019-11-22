
from evaluation.eval_VRPTW import evaluator,google_tw_solver

class EvalTWGoogleOR(evaluator.RoutingEvaluator):
    """
    Using google or tools, eval the VRPTW porblem
    """

    def __init__(self,args,env):
        super(EvalTWGoogleOR,self).__init__(args,env)

        self._update_filename('or_tools_tw')


    def _route_creator(self, manager):
        """
        Route a manager and output the sequence in a specific file
        :param manager: the considered manager
        :return: a sequence of stop
        """
        solver_object = google_tw_solver.GoogleSolverTW(manager_stop_tw=manager,
                                                       env=self.env)
        return solver_object.solve()
