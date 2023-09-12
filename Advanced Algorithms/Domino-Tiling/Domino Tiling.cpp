#include <iostream>
#include <vector>
#include <set>
#include <ctype.h>
#include <typeinfo>
#include <cctype>
using namespace std;

/* Param: Vector of Strings
   Returns: 
   Description: Given a board, print board will display it to the console*/ 
void printBoard(vector<string> board){
    for(int i = 0; i<board.size(); i++){
        for(int j=0; j<board[i].size(); j++){
            cout << " " << board[i][j] << " ";
        }
        cout << "\n";
    }
}

/* Param: 1 Vector of strings, 1 vector of pairs of ints
   Returns: vector of ints
   Description: Given a board and the tiles left, the function counts how many places each tile left can go and returns a count in each
   index corresponding to each tile*/ 
vector<int> countSols(vector<string> board, vector<pair<int, int>> tiles){
    vector<int> numSols;
    for(int i=0; i<tiles.size(); i++)
        numSols.push_back(0);
    for(int i=0; i<board.size(); i++){
        for(int j=0; j<board[i].size(); j++){
            if(isdigit(board[i][j]) && i+1 != board.size() && j+1 != board[i].size() && isdigit(board[i+1][j]) && isdigit(board[i][j+1])){
                int first = (int)board[i][j] - 48;
                int right = (int)board[i][j+1] - 48;
                int down = (int)board[i+1][j] - 48;
                int left = first;
                int up = first;
                int temp;
                if(left > right){
                    temp = left;
                    left = right;
                    right = temp;
                }
                if(up > down){
                    temp = up;
                    up = down;
                    down = temp;
                }
                //cout << first << " " << right << " " << down << "\n";
                //cout << first*7 + right-((first+1)*(first)/2) << "\n";
                numSols[left*7 + right-((left+1)*(left)/2)] = numSols[left*7 + right-((left+1)*(left)/2)] + 1;
                numSols[up*7 + down-((up+1)*(up)/2)] = numSols[up*7 + down-((up+1)*(up)/2)] + 1;
            }
            else if(isdigit(board[i][j]) && i+1 != board.size() && isdigit(board[i+1][j])){
                int up = (int)board[i][j] - 48;
                int down = (int)board[i+1][j] - 48;
                int temp;
                if(up>down){
                    temp = up;
                    up = down;
                    down = temp;
                }
                numSols[up*7 + down-((up+1)*(up)/2)] = numSols[up*7 + down-((up+1)*(up)/2)] + 1;
            }
            else if(isdigit(board[i][j]) && j+1 != board[i].size() && isdigit(board[i][j+1])){
                int left = (int)board[i][j] - 48;
                int right = (int)board[i][j+1] - 48;
                int temp;
                if(left>right){
                    temp = left;
                    left = right;
                    right = temp;
                }
                numSols[left*7 + right-((left+1)*(left)/2)] = numSols[left*7 + right-((left+1)*(left)/2)] + 1;
            }
        }
    }
    return numSols;
}

/* Param: vector of strings, pair of ints
   Returns: vector of ints
   Description: finds all of the places a tile can be placed on the given board and returns all 4 indices needed for 1 tile placement*/ 
vector<int> findPlace(vector<string> board, pair<int, int> tile){
    vector<int> index;
    //cout << (int)board[6][1];
    //printBoard(board);
    for(int i = 0; i < board.size()-1; i++){
        for(int j = 0; j < board[i].size()-1; j++){
             if((int)board[i][j]-48 == tile.first && (int)board[i+1][j]-48 == tile.second){
                //cout << "hi 2";
                index.push_back(i);
                index.push_back(j);
                index.push_back(i+1);
                index.push_back(j);
            }
            else if((int)board[i][j]-48 == tile.first && (int)board[i][j+1]-48 == tile.second){
                //cout << "hi 4";
                index.push_back(i);
                index.push_back(j);
                index.push_back(i);
                index.push_back(j+1);
            }
            else if((int)board[i][j]-48 == tile.second && (int)board[i+1][j]-48 == tile.first){
                index.push_back(i+1);
                index.push_back(j);
                index.push_back(i);
                index.push_back(j);
            }
            else if((int)board[i][j]-48 == tile.second && (int)board[i][j+1]-48 == tile.first){
                //cout << "hi 4";
                index.push_back(i);
                index.push_back(j+1);
                index.push_back(i);
                index.push_back(j);
            }
        }
    }
    return index;
}

