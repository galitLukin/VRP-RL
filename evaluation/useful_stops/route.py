import numpy as np

class Route(object):
    """
    Class of a route, i.e. a succession of stops with return to the depot
    """

    def __init__(self,sequence_stop,guid = None):
        self.sequence_stops = sequence_stop
        self.guid = guid


    @property
    def nb_stops(self):
        """
        :return: the true number of stops (no depot)
        """
        depot = self.sequence_stops[0]
        nb_true_stop = 0
        for stop in self.sequence_stops:
            if abs(depot.x - stop.x) > 0.0001 or abs(depot.y - stop.y) > 0.0001:
               nb_true_stop +=1

        return nb_true_stop

    @property
    def length(self):
        """
        :return: the total length of a route
        """
        tot_dist = 0

        for i in range(0,self.nb_stops-1):
            prev_stop = self.sequence_stops[i]
            current_stop = self.sequence_stops[i+1]

            tot_dist += np.sqrt((prev_stop.x - current_stop.x)**2 + (prev_stop.y - current_stop.y)**2)

        return tot_dist

    
    @property
    def demand(self):
        """
        :return: the total demand of the route
        """
        return sum(stop.demand for stop in self.sequence_stops)

    @property
    def vehicles(self):
        """
        :return: the number of time the vehicles return to depot
        """
        depot = self.sequence_stops[0]
        nb_visit_depot = 0
        for stop in self.sequence_stops:
            if abs(depot.x - stop.x) <= 0.0001 and abs(depot.y - stop.y) <= 0.0001:
                nb_visit_depot +=1

        assert nb_visit_depot >=2, nb_visit_depot

        return nb_visit_depot -1

    @property
    def first_stop(self):
        return self.sequence_stops[1]

    @property
    def last_stop(self):
        return self.sequence_stops[-2]


    def merge_with_another_route(self,other_route):
        """
        Merge the current route with the other route, in this sense
        :param other_route: a route object
        """
        inital_nb_stop = self.nb_stops + other_route.nb_stops
        new_sequence = self.sequence_stops[0:-1]
        new_sequence.extend(other_route.sequence_stops[1:])

        self.sequence_stops = new_sequence

        assert inital_nb_stop == self.nb_stops


