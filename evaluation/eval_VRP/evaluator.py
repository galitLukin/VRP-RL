
import os
from evaluation.useful_stops import managerStops

class RoutingEvaluator(object):
    """
    Mother class of all the benchmarks method
    """

    def __init__(self,args,env):
        self.args = args
        self.env = env

        self.output_file = None

    def _update_filename(self,benchmark_type):
        """
        :return: the name of the output file
        """
         # build task name and datafiles
        task_name = 'vrp-size-{}-len-{}-results-{}.txt'.format(self.args['test_size'], self.env.n_nodes,benchmark_type)
        fname = os.path.join(self.args['log_dir'],'results', task_name)

        self.output_file = fname

    def _load_manager_stops(self):
        """
        Load all the manager stops required
        :return: a list of manager stops
        """
        list_manager = []

        # file
        data_name = 'vrp-size-{}-len-{}-test.txt'.format(self.args['test_size'], self.env.n_nodes)
        data_loc = os.path.join(self.args['data_dir'], data_name)

        data_file =open(data_loc, 'r')
        line = data_file.readline()
        while line:
            list_manager.append(managerStops.managerStops.from_line(line))
            line = data_file.readline()

        data_file.close()
        return list_manager


    def _dump_results(self,list_routes):
        """
        Write the results in the output file
        :param list_routes: a list of sequence of stops including depot if necessary
        """
        data_file =open(self.output_file, 'w')
        for seq in list_routes:
            for stop in seq:
                data_file.write(str(stop.x) + " " + str(stop.y) + " ")

            data_file.write("\n")

        data_file.close()




