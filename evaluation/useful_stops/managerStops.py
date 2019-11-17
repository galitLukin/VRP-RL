
from evaluation.useful_stops import stop

class managerStops(dict):
    """
    Gather all stop under a dict form
    """

    def __init__(self):
        super(managerStops,self).__init__()
        self.depot = None


    @classmethod
    def from_line(cls,line):
        """
        Create a manager from a line of a file
        :param line: the line of a file
        :return: a managerStops object
        """
        words = line.strip().split(" ")
        nb_stops = int(len(words)/3)
        mana = cls()

        for i in range(0,nb_stops-1):
            new_guid = mana._create_guid()
            mana[new_guid] = stop.Stop(guid=new_guid,
                                        x= words[3*i],
                                       y= words[3*i+1],
                                       demand=words[3*i+2])
        # create depot
        depot =stop.Stop(guid="depot",x=words[-3],
                               y = words[-2],demand=words[-1])
        mana._set_depot(depot)
        return mana


    def _set_depot(self,depot):
        self.depot = depot


    def _create_guid(self):
        guid = "stop_" + str(len(self))
        assert not guid in self
        return guid