/* Param: 1 vector of strings, 1 vector of ints, 1 vector of pairs of ints
   Returns: 1 vector of strings
   Description: Given the current board, the number of places a tile can go, and the tiles left, mark board marks the tiles that 
   can have to go in a certain spot. This includes any tiles that only have one spot to go or any spot on the board that can only fit 
   a certain tile (after a few tiles are placed, there may be locations on the board where a number is boxed in and there is only one
   choice per which tile can go there)*/ 
vector<string> markBoard(vector<string> board, vector<int> counts, vector<pair<int,int>> tiles){
    //set the next character for tiling the board
    char maxChar = '@';
    for(int i = 0; i<board.size(); i++){
        for(int j = 0; j<board[i].size(); j++){
            if(!isdigit(board[i][j]) && (int)maxChar < (int)board[i][j])
                maxChar = board[i][j];
        }
    }
    maxChar = (char)(maxChar + 1);
    //fill tiles with only one spot
    vector<int> tmp;
    for(int i = 0; i<counts.size(); i++){
        if(counts[i] == 1){ //findplace doesnt check the bottom right corner
            tmp = findPlace(board, tiles[i]);
            board[tmp[0]][tmp[1]] = maxChar;
            board[tmp[2]][tmp[3]] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
    }
    //cout << board[6][3] << " after finding tiles with only one spot\n";
    /*
    for(int j=0; j<board[j].size()-1; j++){
        if(isdigit(board[0][j]) && isdigit(board[0][j+1] && !isdigit(board[1][j]))){
            board[0]
        }
    }*/
    //Check top and bottom rows
    int n = board.size()-1;
    for(int j = 1; j<board[0].size()-1; j++){
        if(isdigit(board[0][j]) && isdigit(board[0][j-1]) && !isdigit(board[0][j+1]) && !isdigit(board[1][j])){
            board[0][j] = maxChar;
            board[0][j-1] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[0][j]) && !isdigit(board[0][j-1]) && isdigit(board[0][j+1]) && !isdigit(board[1][j])){
            board[0][j] = maxChar;
            board[0][j+1] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[0][j]) && !isdigit(board[0][j-1]) && !isdigit(board[0][j+1]) && isdigit(board[1][j])){
            board[0][j] = maxChar;
            board[1][j] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[n][j]) && isdigit(board[n][j-1]) && !isdigit(board[n][j+1]) && !isdigit(board[n-1][j])){
            board[n][j] = maxChar;
            board[n][j-1] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[n][j]) && !isdigit(board[n][j-1]) && isdigit(board[n][j+1]) && !isdigit(board[n-1][j])){
            board[n][j] = maxChar;
            board[n][j+1] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[n][j]) && !isdigit(board[n][j-1]) && !isdigit(board[n][j+1]) && isdigit(board[n-1][j])){
            board[n][j] = maxChar;
            board[n-1][j] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
    }
    //Check left and right column
    n = board[0].size() - 1;
    for(int i = 1; i<board.size() - 1;i++){
        if(isdigit(board[i][0]) && isdigit(board[i+1][0]) && !isdigit(board[i-1][0]) && !isdigit(board[i][1])){
            board[i][0] = maxChar;
            board[i+1][0] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[i][0]) && !isdigit(board[i+1][0]) && isdigit(board[i-1][0]) && !isdigit(board[i][1])){
            board[i][0] = maxChar;
            board[i-1][0] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[i][0]) && !isdigit(board[i+1][0]) && !isdigit(board[i-1][0]) && isdigit(board[i][1])){
            board[i][0] = maxChar;
            board[i][1] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[i][n]) && isdigit(board[i+1][n]) && !isdigit(board[i-1][n]) && !isdigit(board[i][n-1])){
            board[i][n] = maxChar;
            board[i+1][n] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[i][n]) && !isdigit(board[i+1][n]) && isdigit(board[i-1][n]) && !isdigit(board[i][n-1])){
            board[i][n] = maxChar;
            board[i-1][n] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
        else if(isdigit(board[i][n]) && !isdigit(board[i+1][n]) && !isdigit(board[i-1][n]) && isdigit(board[i][n-1])){
            board[i][n] = maxChar;
            board[i][n-1] = maxChar;
            maxChar = (char)(maxChar + 1);
        }
    }
    //Check middle of board
    for(int i = 1; i<board.size() - 1;i++){
        for(int j = 1; j<board[i].size() -1; j++){
            if(isdigit(board[i][j]) && isdigit(board[i-1][j]) && !isdigit(board[i+1][j]) && !isdigit(board[i][j-1]) && !isdigit(board[i][j+1])){
                board[i][j] = maxChar;
                board[i-1][j] = maxChar;
                maxChar = (char)(maxChar+1);
            }
            else if(isdigit(board[i][j]) && !isdigit(board[i-1][j]) && isdigit(board[i+1][j]) && !isdigit(board[i][j-1]) && !isdigit(board[i][j+1])){
                board[i][j] = maxChar;
                board[i+1][j] = maxChar;
                maxChar = (char)(maxChar+1);
            }
            else if(isdigit(board[i][j]) && !isdigit(board[i-1][j]) && !isdigit(board[i+1][j]) && isdigit(board[i][j-1]) && !isdigit(board[i][j+1])){
                board[i][j] = maxChar;
                board[i][j-1] = maxChar;
                maxChar = (char)(maxChar+1);
            }
            else if(isdigit(board[i][j]) && !isdigit(board[i-1][j]) && !isdigit(board[i+1][j]) && !isdigit(board[i][j-1]) && isdigit(board[i][j+1])){
                board[i][j] = maxChar;
                board[i][j+1] = maxChar;
                maxChar = (char)(maxChar+1);
            }
        }
    }
    //cout << board[6][3] << " after finding spots with only one opening next to them\n";
    return board;
}

