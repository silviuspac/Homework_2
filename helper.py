import pandas as pd
from datetime import date 
import matplotlib.pyplot as plt
import seaborn as se
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Circle
import numpy as np

def explicitArea(area):
  return area["name"]

def calculateAge(birthdate): 
    birthdate_arr = birthdate.split("-")
    today = date.today()
    if str(birthdate_arr[1])+str(birthdate_arr[2]) > str(today.month)+str(today.day): 
        return int(int(today.year) - int(birthdate_arr[0]) - 1)
    else: 
        return int(int(today.year) - int(birthdate_arr[0]))

def coachHelper(coach_teams, nation):
  coach_teams = coach_teams.assign(areaName = coach_teams["area"].apply(explicitArea))
  coach_teams_en = coach_teams[coach_teams["areaName"] == nation]
  coach_teams_en = coach_teams_en.assign(age = coach_teams_en["birthDate"].apply(calculateAge))
  coach_teams_en.rename(columns={"name" : "teamName", "officialName" : "officialTeamName"}, inplace = True)
  coach_teams_en.sort_values(by= ["age"], inplace = True)
  coach_teams_en.drop_duplicates(subset = "currentTeamId", keep="first", inplace = True )
  return coach_teams_en

def boxplotCoaches(coach_teams, nation = ''):
  se.set(style = "whitegrid", font_scale = 1.5)
  plt.figure(figsize=(16,4))
  box = se.boxplot(x = coach_teams['age'], color = 'palegoldenrod')
  box = se.stripplot(x = coach_teams['age'], data = coach_teams, jitter = True, marker = 'o', alpha = 1, color = 'tan', 
                  size = 10, linewidth = 1.5)
  title = 'Boxplot for the age of coaches'
  if nation != '':
    title = title + '('+nation+')'
  box.axes.set_title(title, fontsize = 25, fontweight = 'bold')
  box.set_xlabel('Age', fontsize = 20)

def printYoungestCoaches(coach_teams):
  print("The 10 youngest coaches\n")
  yougest_coaches = coach_teams[:10]
  for index, el in yougest_coaches.iterrows():
    print( el["firstName"], el["lastName"], "\nage:", el["age"], "\t team:", el["teamName"],"\n")

def won_duel(tags):
    for el in tags:
        if el['id'] == 1801:
            return 1
    return 0


def airDuelsHelper(events, players, event):
  air_duels = events[events["subEventName"] == event]
  players.drop(columns=["birthArea", "birthDate", "currentNationalTeamId", "foot", "middleName", "passportArea", "role", "weight"], inplace=True)
  air_duels = pd.merge(air_duels, players, left_on="playerId", right_on="wyId")
  air_duels = air_duels.assign(won_duel = air_duels["tags"].apply(won_duel))
  air_duels.drop(columns = ['teamId', 'currentTeamId', 'wyId', 'eventId','eventName', 'eventSec', 'id', 'matchPeriod', 'positions', 'subEventId', 'subEventName', 'tags', 'matchId'], inplace = True)
  return air_duels

def assignHeightCategory(height):
    if height >= 160 and height < 165:
        return '1.60-65m'
    elif height >=165 and height < 170:
        return '1.65-70m'
    elif height >=170 and height < 175:
        return '1.70-75m'  
    elif height >=175 and height < 180:
        return '1.75-80m'
    elif height >=180 and height < 185:
        return '1.80-85m'
    elif height >=185 and height < 190:
        return '1.85-90m'
    elif height >=190 and height < 195:
        return '1.90-95m'
    elif height >=195 and height < 200:
        return '1.95-2m'
    elif height >=200 and height < 205:
        return '2-2.05m'
    else:
        return ''

