#ifndef CSVPARSERHPP
#define CSVPARSERHPP

#include <fstream>
#include <ios>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

class IndianCitiesDataset{
public:
    std::unordered_map<std::string, std::vector<std::pair<std::string,int>>> mp;

    IndianCitiesDataset(){
        std::fstream fin;
        fin.open("indian-cities-dataset.csv",std::ios::in);
        if(!fin.is_open())throw std::runtime_error("Failed to open csv file");

        std::vector<std::string> row;
        std::string line, word, temp;
        bool firstLine=true;
        while(getline(fin, line)){
            if(firstLine){firstLine=false;continue;}
            row.clear();

            getline(fin, line);
            std::stringstream s(line);

            while(getline(s, word, ',')){
                row.push_back(word);
            }

            if(row.size() < 3) continue;

            this->mp[row[0]].push_back({row[1],stoi(row[2])});
        }

        fin.close();
    }

    const std::vector<std::pair<std::string,int>>& getOutCityDists(std::string startCity){
        return mp[startCity];
    }
};

#endif