/* Param: 1 vector of strings
   Returns: 1 int
   Description: Given a board, returns 1 if the board is solved, 0 if not*/ 
int isSolved(vector<string> board){
    int tmp = 1;
    for(int i = 1; i<board.size();i++){
        for(int j =1; j<board[i].size(); j++){
            if(isdigit(board[i][j]))
                tmp = 0;
        }
    }
    return tmp;
}

/* Param: 2 vector of strings, 1 vector of ints
   Returns: 1 vector of ints
   Description: Given the old board and updated board, remove mapped changes the number of solutions for tiles that were mapped to
   0 so that they are no longer considered options for tiling in future iterations*/ 
vector<int> removeMapped(vector<string> board, vector<string> uboard, vector<int> count){
    int left = 0;
    int right = 0;
    int up = 0;
    int down = 0;
    int temp;
    for(int i = 0; i<uboard.size()-1; i++){
        for(int j =0; j<uboard[i].size()-1; j++){
            if(isalpha(uboard[i][j]) && uboard[i][j] == uboard[i][j+1]){
                //cout << "i is " << i << " and j is " << j << " and board is " << board[i][j] << "\n";
                left = (int)board[i][j]-48;
                right = (int)board[i][j+1]-48;
                if(left>right){
                    temp = left;
                    left = right;
                    right = temp;
                }
                //cout << "index is " << left*7 + right-((left+1)*(left)/2) << "\n";
                count[left*7 + right-((left+1)*(left)/2)] = 0;
            }
            else if(isalpha(uboard[i][j]) && uboard[i][j] == uboard[i+1][j]){
                //cout << "hmmm";
                up = (int)board[i][j]-48;
                down = (int)board[i+1][j]-48;
                if(up>down){
                    temp = up;
                    up = down;
                    down = temp;
                }
                count[up*7 + down-((up+1)*(up)/2)] = 0;
            }
        }
    }
    int lr = uboard.size()-1;
    for(int j =0; j<uboard[lr].size()-1; j++){
        if(isalpha(uboard[lr][j]) && uboard[lr][j] == uboard[lr][j+1]){
                //cout << "i is " << i << " and j is " << j << " and board is " << board[i][j] << "\n";
                left = (int)board[lr][j]-48;
                right = (int)board[lr][j+1]-48;
                if(left>right){
                    temp = left;
                    left = right;
                    right = temp;
                }
                //cout << "index is " << left*7 + right-((left+1)*(left)/2) << "\n";
                count[left*7 + right-((left+1)*(left)/2)] = 0;
            }
    }
    return count;
}

/* Param: 2 vectors of strings
   Returns: 1 int
   Description: Compares two boards, returns 0 if they are the same and 1 if they are not*/ 
int compareBoards(vector<string> b1, vector<string> b2){
    for(int i = 0; i<b1.size(); i++){
        for(int j =0; j<b2.size(); j++){
            if(b1[i][j] != b2[i][j]){
                return 1;
            }
        }
    }
    return 0;
}

/* Param: 1 vector of strings, 1 vector of ints
   Returns: vector of vector of strings
   Description: Takes the current board and the number of solutions for each tile. Takes a tile that only has two places and tiles it both
   possible ways and returns the two new*/ 
