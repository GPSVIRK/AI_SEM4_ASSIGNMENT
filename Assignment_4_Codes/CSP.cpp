#include <bits/stdc++.h>
#include "state_district_connections.hpp"

using namespace std;

bool backTrack(int maxCol, vector<vector<int>>& adj, vector<bool>& visited, vector<vector<int>>& forbiddenColours, vector<int>& colours){
    if(find(visited.begin(), visited.end(), false) == visited.end()){
        return true;
    }

    int maxInd = -1;

    for(int i=0 ; i<adj.size() ; ++i){
        if((maxInd==-1 || adj[maxInd].size() < adj[i].size()) && !visited[i]){
            maxInd = i;//choose unvisited node with max neighbors
        }
    }

    int col = 0;//now to choose colour

    while(col <= maxCol){
        col++;
        if(find(forbiddenColours[maxInd].begin(), forbiddenColours[maxInd].end(), col) == forbiddenColours[maxInd].end()){

            //set neighbors forbiddenColours
            for(int i=0 ; i<adj[maxInd].size() ; ++i){
                forbiddenColours[adj[maxInd][i]].push_back(col);
            }
            colours[maxInd] = col;
            visited[maxInd] = true;

            if(backTrack(maxCol, adj, visited, forbiddenColours, colours)){//found winning
                return true;
            }

            //this part basically never happens
            colours[maxInd] = 0;
            visited[maxInd] = false;
            for(int i=0 ; i<adj[maxInd].size() ; ++i){
                forbiddenColours[adj[maxInd][i]].pop_back();
            }
        }
    }

    return false;
}

void solver(StateDistrictConnections* place, vector<vector<int>>& adj){
    int maxCol=adj.size();
    vector<bool> visited(adj.size(), false);
    vector<vector<int>> forbiddenColours(adj.size());
    vector<int> colours(adj.size(),0);
    bool res = backTrack(maxCol, adj, visited, forbiddenColours, colours);

    if(res == false) cout << "no possible solution\n";
    else{
        for(int i=0 ; i<colours.size() ; ++i){
            cout << place->names[i] << " = " << colours[i] << "\n";
        }
    }
}

int main(){
    StateDistrictConnections* aus = new StateDistrictConnections("Australia.csv");
    StateDistrictConnections* tel = new StateDistrictConnections("Telangana.csv");

    vector<vector<int>> ausAdj = aus->adjList("Australia.csv");
    vector<vector<int>> telAdj = tel->adjList("Telangana.csv");

    //using a backtracking apporach for this

    //Australia:

    cout << "Australian States:\n\n";
    solver(aus, ausAdj);

    //Telangana:
    cout << "\nTelangana Districts:\n\n";

    solver(tel, telAdj);
}
/*
* so the way it works is like you maintain a set for each of the things
* this is the domain for each of them and we want to prune this domain when we assign something
* so we assign then we prune for the neighbors
* we choose the thing by which one has the most neighbors at every step
*/
