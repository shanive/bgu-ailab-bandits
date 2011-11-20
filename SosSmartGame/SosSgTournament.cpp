/**
   @file SosSgTournament.cpp
   simulate tournament of SOS game with uct based players.
*/

/*
needs to get from command line :
size of game,
names of players,
repetitions,
scorebonus/winloss,
switches order,
profile
*/
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <stdio.h>
#include <getopt.h>
#include <vector>
#include "SosGame.h"
#include "SosPlayer.h"
#include "SosUctPlayer.h"
#include "SosUctSearch.h"

using namespace std;

struct Conf {
  int size;
  vector<string> players;
  int repeat;
  int scorebonus;
  SosGame::ValuesOrder order;
  int profile;
  string outputfilename;

  Conf(): size(10), repeat(1000), scorebonus(0), order(SosGame::RANDOM), 
          profile(0), outputfilename("tour.txt")
  {
  }

  void printer()
  {
    cout << "game size: " << this->size <<
      "\nrepetitions: " << this->repeat <<
      "\nscorebonus: " << this->scorebonus <<
      "\norder: " << this->order <<
      "\nprofile: " << this->profile << 
      "\noutput file: " << this->outputfilename << endl; 
    cout << "players:" << endl;
    vector<string>::iterator it ;
    for (it = this->players.begin(); it != this->players.end(); ++it)
      cout << (*it) << " ";
    cout << endl;
  }
};

void usage(){
  cout << "Usage: /.SosSgTournament.cpp --size <number> --repeat <number> --order <0/1/2> --scorebonus --profile --output file-name player-name [player-name]..." << endl;
  exit(2);
}

/**
   @param classname the name of the player's type
   @return an instance of name type
*/
SosPlayer* createPlayer(string classname, SosGame *game){
  if (classname.compare("random") == 0)
    return new SosRandomPlayer(game);
  if (classname.compare("left") == 0)
    return new SosLeftPlayer(game);
  if (classname.compare("UCT") == 0)
    return new SosUctPlayer(game);
}

vector<SosPlayer*> initPlayers(vector<string> players_names, SosGame* game)
{
  //cout << "In initPlayers" << endl;
  vector<SosPlayer*> players;
  vector<string>::iterator it;
  for (it = players_names.begin(); it != players_names.end(); ++it)
    {
      players.push_back(createPlayer(*it, game));
    }
  return players;
}

void deletePlayers(vector<SosPlayer*> players)
{
  //cout << "In deletePlayers" << endl;
  vector<SosPlayer*>::iterator it;
  for( it = players.begin(); it!=players.end(); ++it)
    {
      delete *it;
    }
}

vector< vector<double> > tournament(Conf *conf)
{

  ofstream outfile;
  outfile.open(conf->outputfilename.c_str(), ios::trunc);
  //cout << "In tournament" << endl;
  vector< vector<double> > scores;

  //simulates tournament.
  SosGame* game = new SosGame(conf->size, conf->scorebonus, conf->order);
  vector<SosPlayer*> players = initPlayers(conf->players, game);

//print first row of results table.
  outfile << setw(10) << " ";
  vector<string>::iterator it;
  for ( it = conf->players.begin(); it != conf->players.end(); it++)
    {
      outfile << setw(10) << *it;
    }
  outfile << endl;

  vector<SosPlayer*>::iterator fiter;
  vector<SosPlayer*>::iterator siter;
  it = conf->players.begin();
  for (fiter = players.begin(); fiter != players.end(); ++fiter)
    {
      //cout << "outer loop" << endl;
      vector<double> playerscores;
      for (siter = players.begin() ; siter != players.end(); ++siter)
        {
          //cout << "inner loop" << endl;
          if (fiter == siter){
            playerscores.push_back(400.0);
            continue;
          }
          //cout << "start repetitions" << endl;
          double average = 0.0;
          for (int i = 0; i < conf->repeat; i++)
            {
              average = average + game->twoPlayersGame(*fiter, *siter);
            }
          //cout << "done repetitions" << endl;
          average = average / conf->repeat;
          playerscores.push_back(average);
          //cout << "end inner loop" << endl;
        }
      outfile << setw(10) << *it;
      vector<double>::iterator pit;
      for (pit = playerscores.begin(); pit != playerscores.end(); pit++)
        {
          outfile << setw(10) << *pit;
        }
      outfile << endl;
      ++it;
      scores.push_back(playerscores);
    }
    deletePlayers(players);
    delete game;
    outfile.close();
    return scores;
}



int main(int argc, char *argv[])
{
  Conf *conf = new Conf();

  const struct option longOpts[] = {
  {"size", required_argument, 0, 's'},
  {"repeat", required_argument, 0, 'r'},
  {"scorebonus", no_argument, &conf->scorebonus, 1},
  {"order", required_argument, 0, 'o'},
  {"profile", no_argument, &conf->profile, 1},
  {"output", required_argument, 0, 'f'},
  {0, 0, 0, 0}
  };

  //defalt values for conf
  int option_index = 0;
  int opt = getopt_long(argc, argv, "", longOpts, &option_index);

  
  // while not detected the end of the options 
  while (opt != -1){
    switch(opt)
      {
      case 0:
        // if this option set a flage do nothing else now 
        break;
      case 's':
        conf->size = atoi(optarg);
        break;
      case 'r':
        conf->repeat = atoi(optarg);
        break;
      case 'o':
        {
        int order = atoi(optarg);
        if ((order == SosGame::RANDOM) || (order == SosGame::ASCENDING) || (order == SosGame::DESCENDING))
          conf->order = static_cast<SosGame::ValuesOrder>(order);
        else 
          usage();
        break;
        }
      case 'f':
        conf->outputfilename = optarg;
        break;
      default:
        usage();
      }
    opt = getopt_long(argc, argv, "", longOpts, &option_index);
  }
  // in the variable optind the index in argv of the next remaining argument
  //unoptional
  if (optind == argc)
    usage();
  else{
    for (int i = optind; i < argc; i++)
           conf->players.push_back(argv[i]);
  }

    conf->printer();
    tournament(conf);

    delete conf;
}     

