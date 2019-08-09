import argparse




possible_moves = ['R', # turn right 90degrees
                    'L', #turn left 90
                    'F', #move forward
                    'S' #shoot arrow
                 ]

boardwidth = 0
boardheight = 0




KB = { }
'''
    Knowledge base will be of the form 'pos_x,pos_y' : [stench, breeze, glitter]
'''

class board_object():
    def __init__(self, x, y, name, facing=''):
        self.position = '{0},{1}'.format(x,y)
        self.obj_type = name
        self.facing = facing

def checkForEndCondition(player,thingsOnTheBoard):
    for thing in thingsOnTheBoard:
        if player.position == thing.position:
            if thing.obj_type == 'Gold':
                return 'found the Gold'
            if thing.obj_type == 'Pit':
                return 'found the Pit'
            if thing.obj_type == 'Wumpus':
                return 'were eaten'
        else:
            return ''

def main():
    #import game state
    parser = argparse.ArgumentParser("wumpus")
    parser.add_argument("board", help="The file that contains the default board in an n*n state", type=str)
    args = parser.parse_args()

    gameState = []

    boardObjects = []

    with open(args.board) as gamestate:
        gameState = [line.replace('\n','').split(",") for line in gamestate]

    boardwidth = len(gameState)
    boardheight = len(gameState[0]) 

    #print(gameState)
    gameState.reverse()
    #print(gameState)

    #first we need to populate the entire knowledge base with Socrates definition of true knowledge
    for x in range(0,len(gameState)) :
        for y in range(0,len(gameState[x])):
                if( gameState[x][y] == 'W'):
                    boardObjects.append( board_object(x+1,y+1,'Wumpus') )
                elif(gameState[x][y] == 'P'):
                    boardObjects.append( board_object(x+1,y+1,'Pit') )
                elif(gameState[x][y] == 'G'):
                    boardObjects.append( board_object(x+1,y+1,'Gold') )
                KB.update( {'{0},{1}'.format(x+1,y+1) : [None, None, None] })
    
    #Then we want to add the person to the game, at position 1,1
    playerObject = board_object(1,1,'Player','East')

    endGameVerbage = ''

    while(endGameVerbage == ''):
        add_precept(KB, playerObject, boardObjects)


        endGameVerbage = checkForEndCondition(playerObject,boardObjects)
    

    

    

main()