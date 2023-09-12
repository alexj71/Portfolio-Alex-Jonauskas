#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <algorithm>

#include <cassert>
#include <bitset>
#include <fstream>
#include <string>
#include <sstream>
#include <stdio.h>
using namespace std;


bool degreeOne(map<int, set<int>> G){
    map<int, set<int> >::iterator map_it;
    set<int>::iterator set_it;
    vector<int> edges;
    vector<int> vEdges;
    //int validEdges = 0;
    for(map_it = G.begin(); map_it != G.end(); ++map_it){
        for(set_it = map_it->second.begin(); set_it != map_it->second.end(); ++set_it){
            edges.push_back(*set_it);
        }
    }
    for(int i = 0; i<edges.size(); i++){
        for(map_it = G.begin(); map_it != G.end(); ++map_it){
            if(map_it->first == edges[i]){
                vEdges.push_back(edges[i]);
            }
        }
    }
    sort(vEdges.begin(), vEdges.end());
    auto it = std::unique(vEdges.begin(), vEdges.end());
    bool wasUnique = (it == vEdges.end());
    return wasUnique;
}

//if the index of the weights changes this needs to be fixed
int solSum(vector<int> w, vector<int> sols){
    int sum = 0;
    for(int i = 0; i < sols.size(); i++){
        sum = sum + w[sols[i]];
    }
    return sum;
}

map<int, set<int>> removeEdges(map<int, set<int>> G, int index){
    map<int, set<int>> tmp;
    map<int, set<int> >::iterator map_it;
    set<int>::iterator set_it;
    int i = 0;
    for(map_it = G.begin(); map_it != G.end(); ++map_it){
        set<int> tmpSet = map_it->second;
        tmpSet.erase(index);
        tmp.insert(pair<int, set<int>>(map_it->first, tmpSet));
        //map_it->second = map_it->second.erase(index);
        i++;
    }
    return tmp;
}

//may need to also remove edges from other nodes that touch these neighbors
map<int, set<int>> removeNeighbors(map<int, set<int>> G, set<int> node){
    vector<int> indices; //new
    set<int>::iterator set_it; //new
    for (set_it = node.begin(); set_it !=node.end(); ++set_it){//changed from autoit
        if(G.erase(*set_it) > 0)//if is new
            indices.push_back(*set_it); //new
    } 

    for(int i = 0; i < indices.size(); i++){
        G = removeEdges(G, indices[i]);
    }

    return G;
}

void printMap(map<int, set<int>> G){
    map<int, set<int> >::iterator map_it;
    set<int>::iterator set_it;
    for(map_it = G.begin(); map_it != G.end(); ++map_it){
        cout << "Group " << map_it->first << ": ";

        for(set_it = map_it->second.begin(); set_it != map_it->second.end(); ++set_it)
            cout << *set_it << " ";

        cout << endl;
    }
}

bool anyEdges(map<int, set<int>> G){
    map<int, set<int> >::iterator map_it;
    set<int>::iterator set_it;
    vector<int> edges;
    int validEdges = 0;
    for(map_it = G.begin(); map_it != G.end(); ++map_it){
        for(set_it = map_it->second.begin(); set_it != map_it->second.end(); ++set_it){
            edges.push_back(*set_it);
        }
    }
    for(int i = 0; i<edges.size(); i++){
        for(map_it = G.begin(); map_it != G.end(); ++map_it){
            if(map_it->first == edges[i]){
                validEdges++;
            }
        }
    }
    if(validEdges > 0){
        return true;
    }
    else
        return false;
}

bool isIn(int t, vector<int> sol){
    for(int i = 0; i < sol.size(); i++){
        if(t == sol[i])
            return true;
    }
    return false;
}

vector<int> manualSolve(map<int, set<int>> G, vector<int> w){
    map<int, set<int> >::iterator map_it;
    set<int>::iterator set_it;
    vector <int> nodes;
    vector<int> tmp;
    vector<int> sols;
    //int validEdges = 0;
    for(map_it = G.begin(); map_it != G.end(); ++map_it){
        nodes.push_back(map_it->first);
    }
    for(map_it = G.begin(); map_it != G.end(); ++map_it){
        for(set_it = map_it->second.begin(); set_it != map_it->second.end(); ++set_it){
            if(isIn(*set_it, nodes)){
                if(w[map_it->first] > w[*set_it])
                    tmp.push_back(map_it->first);
                else
                    tmp.push_back(*set_it);
            }
        }
    }

    for(int i = 0; i < tmp.size(); i++){
        if(!isIn(tmp[i], sols))
            sols.push_back(tmp[i]);
    }
    return sols;

}

//G is the graph, w is the weights
vector<int> minWVC(map<int, set<int>> G, vector<int> w){
    vector<int> sols;
    if(degreeOne(G))
        return manualSolve(G, w);
    // if(!anyEdges(G))
    //     return sols;
    map<int, set<int> >::iterator map_it;
    map_it = G.begin();
    set<int> removed = map_it->second;
    int index = map_it->first;
    G.erase(map_it->first);

    G = removeEdges(G, index);//new

    vector<int> sols1 = minWVC(G, w);
    vector<int> sols2 = minWVC(removeNeighbors(G, removed), w);
    if(!isIn(index, sols1))
        sols1.push_back(index);
    for (auto it = removed.begin(); it != removed.end(); ++it){
        if(!isIn(*it, sols2))
            sols2.push_back(*it);
    }

    // for(int i = 0; i < sols1.size(); i++)
    //     cout << sols1[i] << ' ';
    // cout << solSum(w, sols1) << '\n';
    // for(int i = 0; i < sols2.size(); i++)
    //     cout << sols2[i] << ' ';
    // cout << solSum(w, sols2) << '\n';

    if(solSum(w, sols1) < solSum(w, sols2)){
        return sols1;
    }
    else{
        return sols2;
    }
}

