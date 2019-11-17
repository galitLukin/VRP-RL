
from evaluation.eval_VRP import evaluator,google_solver

import os

class EvalGoogleOR(evaluator.RoutingEvaluator):
    """Using google or tools, eval the VRP problem"""

    def __init__(self,args,env):
        super(EvalGoogleOR,self).__init__(args,env)

        self._update_filename('or_tools')


    def perform_routing(self):
        """
        Main function of the class, perform the routing on all the tests sets
        Write result in a new file
        """
        list_manager = self._load_manager_stops()
        list_results = []
        for manager in list_manager:
            route= self._route_manger(manager)
            list_results.append(route)

        # output all the routes
        self._dump_results(list_results)


    def _route_manger(self,manager):
        """
        Route a manager and output the sequence in a specific file
        :param manager: the considered manager
        :return: a sequence of stop
        """
        solver_object = google_solver.GoogleSolver(manager_stop=manager,
                                                   env=self.env)
        return solver_object.solve()




