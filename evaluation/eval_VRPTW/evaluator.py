


import os, time
from evaluation.useful_stops import manager_stop_tw

class RoutingEvaluator(object):
    """
    Mother class of all the benchmarks method
    """

    def __init__(self,args,env,prt,min_veh):
        self.args = args
        self.env = env
        self.prt = prt
        self.min_veh =min_veh
        self.name = "mother_eval"

        self.output_file = None

    def _update_filename(self,benchmark_type):
        """
        :return: the name of the output file
        """
         # build task name and datafiles
        task_name = 'vrptw-size-{}-len-{}-results-{}.txt'.format(self.args['test_size'], self.env.n_nodes,benchmark_type)
        fname = os.path.join(self.args['log_dir'],'results', task_name)

        self.output_file = fname

    def _load_manager_stops(self):
        """
        Load all the manager stops required
        :return: a list of manager stops
        """
        list_manager = []

        # file
        data_name = 'vrptw-size-{}-len-{}-test.txt'.format(self.args['test_size'], self.env.n_nodes)
        data_loc = os.path.join(self.args['data_dir'], data_name)

        data_file =open(data_loc, 'r')
        line = data_file.readline()
        while line:
            list_manager.append(manager_stop_tw.ManagerStopTW.from_line(line))
            line = data_file.readline()

        data_file.close()
        return list_manager


    def _check_manager_stop(self,list_manager_stop):
        """
        Check that every stop fit the capacity of the truck, if not then divide it into two parts
        :return: nothing but update the list_manager_stop
        """
        cap = self.env.capacity
        for manager in list_manager_stop:
            manager.check_capacity(cap)


    def perform_routing(self):
        """
        Main function of the class, perform the routing on all the tests sets
        Write result in a new file
        """
        list_manager = self._load_manager_stops()
        self._check_manager_stop(list_manager)

        list_results = []
        time_beg = time.time()
        for i, manager in enumerate(list_manager):
            route= self._route_creator(manager)
            list_results.append(route)

        time_end = time.time() - time_beg
        self.prt.print_out("Finished evalution with " + str(self.name) + " in " + str(time_end))

        # output all the routes
        self._dump_results(list_results)


    def _dump_results(self,list_routes):
        """
        Write the results in the output file
        :param list_routes: a list of sequence of stops including depot if necessary
        """
        data_file =open(self.output_file, 'w')
        for seq in list_routes:
            for stop in seq:
                data_file.write(str(stop.x) + " " + str(stop.y) + " " + str(stop.begin_tw) + " " + str(stop.end_tw) + " ")

            data_file.write("\n")

        data_file.close()


    def _route_creator(self,manager):
        """
        Route the manager, need to be overwritten
        :param manager: a stop manager
        :return:a route object
        """
        raise Exception("Need to be overwritten in children classes")



