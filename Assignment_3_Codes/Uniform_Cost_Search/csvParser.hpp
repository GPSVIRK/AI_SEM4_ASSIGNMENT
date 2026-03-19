#ifndef CSVPARSERHPP
#define CSVPARSERHPP

#include <fstream>
#include <ios>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

class IndianCitiesDataset{
public:
    std::unordered_map<std::string, std::vector<std::pair<std::string,int>>> mp;

    IndianCitiesDataset(){
        std::fstream fin;
        fin.open("indian-cities-dataset.csv",std::ios::in);

        std::vector<std::string> row;
        std::string line, word, temp;
        while(fin >> temp){
            row.clear();

            getline(fin, line);
            std::stringstream s(line);

            while(getline(s, word, ',')){
                row.push_back(word);
            }

            this->mp[row[0]].push_back({row[1],stoi(row[2])});
        }

        fin.close();
    }

    std::vector<std::pair<std::string,int>> getOutCityDists(std::string startCity){
        return this->mp[startCity];
    }
};

#endif

