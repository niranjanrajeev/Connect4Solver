
from FourConnect import * # See the FourConnect.py file
import csv
import copy
import math
from statistics import mean
ROWS = 6
COLOUMNS = 7
global minimax_count
minimax_count = 0 
class GameTreePlayer:
    
    def __init__(self):
        pass
    
    #function to get the list of all possible coloumns
    def possible_squares(currentState):
        pos_sq = []
        for col in range(COLOUMNS):
            if currentState[0][col]==0:
                pos_sq.append(col)
    
        return pos_sq

    #function to get the row the coin will fall in a coloumn
    def row_of_col(currentState, col):
        for r in range(ROWS-1,-1,-1):
            if currentState[r][col] == 0:
                return r
        return -1
    def evaluate_board(currentState):
        return GameTreePlayer.evaluate_board1(currentState)
        #return GameTreePlayer.evaluate_board2(currentState)

    def evaluate_board2(currentState):
        matrix = [[1,2,3,4,3,2,1],
                    [2,3,4,5,4,3,2],
                    [3,4,5,6,5,4,3],
                    [3,4,5,6,5,4,3],
                    [2,3,4,5,4,3,2],
                    [1,2,3,4,3,2,1]]
        sum = 0
        for i in range(ROWS):
            for j in range(COLOUMNS):
                if currentState[i][j]==1:
                    sum -=matrix[i][j]
                elif currentState[i][j]==2:
                    sum +=matrix[i][j]
        return sum
    #evaluation function     
    def evaluate_board1(currentState):
        score = 0
        # horizontal
        for row in range(ROWS):
            for col in range(COLOUMNS-3):
                line = [currentState[row][col+i] for i in range(4)]
                score += GameTreePlayer.evaluate_line(line)
        #vertical
        for row in range(ROWS-3):
            for col in range(COLOUMNS):
                line = [currentState[row+i][col] for i in range(4)]
                score += GameTreePlayer.evaluate_line(line)

        #positive slopediagonal
        for row in range(ROWS - 3):
            for col in range(COLOUMNS - 3):
                line = [currentState[row + i][col + i] for i in range(4)]
                score += GameTreePlayer.evaluate_line(line)

        #negative sloped diagonal
        for row in range(3,ROWS):
            for col in range(COLOUMNS-3):
                line = [currentState[row-i][col+i] for i in range(4)]
                score += GameTreePlayer.evaluate_line(line)
        return score

    #evaluate a line of 4 consecutive squares
    def evaluate_line(line):
        
        player = 2
        opponent = 1
        emptyspace = 0
        score = 0
        #based on the number of pieces on the line
        if line.count(player) == 4:
            score+= 1000
        elif line.count(player) == 3 and line.count(emptyspace) == 1:
            score+= 50
        elif line.count(player) == 2 and line.count(emptyspace) == 2:
            score+= 5
        elif line.count(emptyspace) == 3 and line.count(player) == 1:
            score+= 2
        elif line.count(emptyspace) == 4:
            score+= 1
        
        
        if line.count(opponent) == 4:
            score -= 2000
        elif line.count(opponent) == 3 and line.count(emptyspace) == 1:
            score -= 100
        elif line.count(opponent) == 2 and line.count(emptyspace) == 2:
            score -= 5
        elif line.count(emptyspace) == 3 and line.count(opponent) == 1:
            score -= 2
        
        
        

        return score

  
    def check_if_winning(currentState,player):

        #horizontal
        for row in range(ROWS):
            for col in range(COLOUMNS-3):
                if currentState[row][col]==player and currentState[row][col+1]==player and currentState[row][col+2]==player and currentState[row][col+3]==player:
                    return True
        
        #vertical
        for row in range(ROWS-3):
            for col in range(COLOUMNS):
                if currentState[row][col]==player and currentState[row+1][col]==player and currentState[row+2][col]==player and currentState[row+3][col]==player:
                    return True
        
        #diagonal
        for row in range(ROWS-3):
            for col in range(COLOUMNS-3):
                if currentState[row][col]==player and currentState[row+1][col+1]==player and currentState[row+2][col+2]==player and currentState[row+3][col+3]==player:
                    return True
        
        #other diagonal
        for row in range(ROWS-3):
            for col in range(3,COLOUMNS):
                if currentState[row][col]==player and currentState[row+1][col-1]==player and currentState[row+2][col-2]==player and currentState[row+3][col-3]==player:
                    return True
        return False
        
    def minimax(currentState,depth,player2,alpha,beta):
        global minimax_count
        minimax_count = minimax_count+1
        pos_coloumns = GameTreePlayer.possible_squares(currentState)
        matrix = [[1,2,3,4,3,2,1],
                [2,3,4,5,4,3,2],
                [3,4,5,6,5,4,3],
                [3,4,5,6,5,4,3],
                [2,3,4,5,4,3,2],
                [1,2,3,4,3,2,1]]
        move_order_heauristic_pos_coloumns = []
        for i in range(len(pos_coloumns)):
            r = GameTreePlayer.row_of_col(currentState,pos_coloumns[i])
            move_order_heauristic_pos_coloumns.append((pos_coloumns[i],matrix[r][pos_coloumns[i]]))
        
        move_order_heauristic_pos_coloumns = sorted(move_order_heauristic_pos_coloumns, key=lambda x: x[1], reverse=True)
        pos_coloumns = [item[0] for item in move_order_heauristic_pos_coloumns]

        if len(pos_coloumns)==0:
            if player2 and GameTreePlayer.check_if_winning(currentState,2):
                return (None,1e9)
            elif player2==0 and GameTreePlayer.check_if_winning(currentState,1):
                return (None,-1e9)
            else:
                return (None,0)

        #only one move is left 
        if len(pos_coloumns)==1 and currentState[ROWS-2][pos_coloumns[0]]!=0:
            
            if player2: 
                currentState[ROWS-1][pos_coloumns[0]]=2
            else:
                currentState[ROWS-1][pos_coloumns[0]]=1
            if player2 and GameTreePlayer.check_if_winning(currentState,2):
                return (pos_coloumns[0],1e9)
            elif player2==0 and GameTreePlayer.check_if_winning(currentState,1):
                return (pos_coloumns[0],-1e9)
            else:
                return (pos_coloumns[0],0)

        if depth == 0 :
            return (None,GameTreePlayer.evaluate_board(currentState))


        if player2 : 
            curr_score = -1e9
            best_coloumn = random.choice(pos_coloumns)
            
            for col in pos_coloumns:
            
                row = GameTreePlayer.row_of_col(currentState,col)
                if row==-1:
                    continue
                
                new_board = copy.deepcopy(currentState)
                new_board[row][col] = 2
                is_game_over = GameTreePlayer.check_if_winning(new_board,2)
                if(is_game_over):
                    curr_score = 1e9
                    best_coloumn = col
                    new_score= 0
                else:
                    result = GameTreePlayer.minimax(new_board,depth-1,False,alpha,beta)
                    new_score = result[1]
                
                
                if(new_score > curr_score):
                    curr_score = new_score
                    best_coloumn = col
                alpha = max(alpha,curr_score)
                if alpha>=beta:
                    break
            return (best_coloumn,curr_score)
        else:
            curr_score = 1e9
            best_coloumn = random.choice(pos_coloumns)
            for col in pos_coloumns:
                row = GameTreePlayer.row_of_col(currentState,col)
                if row == -1:
                    continue
                new_board = copy.deepcopy(currentState)
                new_board[row][col] = 1
                
                is_game_over =  GameTreePlayer.check_if_winning(new_board,1)
                if is_game_over:
                    curr_score = -1e9
                    best_coloumn = col
                    new_score = 0
                else:
                    result = GameTreePlayer.minimax(new_board,depth-1,True,alpha,beta)
                    new_score = result[1]
                if(new_score < curr_score):
                    curr_score = new_score
                    best_coloumn = col
                beta = min(beta,curr_score)
                if alpha>=beta:
                    break
            return (best_coloumn,curr_score)

    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        bestAction = GameTreePlayer.minimax(currentState,3,True,-math.inf,math.inf)[0]
 
        #bestAction = input("Take action (0-6) : ")
        return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():

    number = 10
    gametree = 0
    myopic=0
    numberOfMoves = []
    numberOfTimes = []
    for i in range(number):
        global minimax_count
        minimax_count=0
        move = 0
        fourConnect = FourConnect()
        fourConnect.PrintGameState()
        gameTree = GameTreePlayer()
        while move<42: #At most 42 moves are possible
            if move%2 == 0: #Myopic player always moves first
                fourConnect.MyopicPlayerAction()
            else:
                currentState = fourConnect.GetCurrentState()
                gameTreeAction = gameTree.FindBestAction(currentState)
                fourConnect.GameTreePlayerAction(gameTreeAction)
            fourConnect.PrintGameState()
            move += 1
            if fourConnect.winner!=None:
                print("Game Over")
                numberOfTimes.append(minimax_count)
                numberOfMoves.append(move)
                print(minimax_count)
                
                if fourConnect.winner==2:
                    gametree=gametree+1
                    
                elif fourConnect.winner==1:
                    myopic=myopic+1
                break

    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
    """
    
    print("Number of Games      :",number)
    print("Game Tree won        :",gametree)
    print("Myopic won           :",myopic)
    print("Avg moves to win     :",mean(numberOfMoves))
    print("Avg number of times Minimax function was called:",mean(numberOfTimes))


def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2021A7PS3055G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    PlayGame()
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    #RunTestCase()


if __name__=='__main__':
    main()
