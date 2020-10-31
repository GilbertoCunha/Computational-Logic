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
	Esta função lê o ficheiro csv de um projeto
	e transforma-o num dataframe de pandas
    """
	
    df = pd.read_csv(path) # Transformar csv em dataframe
    col_names = {}
	# Coletar as horas presentes na primeira coluna do dataframe
    for i in range(len(df)):
        col_names[i] = df.iloc()[i][0]
    df.drop(columns=[df.columns[0]], inplace=True) # Remover a primeira coluna do dataframe
    df.rename(index=col_names, inplace=True) # Colocar as horas coletadas no nome das linhas do dataframe
    
    return df


def get_project(path):
    """
	Esta função lê o ficheiro csv da disponibilidade
	dos colaboradores de um projeto e transforma-o
	num objeto da classe Projeto
    """
	
	# Converter ficheiro num dataframe pandas
    df = read_schedule(path)
    
	# Colecionar os nomes dos colaboradores e líder
    names = []
    for col in df:
        for elem in df[col]:
            if type(elem) != float:
                for name in elem.split():
                    names.append(name)
    names = list(dict.fromkeys(names))

	# Criar dicionários para guardar as slots do líder e colaboradores
    leader = {name.split('*')[0]: [] for name in names if "*" in name}
    participants = {name: [] for name in names if "*" not in name}

	# Popular os dicionários com os dados do dataframe
    for col in df:
        for i, elem in enumerate(df[col]):
            if elem != float:
                # Append do líder
                for l in leader:
                    if l in str(elem):
                        start, end = df.index[i].replace('h','').split('-')
                        leader[l].append((col.lower()[:3], int(start), int(end)))
                # Append dos participantes
                for p in participants:
                    if p in str(elem):
                        start, end = df.index[i].replace('h','').split('-')
                        participants[p].append((col.lower()[:3], int(start), int(end)))

	# Transformar os dicionários em listas
    leader = next(iter(leader.values()))
    participants = [participants[key] for key in participants]

	# Definir o id do projeto e o número de reuniões semanais
    project_id = path.split('/')[-1].split('.')[0]
    num_meets = int(input(f"How many meetings should be held for project {project_id} this week?"))
    
    return Project(project_id, num_meets, leader, participants)

def get_schedule(path, available_rooms):
    """
	Esta função lê todos ficheiros csv na diretoria path
	e converte-os num objeto da classe Schedule
    """
	
    projects = []
	# Colecionar os projetos de cada ficheiro csv numa lista
    for file in glob.glob(path + "/*.csv"):
        projects.append(get_project(file))
        
    return Schedule(projects, available_rooms)

def pd_centered(df):
	"""
	Esta função centra as colunas de um dataframe de pandas
	"""
	return df.style.set_table_styles([
		{"selector": "th", "props": [("text-align", "center")]},
		{"selector": "td", "props": [("text-align", "center")]}])

def meeting_to_df(r):
	"""
	Esta função converte uma lista de tuplos correspondentes às reuniões da semana
	(correspondentes ao output do método get_meetings() da classe Schedule) num dataframe
	de pandas com o horário completo
	"""
	
	# Criar um dicionário com todos os dias e horas do horário
	df_dict = {d: {f"{h}h-{h+1}h": "" for h in range(8, 17)} for d in ["mon","tue","wed","thu","fri"]}
	
	for day in df_dict: # Iterar os dias do dicionário
		for hour in range(8, 17): # Iterar as horas do dicionário
			for name, d, h, room in r: # Iterar os outputs do método get_mettings() 
				if day == d and hour == int(h): # Verificar se o output corresponde ao dia e hora do horário
					df_dict[day][f"{hour}h-{hour+1}h"] += f"| {name} - {room} |" # Adicionar o nome do projeto e a sala
	
	return pd.DataFrame(df_dict)