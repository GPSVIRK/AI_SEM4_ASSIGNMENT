#include <bits/stdc++.h>
#include <queue>
#include "csvParser.hpp"

using namespace std;

struct Dist{
    int value=INT_MAX;
};

typedef pair<string,Dist> pqNode;
struct Comparator{
    bool operator()(const pqNode& a, const pqNode& b){
        return a.second.value > b.second.value;
    }
};

void printPath(unordered_map<string, string>& parent, string startCity, string endCity){
    if(parent.find(endCity) == parent.end()){
        cout << "No path found\n";
        return;
    }

    stack<string> stk;
    string curr = endCity;

    while(curr != startCity){
        stk.push(curr);
        curr = parent[curr];
    }

    stk.push(startCity);

    cout << "Path from start to end:\n";

    while(!stk.empty()){
        cout << stk.top() << " --> ";
        stk.pop();
    }

    cout << "DONE\n";
}
int dijkstraCode(){
    IndianCitiesDataset ICD;

    string startCity, endCity;
    cout << "enter start and end cities:\n";

    bool flag=false;
    while(!flag){
        cin >> startCity >> endCity;
        if(ICD.mp.find(startCity) == ICD.mp.end() || ICD.mp.find(endCity) == ICD.mp.end()){
            cout << "Err: enter valid start and end cities:\n";
            continue;
        }

        flag=true;
    }

    priority_queue<pqNode, vector<pqNode>, Comparator> pq;
    unordered_map<string, Dist> distMp;//startCity->string distance=Dist.value; this is distance array
    unordered_map<string, string> parent; //child, parent
    distMp[startCity].value = 0;
    pq.push({startCity, distMp[startCity]});


    while(!pq.empty()){
        pqNode curr = pq.top();
        pq.pop();

        if(curr.first == endCity){
            break;
        }
        if(curr.second.value > distMp[curr.first].value) continue;

        const vector<pair<string, int>> outCityDists = ICD.getOutCityDists(curr.first);

        for(auto i : outCityDists){
            int newDist = i.second + distMp[curr.first].value;
            if(distMp.find(i.first) == distMp.end() || distMp[i.first].value > newDist){//check distances
                distMp[i.first].value = newDist;
                pq.push({i.first, distMp[i.first]});
                parent[i.first] = curr.first;
            }
        }
    }

    printPath(parent, startCity, endCity);

    return distMp[endCity].value;
}

int main(){
    int finalDistance = dijkstraCode();

    cout << "Final distance traveled: " << finalDistance << "\n";
}