def mergedAirDuelsPlayers(air_duels_won_by_player, air_duels_by_player):
  air_duels_won_by_player.reset_index(inplace=True)
  air_duels_by_player.reset_index(inplace=True)
  air_duels_by_player.rename(columns={"won_duel" : "tot_duel"}, inplace=True)
  air_duels_by_player_mg = pd.merge(air_duels_by_player, air_duels_won_by_player, left_on="playerId", right_on="playerId")
  air_duels_by_player_mg.sort_values(by="won_duel",ascending=False, inplace=True)
  air_duels_by_player_mg.drop(columns=["shortName_y", "height_y", "firstName_y", "lastName_y"], inplace=True)
  air_duels_by_player_mg.rename(columns={"shortName_x" : "shortName", "firstName_x" : "firstName", "lastName_x" : "lastName", "height_x" : "height"}, inplace=True)
  air_duels_by_player_mg_redux = air_duels_by_player_mg[air_duels_by_player_mg.tot_duel > air_duels_by_player_mg.tot_duel.mean()]
  air_duels_by_player_mg_redux = air_duels_by_player_mg_redux.assign(ratio = air_duels_by_player_mg_redux["won_duel"]/air_duels_by_player_mg_redux["tot_duel"])
  air_duels_by_player_mg_redux = air_duels_by_player_mg_redux.assign(category = air_duels_by_player_mg_redux.height.apply(assignHeightCategory))
  return air_duels_by_player_mg_redux

def airDuelsScatterPlot(air_duels_by_player_mg_redux, nation = ''):
  se.set(style = "ticks", font_scale = 1.5)
  plt.figure(figsize=(16,10))
  sc = plt.scatter(air_duels_by_player_mg_redux.height, air_duels_by_player_mg_redux.ratio, alpha = 1,
                  c = air_duels_by_player_mg_redux.height, s= 150, cmap = 'Spectral', edgecolors = 'black')
  plt.colorbar(sc)
  title = 'Height vs. Ratio scatterplot'
  if nation != '':
        title = 'Height vs. Ratio ('+nation+')'
  plt.title(title, fontsize = 25, fontweight = 'bold')
  plt.xlabel('Height', fontsize = 20)
  plt.ylabel('Ratio', fontsize = 20)

def getStartingPosition(event):
  return list(event)[0]

def getPlayersCordinatesFromEvents(p1, p2, players, spain_matches, spain_events):
  messi = players[players['shortName'].str.contains(p1)]
  ronaldo = players[players['shortName'].str.contains(p2)]
  messi   = messi.drop(columns=["birthArea", "birthDate", "currentNationalTeamId", "firstName", "foot", "height", "lastName", "middleName", "passportArea", "role", "weight"])
  ronaldo = ronaldo.drop(columns=["birthArea", "birthDate", "currentNationalTeamId", "firstName", "foot", "height", "lastName", "middleName", "passportArea", "role", "weight"])
  barca_real_match = spain_matches[spain_matches["dateutc"].str.contains('2018-05-06') & spain_matches["label"].str.contains('Barcelona')]
  barca_real_events = spain_events[spain_events["matchId"].isin(barca_real_match["wyId"].values)]
  ronaldo_events = barca_real_events[barca_real_events["playerId"].isin(ronaldo["wyId"].values)]
  messi_events = barca_real_events[barca_real_events["playerId"].isin(messi["wyId"].values)]
  ronaldo_events = ronaldo_events[ronaldo_events.eventName.isin(["Pass", "Duel", "Free Kick", "Shot"])]
  messi_events = messi_events[messi_events.eventName.isin(["Pass", "Duel", "Free Kick", "Shot"])]
  ronaldo_events = ronaldo_events.drop(columns = ["eventId", "matchId", "matchPeriod", "id", "eventSec", "playerId", "subEventId", "subEventName", "tags", "teamId"])
  messi_events = messi_events.drop(columns=["eventId", "matchId", "matchPeriod", "id", "eventSec", "playerId", "subEventId", "subEventName", "tags", "teamId"])
  ronaldo_events = ronaldo_events.assign(starting_position = ronaldo_events["positions"].apply(getStartingPosition))
  messi_events = messi_events.assign(starting_position = messi_events["positions"].apply(getStartingPosition))
  ronaldo_cordinates = list(ronaldo_events.starting_position.values)
  messi_cordinates = list(messi_events.starting_position.values)
  ronaldo_cordinates_x = [el['x']*1.2 for el in ronaldo_cordinates]
  ronaldo_cordinates_y = [el['y']*0.8 for el in ronaldo_cordinates]
  messi_cordinates_x = [el['x']*1.2 for el in messi_cordinates]
  messi_cordinates_y = [el['y']*0.8 for el in messi_cordinates]
  ronaldo_cordinates_x_y = {'x' : ronaldo_cordinates_x, 'y' : ronaldo_cordinates_y}
  messi_cordinates_x_y = {'x' : messi_cordinates_x, 'y' : messi_cordinates_y}
  return {"ronaldo":ronaldo_cordinates_x_y, "messi" : messi_cordinates_x_y }

