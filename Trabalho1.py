from z3 import *
import time

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
        participants = self.project.participants
        leader = self.project.leader
        days = {"MON":0, "TUE":1, "WED":2, "THU":3, "FRI":4, "SAT":5, "SUN":6}
        start = time.time()

        avail_slots = {}
        D = Int('D') # Day
        T = Int('Time') # Time of day
        N = Int('N') # Number of available participants
        s = Solver()
        for slot in leader:
            s.push() # Save slot
            s.add(D == days[slot.day])
            
            # Iterate slot hours
            avail_slots[slot.day] = []
            for hour in range(slot.time_interval[0], slot.time_interval[1]): s
                s.push() # Guardar hora
                s.add(T == hour)
                
                num_part = 1
                for part in participants: # Iterar participantes
                    s.push() # Guardar participantes
                    part_cond = Or([pslot.slot_to_cond(T, D) for pslot in part])
                    s.add(part_cond)
                    
                    if s.check() == sat:
                        num_part += 1
                        
                    s.pop() # Remover participante
                       
                print(slot.day, hour, num_part >= (len(participants)+1)/2)
                s.add(And(N == num_part, N >= (len(participants)+1)/2))
                if s.check() == sat: # Esta hora está disponível
                    m = s.model()
                    avail_slots[slot.day].append(m[T])
                s.pop() # Remover hora
            s.pop() # Remover slot

        print(f"This took {time.time() - start} seconds")
        print(avail_slots)


class Project():
    """
    Description of Project

    Attributes:
        project_id (int): project identifier
        num_meetings (int): number of project meetings
        participants ([[class Slot]]): participant collaborators working on the project, does not include leader
        leader ([class Slot]): leader of the project collaborators
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

    def slot_to_cond(self, x, d):
        days = {"MON":0, "TUE":1, "WED":2, "THU":3, "FRI":4, "SAT":5, "SUN":6}
        return And([x >= self.time_interval[0], x < self.time_interval[1], d == days[self.day]])
        

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


participants = [
    [Slot("MON", 8, 9), Slot("MON", 10, 13), Slot("TUE", 11, 13), Slot("TUE", 14, 16),  Slot("WED", 8, 12)], 
    [Slot("MON", 8, 9), Slot("TUE", 9, 12), Slot("TUE", 13, 16),  Slot("WED", 9, 11)]
]
leader = [Slot("MON", 8, 9), Slot("TUE", 10, 18), Slot("WED", 9, 13)]
projeto = Project(1, 3, participants, leader)
rooms = [Room(9, True), Room(1, False)]
meeting = Meeting(projeto, rooms)
meeting.get_slots()