vector<int> boundedMinWVC(map<int, set<int>> G, vector<int> w, int k){
    vector<int> sols;
    if(degreeOne(G))
        return manualSolve(G, w);
    // if(!anyEdges(G))
    //     return sols;
    if(k < 1){
        vector<int> all = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        return all;
    }
    map<int, set<int> >::iterator map_it;
    map_it = G.begin();
    set<int> removed = map_it->second;
    int index = map_it->first;
    G.erase(map_it->first);

    G = removeEdges(G, index);//new

    vector<int> sols1 = boundedMinWVC(G, w, k-1);
    vector<int> sols2 = boundedMinWVC(removeNeighbors(G, removed), w, k - removed.size());
    if(!isIn(index, sols1))
        sols1.push_back(index);
    for (auto it = removed.begin(); it != removed.end(); ++it){
        if(!isIn(*it, sols2))
            sols2.push_back(*it);
    }

    // for(int i = 0; i < sols1.size(); i++)
    //     cout << sols1[i] << ' ';
    // cout << solSum(w, sols1) << '\n';
    // for(int i = 0; i < sols2.size(); i++)
    //     cout << sols2[i] << ' ';
    // cout << solSum(w, sols2) << '\n';

    if(solSum(w, sols1) < solSum(w, sols2)){
        return sols1;
    }
    else{
        return sols2;
    }
}

// int numInSecNotFirst(vector<int> sols, set<int> numsAbove){
//     int num = 0;
//     int flag = 0;
//     //set<int>::iterator sol_it;
//     set<int>::iterator na_it;
//     for(na_it = numsAbove.begin(); na_it != numsAbove.end(); ++na_it){
//         for(int i = 0; i < sols.size(); i++){
//             if(*na_it == sols[i])
//                 flag = 1;
//         }
//         if(flag == 0)
//             num = num + 1;
//         flag = 0;
//     }
//     return num;
// }

int main(int argc,char *argv[]){
    //cout << argv[1] << argv[2];
    if(argc != 3){
        cerr << "./MWVC g3.dat g3.weight" << endl;
        return 1;
    }

    ifstream graph_file(argv[1]);
    map<int, set<int>> G;
    string line;
    int vertex, neighbor;
    getline(graph_file, line);
    while(!graph_file.eof()){
        getline(graph_file, line);
        istringstream iss(line);
        iss >> vertex;
        while(!iss.eof()){
            iss >> neighbor;
            G[vertex].insert(neighbor);
        }
    }
    graph_file.close();

    vector<int> w;
    int weight;
    ifstream weights_file(argv[2]);
    weights_file >> weight;
    while(!weights_file.eof()){
        weights_file >> weight;
        w.push_back(weight);
    }
    weights_file.close();

    //G3
    // map<int, set<int>> G;
    // G.insert(pair<int, set<int>>(0, {2}));
    // G.insert(pair<int, set<int>>(1, {2}));
    // G.insert(pair<int, set<int>>(2, {0,1}));
    // vector<int> w = {898, 803, 766};

    //G4
    // map<int, set<int>> G;
    // G.insert(pair<int, set<int>>(0, {2, 3}));
    // G.insert(pair<int, set<int>>(1, {2, 3}));
    // G.insert(pair<int, set<int>>(2, {0,1}));
    // G.insert(pair<int, set<int>>(3, {0,1}));
    // vector<int> w = {898, 803, 766, 993};

    //G11
    // map<int, set<int>> G;
    // G.insert(pair<int, set<int>>(0, {3}));
    // G.insert(pair<int, set<int>>(1, {9}));
    // G.insert(pair<int, set<int>>(2, {6, 7, 8}));
    // G.insert(pair<int, set<int>>(3, {0, 4}));
    // G.insert(pair<int, set<int>>(4, {3, 5}));
    // G.insert(pair<int, set<int>>(5, {4, 6, 7}));
    // G.insert(pair<int, set<int>>(6, {2, 5}));
    // G.insert(pair<int, set<int>>(7, {2, 5}));
    // G.insert(pair<int, set<int>>(8, {2, 10}));
    // G.insert(pair<int, set<int>>(9, {1, 10}));
    // G.insert(pair<int, set<int>>(10, {8, 9}));
    // vector<int> w = {898, 803, 766, 993, 2, 522, 221, 381, 730, 970, 185};

    int k = 5;

    vector<int> s = minWVC(G, w);
    //vector<int> s = boundedMinWVC(G, w, k);
    cout << "Min Weight Vertex cover: ";
    for(int i = 0; i < s.size(); i++){
        cout << s[i] << ' ';
    }
    cout << "\n" << "Weight: " << solSum(w, s) << "\n";
    
    return 0;
}
