#ifndef STATEDISTRICT_H
#define STATEDISTRICT_H

#include <algorithm>
#include <bits/stdc++.h>
#include <fstream>
#include <ios>
#include <stdexcept>

using namespace std;

class StateDistrictConnections{
    public:
    vector<string> names;
    StateDistrictConnections(string fileName){
        fstream fin;

        fin.open(fileName,ios::in);
        if(!fin.is_open()) throw runtime_error("Failed to open csv file");

        string line, word;

        while(getline(fin, line)){
            stringstream s(line);

            getline(s,word,',');

            this->names.push_back(word);
        }

        fin.close();
    }

    vector<vector<int>> adjList(string fileName){
        vector<vector<int>> ret(this->names.size());//ind->list of inds its connected to

        fstream fin;

        fin.open(fileName,ios::in);
        if(!fin.is_open()) throw runtime_error("Failed to open csv file");

        vector<string> row;
        string line, word;
        int i=0;//keeps track of line number which is also the index of this->names

        while(getline(fin, line)){
            row.clear();
            stringstream s(line);

            bool first=true;
            while(getline(s,word,',')){
                if(first){
                    first=false;
                    continue;
                }
                row.push_back(word);
            }
            for(auto r: row){
                int ind = find(this->names.begin(), this->names.end(), r) - this->names.begin();
                ret[i].push_back(ind);
            }
            i++;
        }

        fin.close();

        return ret;
    }
};

#endif
