
from evaluation.useful_stops import managerStops, stop_tw

class ManagerStopTW(managerStops.managerStops):
    """
    Gather all stop with tw
    """

    def __init__(self):
        super(ManagerStopTW,self).__init__()

    @classmethod
    def from_line(cls,line):
        """
        Create a manager from a line of a file
        :param line: the line of a file
        :return: a managerStops object
        """
        words = line.strip().split(" ")
        nb_stops = int(len(words)/5)
        mana = cls()

        for i in range(0,nb_stops-1):
            new_guid = mana._create_guid()
            mana[new_guid] = stop_tw.StopTW(guid=new_guid,
                                            x= words[5*i],
                                            y= words[5*i+1],
                                            demand=words[5*i+4],
                                            begin_tw=words[5*i + 2],
                                            end_tw=words[5*i +3])
        # create depot
        depot =stop_tw.StopTW(guid="depot",x=words[-5],
                               y = words[-4],demand=words[-1],begin_tw=words[-3],end_tw=words[-2])
        mana._set_depot(depot)
        return mana