vector<vector<string>> makeChoice(vector<string> board, vector<int> sols){
    //find a tile to choose
    int i = 0;
    while(i < sols.size()){
        if(sols[i] == 2)
            break;
        i++;
    }
    if(i == 0)
        throw std::invalid_argument("No tile with only two spots for 'makeChoice' to choose");
    int f = 0;
    int s = 0;
    for(int j = 0; j < i; j++){
        if(s < 6){
            s++;
        }
        else{
            f++;
            s = f;
        }
    }
    
    pair<int, int> tile;
    tile.first = f;
    tile.second = s;

    //find first location of that tile
    vector<int> firstLoc = findPlace(board, tile);
    //cout << firstLoc[0] << firstLoc[1] << firstLoc[2] << firstLoc[3] << "\n";
    //cout << "Tile: " << tile.first << "-" << tile.second << "\n";
    char maxChar = '@';
    for(int i = 0; i<board.size(); i++){
        for(int j = 0; j<board[i].size(); j++){
            if(!isdigit(board[i][j]) && (int)maxChar < (int)board[i][j])
                maxChar = board[i][j];
        }
    }
    maxChar = (char)(maxChar + 1);
    //cout << maxChar;
    vector<string> board1 = board;
    board1[firstLoc[0]][firstLoc[1]] = maxChar;
    board1[firstLoc[1]][firstLoc[2]] = maxChar;
    //maxChar = (char)(maxChar + 1);

    //find second location of that tile
    vector<int> secLoc = findPlace(board1,tile);
    //cout << secLoc[0] << secLoc[1] << secLoc[2] << secLoc[3];
    vector<string> board2 = board;
    board2[secLoc[0]][secLoc[1]] = maxChar;
    board2[secLoc[2]][secLoc[3]] = maxChar;
    //printBoard(board1);
    //printBoard(board2);
    vector<vector<string>> boards;
    boards.push_back(board1);
    boards.push_back(board2);
    return boards;
}

//unused, kept for my own reference
vector<string> solve(vector<string> board, vector<string> btmp, vector<pair<int, int>> tiles, vector<int> tmp){
    vector<string> oldBoard = board;
    while(isSolved(btmp) == 0){
        oldBoard = btmp;
        tmp = countSols(btmp, tiles);
        tmp = removeMapped(board, btmp, tmp);
        btmp = markBoard(btmp, tmp, tiles);
        if(compareBoards(oldBoard, btmp) == 0){
            break;
            for(int i = 0; i < tmp.size(); i++){
                cout << tmp[i] << ' ';
            }
            cout << "\n";
            vector<vector<string>> newBoards = makeChoice(btmp, tmp);
            //btmp = solve(board, newBoards[0], tiles, tmp);
            btmp = solve(board, newBoards[1], tiles, tmp);
            //break;
        }
        printBoard(btmp);
    } 
    return btmp;
}

int main(){
    vector<string> board = {"    33    ", "   0316   ","   1506   ", " 22344454 ", "1402505566", "0455261231", " 00244061 ", "   3611   ", "   3526   ", "    23    "};
    //vector<string> board = {"    66    ", "   6033   ", "   5443   ", " 45554434 ","2230001000","3322011455"," 15222111 ","   6263   ","   1666   ","    54    "};
    vector<pair<int, int>> tiles = {{0,0}, {0,1}, {0,2}, {0,3}, {0,4}, {0,5}, {0,6}, {1,1}, {1,2}, {1,3}, {1,4}, {1,5}, {1,6}, {2,2},{2,3}, {2,4}, {2,5}, {2,6}, {3,3}, {3,4}, {3,5}, {3,6}, {4,4}, {4,5}, {4,6}, {5,5}, {5,6}, {6,6}};
    vector<int> tmp = countSols(board, tiles);
    vector<string> btmp = markBoard(board, tmp, tiles);
    vector<string> oldBoard = board;
    //solve(board, btmp, tiles, tmp);
    while(isSolved(btmp) == 0){
        oldBoard = btmp;
        tmp = countSols(btmp, tiles);
        tmp = removeMapped(board, btmp, tmp);
        btmp = markBoard(btmp, tmp, tiles);
        if(compareBoards(oldBoard, btmp) == 0){
            for(int i = 0; i < tmp.size(); i++){
                cout << tmp[i] << ' ';
            }
            cout << "\n";
            tmp = countSols(btmp, tiles);
            tmp = removeMapped(board, btmp, tmp);
            vector<vector<string>> newBoards = makeChoice(btmp, tmp);
            printBoard(newBoards[0]);
            printBoard(newBoards[1]);
            break;
        }
        printBoard(btmp);
    } 
}