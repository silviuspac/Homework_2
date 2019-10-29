import pandas as pd
import seaborn as sn
import codecs
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from collections import OrderedDict

#RQ1

def load_PremierLeague_games(premier_games):
	pl = pd.read_json(premier_games)
	# Take only columns we need
	df = pd.DataFrame(pl, columns = ['gameweek','label'])
	# Sort data frame by game week
	df.sort_values(by = ['gameweek'], inplace = True)
	df.reset_index(drop = True, inplace = True)
	df = split_label(df)
	return df


# split label column in 4 columns
def split_label(df):

	# create the 4 columns
	df['team1'] = ''
	df['team2'] = ''
	df['points1'] = 0
	df['points2'] = 0

	# for every row
	for i in range(len(df)):
		# split rows
		temp = df['label'][i]
		l = ((temp.replace(',', '-')).split('-'))
		df['team1'][i] = l[0].strip()
		df['team2'][i] = l[1].strip()
		p1 = l[2].strip()
		p2 = l[3].strip()

		# points earned by the teams
		if(int(p1) > int(p2)):
		    df['points1'][i] +=  3
		elif(int(p1) == int(p2)):
		    df['points1'][i] += 1
		    df['points2'][i] += 1
		else:
		    df['points2'][i] += 3

	return df

def get_points_by_week(df):

	# Create dict with points week by week
	d = {}
	for i in range(len(df)):
	    if df.team1[i] not in d:
	        d[df.team1[i]] = [int(df.points1[i]),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	    else:
	        d[df.team1[i]][df.gameweek[i]-1] += df.points1[i] + d[df.team1[i]][df.gameweek[i]-2]
	    if df.team2[i] not in d:
	        d[df.team2[i]] = [int(df.points2[i]),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	    else:
	        d[df.team2[i]][df.gameweek[i]-1] += df.points2[i] + d[df.team2[i]][df.gameweek[i]-2]
	allsquad = pd.DataFrame(d)
	allsquad.index = np.arange(1, len(allsquad)+1)


	# find longest win/lose streak
	streak = OrderedDict()
	for elem in d:
	    if elem not in streak:
	        streak[elem] = [0, 0]   # [win, lose] streak
	    current_win = 1
	    current_lose = 1
	    max_win = 1
	    max_lose = 1
	    for i in range(1, len(d[elem])):
	        if d[elem][i] == d[elem][i-1] + 3:
	            current_win += 1
	            if current_lose >= max_lose:
	                max_lose = current_lose
	            current_lose = 0
	        elif d[elem][i] == d[elem][i-1]:
	            current_lose += 1
	            if current_win >= max_win:
	                max_win = current_win
	            current_win = 0
	        else:
	            if current_lose >= max_lose:
	                max_lose = current_lose
	            current_lose = 0
	            if current_win >= max_win:
	                max_win = current_win
	            current_win = 0
	        streak[elem][0] = max_win
	        streak[elem][1] = max_lose
	win_ord = OrderedDict(sorted(streak.items(), key=lambda x:x[1][0]))   # sort by win streak
	winner1 = list(win_ord)[-1]
	winner2 = list(win_ord)[-2]
	lose_ord = OrderedDict(sorted(streak.items(), key=lambda x:x[1][1]))   # sort by win streak
	loser1 = list(lose_ord)[-1]
	loser2 = list(lose_ord)[-2]

	plot_points(allsquad, winner1, winner2, loser1, loser2)

def plot_points(df, winner1, winner2, loser1, loser2):
	fig, ax = plt.subplots()
	sn.set(font_scale = 1.5)
	fig.set_size_inches(16, 11)
	ax.xaxis.grid(False)
	ax.set_xticks(list(range(1, 39))) 
	ax.set_xticklabels(list(range(1, 39)), fontsize = 14, horizontalalignment='right')
	ax.axes.set_title("Rankings", fontsize = 30, fontweight="bold")
	ax.set_xlabel("Gameweeks",fontsize = 20)
	ax.set_ylabel("Points",fontsize = 20)
	x = sn.lineplot(data = df, hue = df.columns, ax = ax, legend = 'full', palette = 'cubehelix', style = 'choice', 
	                dashes = False, size = 'coherence', sizes=(.25, 2.5))
	x.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1, fontsize = 15)
	# ax.set_xticks([float(n)+0.5 for n in ax.get_xticks()])
	plt.plot(df[winner1], marker = '', linewidth = 15, alpha = 0.5)
	plt.plot(df[winner2], marker = '', linewidth = 15, alpha=0.5)
	plt.plot(df[loser1], marker = '', linewidth = 15, alpha=0.5)
	plt.plot(df[loser2], marker = '', linewidth = 15, alpha=0.5)
	plt.show(x)

# RQ4

def accurate_pass(tags):
    for el in tags:
        if el['id'] == 1801:
            return 1
    return 0

def load_passes(e, p):
	# Load events in Premier League
	events = pd.read_json(e)
	# Take only columns we need
	df_events = pd.DataFrame(events, columns = ['eventId', 'tags', 'playerId', 'eventName'])
	# Take only pass events
	df_events = df_events.loc[df_events['eventId'] == 8]
	# Add column with accutate(1) and not accurate(0)
	df_events = df_events.assign(comp = df_events["tags"].apply(accurate_pass))

	#load players
	players = pd.read_json(p)
	df_players = pd.DataFrame(players, columns = ['wyId', 'shortName'])

	# merge passes and player to find names
	df_players.rename(columns = {'wyId' : 'playerId'}, inplace = True)
	df_merged = pd.merge(df_events, df_players, on = "playerId")

	return df_merged

def top10_accuratePlayers(data):
	# mean of total passes
	mean = data.groupby(['shortName']).count().mean()[0]

	# remove players who doesn't hame min number of passes (<mean)
	value_counts = data['shortName'].value_counts()
	to_remove = value_counts[value_counts < mean].index
	data = data[~data.shortName.isin(to_remove)]

	# Percenteage of accurate passes (accurate/attempted)
	df_g = data[data['comp'] == 1].groupby(['shortName']).size()/(data.groupby(['shortName']).size())

	# Sort most accurate players
	df_g.sort_values(ascending = False, inplace = True)
	res = df_g.to_dict()
	l = list(res.keys())
	# Print top 10 accurate players
	for i in range(10):
  	  l[i] = [codecs.unicode_escape_decode(l[i])[0], df_g[i]]
  	  print(f"{l[i][0]:<15}{l[i][1]:>10}")


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
def get_teams10(df_goals, teams_file):
	df_slot10 = df_goals[df_goals['timeSlot'] == 'Slot10']
	df_slot10 = df_slot10.groupby(['teamId']).teamId.agg('count').to_frame('goals')

	# actually 11 teams cause same number of goals
	df_team10 = df_slot10.sort_values(by = 'goals', ascending = False)[:11]

	# load teams for names
	t = pd.read_json(teams_file)
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


def contingency_table(dataframe, teams):
    for i in range(len(teams)):
        globals()['dic_t%s' % i] = {"win" : [0,0], "lose" : [0,0], "draw" : [0,0]}

    for i in range(len(dataframe)):
        for j in range(len(teams)):        
            if dataframe.team1[i] == teams[j] and dataframe.team2[i] not in teams:
                if dataframe.points1[i] > dataframe.points2[i]:
                    eval('dic_t%s' % j)["win"][0] += 1
                elif dataframe.points1[i] < dataframe.points2[i]:
                    eval('dic_t%s' % j)["lose"][0] += 1
                else:
                    eval('dic_t%s' % j)["draw"][0] += 1
            elif dataframe.team2[i] == teams[j] and dataframe.team1[i] not in teams:
                if dataframe.points1[i] > dataframe.points2[i]:
                    eval('dic_t%s' % j)["win"][1] += 1
                elif dataframe.points1[i] < dataframe.points2[i]:
                    eval('dic_t%s' % j)["lose"][1] += 1
                else:
                    eval('dic_t%s' % j)["draw"][1] += 1

    for k in range(1, 6):
        globals()['cont_table_t%s' % k] = pd.DataFrame(eval('dic_t%s' % int(k-1)))
        eval('cont_table_t%s' % k).index = ['home', 'away']

    cont_table = cont_table_t1 + cont_table_t2 + cont_table_t3 + cont_table_t4 + cont_table_t5

    return(cont_table)