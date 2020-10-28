import pandas as pd
import glob

class Schedule():
    def __init__(self, projects, rooms):
        self.rooms = rooms
        self.x_in = projects
        self.num_meetings = self.projects_to_min_meets()
        self.x_in = self.projects_to_tensor()
        
    def projects_to_min_meets(self):
        tensor = {}
        for p in self.x_in:
            tensor[p.project_id] = p.num_meetings
        return tensor
        
    def projects_to_tensor(self):
        tensor = {}
        for p in self.x_in:
            tensor[p.project_id] = p.collaborators
        return tensor


class Project():
    def __init__(self, project_id, num_meetings, leader, participants):
        self.project_id = project_id
        self.num_meetings = num_meetings
        self.collaborators = [leader] + participants
        self.collaborators = self.slots_to_tensor()
        
    def slots_to_tensor(self):
        days = ["mon", "tue", "wed", "thu", "fri"]
        tensor = {}
        for i in range(len(self.collaborators)):
            tensor[i] = {}
            for day in days:
                tensor[i][day] = {}
                for hour in range(8, 17):
                    tensor[i][day][hour] = 0
                    for (d, hs, he) in self.collaborators[i]:
                        if d == day and hour >= hs and hour < he:
                            tensor[i][day][hour] = 1
        return tensor


def read_schedule(path):
    """
    This function reads the csv file of a project's schedule
    and transforms it into a pandas dataframe
    """
    df = pd.read_csv(path)
    col_names = {}
    for i in range(len(df)):
        col_names[i] = df.iloc()[i][0]
    df.drop(columns=[df.columns[0]], inplace=True)
    df.rename(index=col_names, inplace=True)
    
    return df


def get_project(path):
    """
    This function reads a csv file of a project's schedule
    and turns it into an object of the Project class
    """
    df = read_schedule(path)
    
    names = []
    for col in df:
        for elem in df[col]:
            if type(elem) != float:
                for name in elem.split():
                    names.append(name)
    names = list(dict.fromkeys(names))

    leader = {name.split('*')[0]: [] for name in names if "*" in name}
    participants = {name: [] for name in names if "*" not in name}

    for col in df:
        for i, elem in enumerate(df[col]):
            if elem != float:
                # Append leader
                for l in leader:
                    if l in str(elem):
                        start, end = df.index[i].replace('h','').split('-')
                        leader[l].append((col.lower()[:3], int(start), int(end)))
                # Append participants
                for p in participants:
                    if p in str(elem):
                        start, end = df.index[i].replace('h','').split('-')
                        participants[p].append((col.lower()[:3], int(start), int(end)))

    leader = next(iter(leader.values()))
    participants = [participants[key] for key in participants]

    project_id = path.split('/')[-1].split('.')[0]
    num_meets = int(input(f"How many meetings should be held for project {project_id} this week?"))
    
    return Project(project_id, num_meets, leader, participants)

def get_schedule(path, available_rooms):
    """
    This function reads all project's csv files and turns them
    into an object of the class Schedule
    """
    projects = []
    for file in glob.glob(path + "/*.csv"):
        projects.append(get_project(file))
        
    return Schedule(projects, available_rooms)

def pd_centered(df):
    return df.style.set_table_styles([
        {"selector": "th", "props": [("text-align", "center")]},
        {"selector": "td", "props": [("text-align", "center")]}])

def meeting_to_df(r):
	df_dict = {d: {f"{h}h-{h+1}h": "" for h in range(8, 17)} for d in ["mon","tue","wed","thu","fri"]}
	for day in df_dict:
		for hour in range(8, 17):
			for name, d, h, room in r:
				if day == d and hour == int(h):
					df_dict[day][f"{hour}h-{hour+1}h"] += f"| {name} | {room} |"
	return pd.DataFrame(df_dict)