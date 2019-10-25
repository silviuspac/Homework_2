import pandas as pd
import seaborn as sn

# CR1

# function for filtering the events to take only goals
def goal(tags):
    for el in tags:
        if el['id'] == 101 or el['id'] == 102:
            return 1
    return 0

# load the data
def make_goals_DataFrame(events):
	df_events = pd.DataFrame()

	# Read and filter every json file and then store all of them in a single DataFrame
	# Fount out this is faster and lighter than storing them in a DataFrame and then filter ALL
	# Add timeSlot column
	for i in range(len(events)):
	    
	    # read every json file in events and store it in a DataFrame
	    e = pd.read_json(events[i])
	    temp = pd.DataFrame(e)
	    
	    # keep only the columns needed
	    temp = temp[['eventId', 'tags', 'playerId', 'teamId', 'matchPeriod', 'eventSec']]
	    
	    # drop the events without the tag goal or autogol and the event 'save attempt' otherwise we have duplicates of goals
	    temp = temp[(temp['tags'].apply(goal) != 0) & (temp['eventId'] != 9)]
	    
	    # we dont need columns = ['eventId', 'tags'] anymore
	    temp.drop(columns = ['eventId', 'tags'], inplace = True)

	    # Create new column with time slots
	    temp['timeSlot'] = temp.apply(time_slot, axis=1)  # axis = 1 apply time_slot to every single row
	    
	    # append filtered df to a DataFrame
	    df_events = df_events.append(temp, ignore_index = True)

	return df_events

# define time slots
def time_slot(row):
    h = row['matchPeriod']
    m = row['eventSec']/60
    if h == '1H':
        if 0 <= m < 9:
            return 'Slot1'                  # [0, 9)
        elif 9 <= m < 18:
            return 'Slot2'                  # [9, 18)
        elif 18 <= m < 27:
            return 'Slot3'                  # [18, 27)
        elif 27 <= m < 36:
            return 'Slot4'                  # [27, 36)
        elif 36 <= m < 45:
            return 'Slot5'                  # [36, 45)
        else:
            return 'Extra1'                 # 45+
    if h == '2H':
        if 0 <= m < 9:
            return 'Slot6'                  # [45, 54)
        elif 9 <= m < 18:
            return 'Slot7'                  # [54, 63)
        elif 18 <= m < 27:
            return 'Slot8'                  # [63, 72)
        elif 27 <= m < 36:
            return 'Slot9'                  # [72, 81)
        elif 36 <= m < 45:
            return 'Slot10'                 # [81, 90)
        else:
            return 'Extra2'                 # 90+
    return


# Make barplot of absolute frequecies
def teams_goal_barPlot(df_goals):

	sn.set(font_scale = 1.2)
	goals_barPlot = sn.countplot(x=df_goals['timeSlot'], data=df_goals, order = ['Slot1','Slot2','Slot3','Slot4',
    	                                                     'Slot5','Extra1', 'Slot6','Slot7','Slot8','Slot9','Slot10','Extra2'], 
    	                                                     palette = 'inferno')
	goals_barPlot.figure.set_size_inches(15,10)
	goals_barPlot.set_title('Goals frequencies per time slot', fontsize = 25, fontweight = 'bold')
	goals_barPlot.set_xlabel('Timeslots', fontsize = 20)
	goals_barPlot.set_ylabel('Frequencies', fontsize = 20)
	goals_barPlot.set_xticklabels(['0-9 minutes', '9-18 minutes', '18-27 minutes', '27-36 minutes', '36-45 minutes', 
    	'First extra', '45-54 minutes', '54-63 minutes', '63-72 minutes', '72-81 minutes', 
    	'81-90 minutes', 'Second extra'], 
    	fontsize = 14, rotation = 45)
	goals_barPlot.yaxis.grid(False)


# top ten teams Slot10 [81, 90)
def get_teams10(df_goals):
	df_slot10 = df_goals[df_goals['timeSlot'] == 'Slot10']
	df_slot10 = df_slot10.groupby(['teamId']).teamId.agg('count').to_frame('goals')

	# actually 11 teams cause same number of goals
	df_team10 = df_slot10.sort_values(by = 'goals', ascending = False)[:11]

	# load teams for names
	t = pd.read_json('../data/teams.json')
	df_teams = pd.DataFrame(t)
	df_teams = df_teams[['wyId', 'officialName']]
	df_teams.rename(columns = {'wyId' : 'teamId'}, inplace = True)
	df_team10 = pd.merge(df_team10, df_teams, on = 'teamId')
	df_team10 = df_team10[['teamId','goals','officialName']]
	
	return df_team10
	# printare in modo carino i nomi

# players who scored in 8th slot
def get_numPlayer_8slots(df_goals):
	# players able to score in 8 different intervals
	# select player id and timeslot, and then drop duplicates
	df_players_slots = df_goals[['playerId', 'timeSlot']]
	df_players_slots = df_players_slots.drop_duplicates()
	df_players_slots = df_players_slots.groupby('playerId').count()
	df_players_slots = df_players_slots[df_players_slots['timeSlot'] == 8]
	print(len(df_players_slots), "Players scored in 8th slot")
	# 37 players scored in 8 or more different time slots