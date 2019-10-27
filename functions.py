# RQ2

import pandas as pd

def contingency_table(dataframe, teams):
    for i in range(len(teams)):
        globals()['dic_t%s' % i] = {"win" : [0,0], "lose" : [0,0], "draw" : [0,0]}

    for i in range(len(dataframe)):
        for j in range(len(teams)):        
            if dataframe.team1[i] == teams[j] and dataframe.team2[i] not in teams:
                if dataframe.score1[i] > dataframe.score2[i]:
                    eval('dic_t%s' % j)["win"][0] += 1
                elif dataframe.score1[i] < dataframe.score2[i]:
                    eval('dic_t%s' % j)["lose"][0] += 1
                else:
                    eval('dic_t%s' % j)["draw"][0] += 1
            elif dataframe.team2[i] == teams[j] and dataframe.team1[i] not in teams:
                if dataframe.score1[i] > dataframe.score2[i]:
                    eval('dic_t%s' % j)["win"][1] += 1
                elif dataframe.score1[i] < dataframe.score2[i]:
                    eval('dic_t%s' % j)["lose"][1] += 1
                else:
                    eval('dic_t%s' % j)["draw"][1] += 1

    for k in range(1, 6):
        globals()['cont_table_t%s' % k] = pd.DataFrame(eval('dic_t%s' % int(k-1)))
        eval('cont_table_t%s' % k).index = ['home', 'away']

    cont_table = cont_table_t1 + cont_table_t2 + cont_table_t3 + cont_table_t4 + cont_table_t5

    return(cont_table)

# The above function takes in input the dataframe as modified in RQ1, a list of teams,
# and return a contingency table with the amount of victories, losses and draws ready
# to undergo the chi-squared test provided by scipy's library with chi2_contingency.
