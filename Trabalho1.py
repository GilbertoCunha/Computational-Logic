class Meeting():
    """
    A class that represents a meeting

    Attributes:
        project (class Project): project associated with the meeting.
        avail_rooms ([class Room]): rooms available for the meeting to take place.
        slots (class Slot): hours and days available for the meeting to take place. (output) of this problem.
        room (class Room): (output) room where the meeting will take place.

    Args:
        project (class Project): (input) project associated with the meeting
        avail_rooms (undefined): (input) rooms available for the meeting to take place
    """
    def __init__(self, project, avail_rooms):
        self.project = project
        self.avail_rooms = avail_rooms

    def get_slots(self):
        """ This method verifies the project's collaborators and available rooms
        determine the time and room for the meeting
        """


class Project():
    """
    Description of Project

    Attributes:
        project_id (int): project identifier
        num_meetings (int): number of project meetings
        participants ([class Slot]): participant collaborators working on the project, does not include leader
        leader (class Slot): leader of the project collaborators
    """
    def __init__(self, project_id, num_meetings, participants, leader):
        self.project_id = project_id
        self.num_meetings = num_meetings
        self.participants = participants
        self.leader = leader


class Slot():
    """
    Description of Slot

    Attributes:
        day (string): weekdays 
        time_interval ((int,int)): start and end hour of availability

    Args:
        day (string): available day of the week
        start (int): start hour of availability
        end (int): end hour of availability
    """
    def __init__(self, day, start, end):
        self.day = day
        self.time_interval = (start, end)
        

class Room():
    """
    Description of Room

    Attributes and Args:
       room_id (int): room identification number
       availability (bool(z3)): defines wether or not a room is available 
    """
    def __init__(self, room_id, availability):
        self.room_id = room_id
        self.availability = availability
