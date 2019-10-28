from datetime import date 
import matplotlib.pyplot as plt
  
def calculateAge(birthdate): 
    birthdate_arr = birthdate.split("-")
    today = date.today()
    if str(birthdate_arr[1])+str(birthdate_arr[2]) > str(today.month)+str(today.day): 
        return int(int(today.year) - int(birthdate_arr[0]) - 1)
    else: 
        return int(int(today.year) - int(birthdate_arr[0]))

def won_duel(tags):
    for el in tags:
        if el['id'] == 1801:
            return 1
    return 0

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

def getColorsByHeight(categories):
    res = []
    for category in categories:
        if category >= 160 and category < 165:
            res.append("white")
        elif category >=165 and category < 170:
            res.append("magenta")
        elif category >=170 and category < 175:
            res.append("yellow")
        elif category >=175 and category < 180:
            res.append("green")
        elif category >=180 and category < 185:
            res.append("blue")
        elif category >=185 and category < 190:
            res.append("orange")
        elif category >=190 and category < 195:
            res.append("red")
        elif category >=195 and category < 200:
            res.append("black")
        elif category >=200 and category < 205:
            res.append("gray")
    return res

def getStartingPosition(event):
    return list(event)[0]

## todo move in functions
from matplotlib.patches import Arc
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Circle

#%matplotlib inline
import seaborn as sns 

#Create figure
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

    sns.kdeplot(list(cordinates['x']),list(cordinates['y']), shade=True, n_levels = 750, cmap = colorHeat, shade_lowest=False)
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

## todo move in functions
from matplotlib.patches import Arc
#matplotlib inline
import seaborn as sns 

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