def heatMap(cordinates, colorHeat): 
    #Create figure
    fig=plt.figure( facecolor="white") #set up the figures
    fig.set_size_inches(8, 6)
    ax=fig.add_subplot(1,1,1)

    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    Pitch = Rectangle([0,0], width = 120, height = 80, color="black", fill = False)
    #Left, Right Penalty Area and midline
    LeftPenalty = Rectangle([0,22.3], width = 14.6, height = 35.3, fill = False,color="black")
    RightPenalty = Rectangle([105.4,22.3], width = 14.6, height = 35.3, fill = False,color="black")
    midline = ConnectionPatch([60,0], [60,80], "data", "data",color="black")

    #Left, Right 6-yard Box
    LeftSixYard = Rectangle([0,32], width = 4.9, height = 16, fill = False,color="black")
    RightSixYard = Rectangle([115.1,32], width = 4.9, height = 16, fill = False,color="black")


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.1,color="black", fill = False)
    centreSpot = plt.Circle((60,40),0.71,color="black")
    #Penalty spots and Arcs around penalty boxes
    leftPenSpot = plt.Circle((9.7,40),0.71,color="black")
    rightPenSpot = plt.Circle((110.3,40),0.71,color="black")
    leftArc = Arc((9.7,40),height=16.2,width=16.2,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((110.3,40),height=16.2,width=16.2,angle=0,theta1=130,theta2=230,color="black")
    
    element = [ LeftPenalty, RightPenalty, midline, LeftSixYard, RightSixYard, centreCircle, 
               centreSpot, rightPenSpot, leftPenSpot, leftArc, rightArc]
    ax.add_patch(Pitch)
    for i in element:
        ax.add_patch(i)

    se.kdeplot(list(cordinates['x']),list(cordinates['y']), shade=True, n_levels = 750, cmap = colorHeat, shade_lowest=False)
    plt.ylim(-1, 82)
    plt.xlim(-1, 122)
    plt.axis('off')
    #Display Pitch
    plt.show()

def isAccuratePass(tags):
  for el in tags:
      if el['id'] == 1801:
          return 1
  return 0

#Create figure
def plotPassesMap(passes, title): 
  fig=plt.figure()
  fig.set_size_inches(7, 5)
  ax=fig.add_subplot(1,1,1)

  #Pitch Outline & Centre Line
  plt.plot([0,0],[0,90], color="black")
  plt.plot([0,130],[90,90], color="black")
  plt.plot([130,130],[90,0], color="black")
  plt.plot([130,0],[0,0], color="black")
  plt.plot([65,65],[0,90], color="black")

  #Left Penalty Area
  plt.plot([16.5,16.5],[65,25],color="black")
  plt.plot([0,16.5],[65,65],color="black")
  plt.plot([16.5,0],[25,25],color="black")

  #Right Penalty Area
  plt.plot([130,113.5],[65,65],color="black")
  plt.plot([113.5,113.5],[65,25],color="black")
  plt.plot([113.5,130],[25,25],color="black")

  #Left 6-yard Box
  plt.plot([0,5.5],[54,54],color="black")
  plt.plot([5.5,5.5],[54,36],color="black")
  plt.plot([5.5,0.5],[36,36],color="black")

  #Right 6-yard Box
  plt.plot([130,124.5],[54,54],color="black")
  plt.plot([124.5,124.5],[54,36],color="black")
  plt.plot([124.5,130],[36,36],color="black")

  #Prepare Circles
  centreCircle = plt.Circle((65,45),9.15,color="black",fill=False)
  centreSpot = plt.Circle((65,45),0.8,color="black")
  leftPenSpot = plt.Circle((11,45),0.8,color="black")
  rightPenSpot = plt.Circle((119,45),0.8,color="black")

  #Draw Circles
  ax.add_patch(centreCircle)
  ax.add_patch(centreSpot)
  ax.add_patch(leftPenSpot)
  ax.add_patch(rightPenSpot)

  #Prepare Arcs
  leftArc = Arc((11,45),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")
  rightArc = Arc((119,45),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")

  #Draw Arcs
  ax.add_patch(leftArc)
  ax.add_patch(rightArc)

  #Tidy Axes
  plt.axis('off')

  ax.set_title(title)
  
  colorPass = ['red', 'blue']
  for index, ev in passes.iterrows():
      ax.annotate("", xy = (ev['positions'][1]['x'] * 1.3, ev['positions'][1]['y'] * 0.9), xycoords = 'data', xytext = (ev['positions'][0]['x'] * 1.3, ev['positions'][0]['y'] * 0.9), textcoords = 'data',arrowprops=dict(arrowstyle="->",connectionstyle="arc3", color = colorPass[ev['accuratePass']]),)

  #Display Pitch
  plt.show()

def getPlayersPassesFromEvents(p1, p2, italy_events, italy_matches, players):
  jorginho = players[players['shortName'].str.contains(p2)]
  pjanic = players[players['firstName'].str.contains(p1)]
  jorginho = jorginho.drop(columns=["birthArea", "birthDate", "currentNationalTeamId", "firstName", "foot", "height", "lastName", "middleName", "passportArea", "role", "weight"])
  pjanic   = pjanic.drop(columns=["birthArea", "birthDate", "currentNationalTeamId", "firstName", "foot", "height", "lastName", "middleName", "passportArea", "role", "weight"])
  pjanic["shortName"] = "M. Pjanic"
  juve_napoli_match = italy_matches[italy_matches["dateutc"].str.contains('2018-04-22') & italy_matches["label"].str.contains('Napoli')]
  juve_napoli_events = italy_events[italy_events["matchId"].isin(juve_napoli_match["wyId"].values)]
  pjanic_events = juve_napoli_events[juve_napoli_events["playerId"].isin(pjanic["wyId"].values)]
  jorginho_events = juve_napoli_events[juve_napoli_events["playerId"].isin(jorginho["wyId"].values)]
  pjanic_events = pjanic_events[pjanic_events.eventName.isin(["Pass"])]
  jorginho_events = jorginho_events[jorginho_events.eventName.isin(["Pass"])]
  pjanic_events = pjanic_events.drop(columns = ["eventId", "matchId", "matchPeriod", "id", "eventSec", "playerId", "subEventId", "teamId"])
  jorginho_events = jorginho_events.drop(columns=["eventId", "matchId", "matchPeriod", "id", "eventSec", "playerId", "subEventId", "teamId"])
  pjanic_events = pjanic_events.assign(accuratePass = pjanic_events.tags.apply(isAccuratePass))
  jorginho_events = jorginho_events.assign(accuratePass = jorginho_events.tags.apply(isAccuratePass))
  return {"pjanic" : pjanic_events, "jorginho" : jorginho_events}

def getFoulsPerMatch(events_ita, events_spa, events_eng, events_fra, events_ger):
  fouls_ita = events_ita[events_ita["eventName"] == "Foul"]
  fouls_spa = events_spa[events_spa["eventName"] == "Foul"]
  fouls_eng = events_eng[events_eng["eventName"] == "Foul"]
  fouls_fra = events_fra[events_fra["eventName"] == "Foul"]
  fouls_ger = events_ger[events_ger["eventName"] == "Foul"]
  fouls_ita = fouls_ita.drop(columns=["eventId", "eventName", "playerId", "eventSec", "matchPeriod", "positions", "subEventId", "subEventName", "tags", "teamId", "id"])
  fouls_spa = fouls_spa.drop(columns=["eventId", "eventName", "playerId", "eventSec", "matchPeriod", "positions", "subEventId", "subEventName", "tags", "teamId", "id"])
  fouls_eng = fouls_eng.drop(columns=["eventId", "eventName", "playerId", "eventSec", "matchPeriod", "positions", "subEventId", "subEventName", "tags", "teamId", "id"])
  fouls_fra = fouls_fra.drop(columns=["eventId", "eventName", "playerId", "eventSec", "matchPeriod", "positions", "subEventId", "subEventName", "tags", "teamId", "id"])
  fouls_ger = fouls_ger.drop(columns=["eventId", "eventName", "playerId", "eventSec", "matchPeriod", "positions", "subEventId", "subEventName", "tags", "teamId", "id"])
  fouls_ita = fouls_ita.assign(count = 1)
  fouls_spa = fouls_spa.assign(count = 1)
  fouls_eng = fouls_eng.assign(count = 1)
  fouls_fra = fouls_fra.assign(count = 1)
  fouls_ger = fouls_ger.assign(count = 1)
  fouls_ita_for_each_match = fouls_ita.groupby("matchId").sum()
  fouls_spa_for_each_match = fouls_spa.groupby("matchId").sum()
  fouls_eng_for_each_match = fouls_eng.groupby("matchId").sum()
  fouls_fra_for_each_match = fouls_fra.groupby("matchId").sum()
  fouls_ger_for_each_match = fouls_ger.groupby("matchId").sum()
  fouls_ita_per_match = fouls_ita_for_each_match.mean()
  fouls_spa_per_match = fouls_spa_for_each_match.mean()
  fouls_eng_per_match = fouls_eng_for_each_match.mean()
  fouls_fra_per_match = fouls_fra_for_each_match.mean()
  fouls_ger_per_match = fouls_ger_for_each_match.mean()
  return {"ita" :fouls_ita_per_match, "spa" :fouls_spa_per_match, "eng" :fouls_eng_per_match, "fra":fouls_fra_per_match, "ger":fouls_ger_per_match}

def plotFouls(fouls_per_match):
  objects = ("ITA", "SPA", "ENG", "FRA", "GER")
  y_pos = np.arange(len(objects))
  f = plt.subplots(figsize=(7,5))
  fouls_list = [fouls_per_match["ita"].values[0], fouls_per_match["spa"].values[0], fouls_per_match["eng"].values[0], fouls_per_match["fra"].values[0], fouls_per_match["ger"].values[0]]
  plt.bar(y_pos, fouls_list, align='center', alpha=0.8)
  plt.xticks(y_pos, objects)
  plt.ylabel('Fouls')
  plt.title('Leagues')
  plt.show()

def load_games(games):
	pl = pd.read_json(games)
	# Take only columns we need
	df = pd.DataFrame(pl, columns = ['gameweek','label'])
	# Sort data frame by game week
	df.sort_values(by = ['gameweek'], inplace = True)
	df.reset_index(drop = True, inplace = True)
	df = split_label(df)
	return df

def split_label(df):
	df['team1'] = ''
	df['team2'] = ''
	df['points1'] = 0
	df['points2'] = 0
	df.label = df.label.str.replace(r"-\\u00c9", "_")
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

