#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include "state_district_connections.hpp"

using namespace std;

void writeToJSONFile(ofstream& jsonFile, string countryState, vector<string>& names, vector<int>& colours);

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

vector<int> solver(vector<vector<int>>& adj){
    int maxCol=adj.size();
    vector<bool> visited(adj.size(), false);
    vector<vector<int>> forbiddenColours(adj.size());
    vector<int> colours(adj.size(),0);

    bool res = backTrack(maxCol, adj, visited, forbiddenColours, colours);

    if(res == false) {
        cout << "no possible solution\n";
        return vector<int>();//there will always be a solution, so this is unessecary
    }

    return colours;
}

int main(){
    StateDistrictConnections* aus = new StateDistrictConnections("Australia.csv");
    StateDistrictConnections* tel = new StateDistrictConnections("Telangana.csv");

    vector<vector<int>> ausAdj = aus->adjList("Australia.csv");
    vector<vector<int>> telAdj = tel->adjList("Telangana.csv");

    //using a backtracking apporach for this

    //Australia:

    vector<int> ausCol = solver(ausAdj);

    //Telangana:

    vector<int> telCol = solver(telAdj);

    //convert to JSON for communication

    ofstream jsonFile("result.json");
    jsonFile << "{";
    writeToJSONFile(jsonFile, "aus", aus->names, ausCol);
    jsonFile << ",";
    writeToJSONFile(jsonFile, "tel", tel->names, telCol);
    jsonFile << "}";
}

void writeToJSONFile(ofstream& jsonFile, string countryState, vector<string>& names, vector<int>& colours){
    jsonFile << '"' << countryState << '"' << ":{";

    int n = names.size();

    for(int i=0 ; i<n ; ++i){
        jsonFile << '"' << names[i] << '"' << ':' << colours[i];
        if(i<n-1) jsonFile << ',';
    }

    jsonFile << "}";
}
