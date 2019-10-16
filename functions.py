# RQ1 / RQ2

def add_teams_scores(df):    # add 4 colums (team1, team2, score1, score2) by splitting label column
	df['team1'] = ''
	df['team2'] = ''
	df['score1'] = 0
	df['score2'] = 0
	for i in range(len(df)):
    df['team1'][i] = ((df['label'][i].replace(',', '-')).split('-'))[0].strip()
    df['team2'][i] = ((df['label'][i].replace(',', '-')).split('-'))[1].strip()
    p1 = ((df['label'][i].replace(',', '-')).split('-'))[2].strip()
    p2 = ((df['label'][i].replace(',', '-')).split('-'))[3].strip()
    if(int(p1) > int(p2)):
        df['score1'][i] +=  3
    elif(int(p1) == int(p2)):
        df['score1'][i] += 1
        df['score2'][i] += 1
    else:
        df['score2'][i] += 3

def team_points(df):    # return a DataFrame with the points of each team sorted by week
	d = {}
	for i in range(len(df)):
		if df.team1[i] not in d:
			d[df.team1[i]] = [int(df.score1[df.gameweek[i]-1]),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    	else:
        	d[df.team1[i]][df.gameweek[i]-1] += df.score1[i] + d[df.team1[i]][df.gameweek[i]-2]
    	if df.team2[i] not in d:
        	d[df.team2[i]] = [int(df.score2[df.gameweek[i]-1]),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    	else:
        	d[df.team2[i]][df.gameweek[i]-1] += df.score2[i] + d[df.team2[i]][df.gameweek[i]-2]
    return DataFrame(d)

def cont_table(df, team):
