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
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <stdio.h>
#include <getopt.h>
#include <vector>
#include "SosGame.h"
#include "SosState.h"
#include "SosPlayer.h"

using namespace std;

struct Conf {
  int size;
  vector<string> players;
  int repeat;
  int scorebonus;
  SosGame::ValuesOrder order;
  int profile;

  Conf(): size(10), repeat(1000), scorebonus(0), order(RANDOM), 
          profile(0)
  {
  }

  void printer()
  {
    cout << "game size: " << this->size <<
      "\nrepetitions: " << this->repeat <<
      "\nscorebonus: " << this->scorebonus <<
      "\norder: " << this->order <<
      "\nprofile: " << this->profile << endl; 
    cout << "players:" << endl;
    vector<string>::iterator it ;
    for (it = this->players.begin(); it != this->players.end(); ++it)
      cout << (*it) << " ";
    cout << endl;
  }
};

void usage(){
  cout << "Usage: /.SosSgTournament.cpp --size <number> --repeat <number> --order <0/1/2> --scorebonus --profile player-name [player-name]..." << endl;
  exit(2);
}

/**
   @param classname the name of the player's type
   @return an instance of name type
*/
SosPlayer* createPlayer(string classname, SosGame *game){
  if (classname.compare("SosRandomPlayer") == 0)
    return new SosRandomPlayer(game);
  if (classname.compare("SosLeftPlayer") == 0)
    return new SosLeftPlayer(game);
  if (classname.compare("SosRightPlayer") == 0)
    return new SosRightPlayer(game);
}

vector<vector<double>> tournament(Conf *conf)
{
  int nuPlayers = conf.players.size();
  vector<vector<double>> scores;

  //simulates tournament.
  SosGame game(conf.size, conf.scorebonus, conf.order);
  
  vector<string>::iterator fiter;
  vector<string>::iterator siter;
  
  for (fiter = conf.players.begin(); fiter != conf.players.end(); ++fiter)
    {
      vector<double> playerscores;
      for (siter = conf.players.begin() ; siter != conf.players.end(); ++siter)
        {
          if (fiter == siter){
            playerscores.push_back(400.0);
            continue;
          }
          SosPlayer* firstplayer = createPlayer(*fiter, game);
          SosPlayer* secondplayer = createPlayer(*siter, game);
          double average = 0.0;
          for (int i = 0; i < conf.repeat; i++)
            {
              average += twoPlayersGame(firstplayer, secondplayer);
            }
          playerscores.push_back(average/conf.repeat);
        }
      scores.push_back(playerscores);
    }
    return scores;
}



int main(int argc, char *argv[])
{
  Conf conf;

  const struct option longOpts[] = {
  {"size", required_argument, 0, 's'},
  {"repeat", required_argument, 0, 'r'},
  {"scorebonus", no_argument, &conf.scorebonus, 1},
  {"order", required_argument, 0, 'o'},
  {"profile", no_argument, &conf.profile, 1},
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
        conf.size = atoi(optarg);
        break;
      case 'r':
        conf.repeat = atoi(optarg);
        break;
      case 'o':
        {
        int order = atoi(optarg);
        if ((order == RANDOM) || (order == ASCENDING) || (order == DESCENDING))
          conf.order = static_cast<SosGame::ValuesOrder>(order);
        else 
          usage();
        break;
        }
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
           conf.players.push_back(argv[i]);
  }

    conf.printer();
}     

