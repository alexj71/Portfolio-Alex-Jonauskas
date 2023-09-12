#include <iostream>
using namespace std;
  
// Returns true if there is a subset that sums to 0 of at least size k
bool isZeroSum(int set[], int n, int k)
{
    //make table
    int negSum = 0;
    int posSum = 0;
    for(int i = 0; i < n; i++){
        if(set[i] < 0){
            negSum = negSum + set[i];
        }
        else if(set[i] > 0){
            posSum = posSum + set[i];
        }
        else{
            return true;
        }
    }
    int numCols = negSum * (-1) + posSum + 1;
    bool subset[n][numCols];
    int count = 0;
  
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < numCols; j++) {
            if(set[i] == (j+negSum)){
                subset[i][j] = true;
            }
            else if(i == 0){
                subset[i][j] = false;
            }
            else if (i > 0 && (j < set[i] || set[i]*(-1) + j > numCols - 1))
                subset[i][j] = subset[i - 1][j];
            else{
                subset[i][j] = subset[i - 1][j] || subset[i - 1][j - set[i]];
            }
        }
    }

    //Backtrack through table counting solution sizes and getting solution sets.
    //Some of the code below is probably unneccesary because at first I thought we only needed to know the sizes,
    //and not find an actual subset so at first all I did was find the size of the largest subset
    int z = negSum*(-1);

    int numSols = 0;
    for(int i = 0; i < n; i++){
        if(subset[i][z]){
            numSols = numSols + 1;
        }
    }
    int sol[numSols][n];
    for(int i = 0; i < numSols; i++){
        for(int j = 0; j < n; j++){
            sol[i][j] = 0;
        }
    }
    int solRow = 0;
    int solCol = 0;

    int solSizes[n];
    for(int i = 0; i < n; i++)
        solSizes[i] = 0;
    for(int i = 0; i < n; i++){
        solCol = 0;
        if(sol[0][0] != 0)
            solRow = solRow + 1;
        z = negSum*(-1);
        bool temp = subset[i][z];
        int j = i;
        while(temp){
            sol[solRow][solCol] = set[j];
            solCol = solCol + 1;
            solSizes[i] = solSizes[i] + 1;
            if(j > 0 && (z - set[j] >= 0) && (z - set[j] < numCols) && subset[j-1][z-set[j]]){
                z = z - set[j];
                temp = subset[j-1][z];
                //sol[i][j] = set[j];
                j = j - 1;
                
            }
            else if(j>0 && subset[j-1][z]){
                j = j -1;
                solSizes[i] = solSizes[i] - 1;
                sol[solRow][solCol-1] = 0;
            }
            else
                temp = false;
        }
    }

    for(int i = 0; i < numSols; i++){
        if(i != 0){cout << "\n";}
        cout << "Solution: ";
        for(int j = 0; j < n; j++){
            if(sol[i][j] != 0)
                cout << sol[i][j] << " ";
        }
    }
    cout << "\n";
    //Grab largest size
    int maxSol = 0;
    for(int i = 0; i < n; i++){
        //cout << solSizes[i];
        if(solSizes[i]>maxSol)
            maxSol = solSizes[i];
    }
  
      // uncomment this code to print table
     /* 
     for (int i = 0; i < n; i++)
     {
       for (int j = 0; j < numCols; j++)
            cout << "    " << subset[i][j];
       cout <<"\n";
     }
    cout << maxSol; */
    
    return (subset[n-1][negSum*(-1)] && (maxSol >= k));
    
}
  
// Driver code
int main()
{
    //Uncomment any test below, ordered 1 - 7
    //int set[] = {-2,-1,2,3,4}; int k = 3;
    //int set[] = {-12,1,3,5,9,11}; int k = 1;
    //int set[] = {-12, 1,3,5,9,11}; int k = 4;
    //int set[] = {-15,-14,-13,-12,-11,-10,-5,-1,15,20,25,30,35,40,45,60,100,170} ;int k = 4;
    //int set[] = {-200,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28}; int k = 5;
    //int set[] = {-200,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34}; int k = 5;
    int set[] = {-201,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66}; int k = 5;
    /*
    for(int i = 0; i < 100; i++){
        set[i] = (i+1) * 10;
    }*/
    int n = sizeof(set) / sizeof(set[0]);
    if (isZeroSum(set, n, k) == true)
        cout <<"Found a subset of at least size k that sums to zero \n";
    else
        cout <<"No subset of at least size k to sum to zero \n";
    return 0;
}