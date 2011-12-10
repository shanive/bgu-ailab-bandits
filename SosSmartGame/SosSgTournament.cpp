/**
   @file SosSgTournament.cpp
   simulate tournament of SOS game with uct based players.
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
#include "SgUctValue.h"
#include "SosUctPlayer.h"
#include "SosUctSearch.h"
#include "math.h"

using namespace std;

struct Conf {
  int size;
  vector<string> players;
  int repeat;
  int scorebonus;
  SosGame::ValuesOrder order;
  int min_sample;
  int max_sample;
  double sample_step;
  int profile;
  string outputfilename;

  Conf(): size(10), repeat(1000), scorebonus(0), order(SosGame::SEMIRANDOM),
          min_sample(10), max_sample(100), sample_step(1.2),
          profile(0), outputfilename("tour.txt")
  {
  }

  void printer()
  {
    cout << "game size: " << this->size <<
      "\nrepetitions: " << this->repeat <<
      "\nscorebonus: " << this->scorebonus <<
      "\norder: " << this->order <<
      "\nminimum samples: " << this->min_sample <<
      "\nmaximum samples: " << this->max_sample <<
      "\nsamples step: " << this->sample_step <<
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
  cout << "Usage: /.tour --size <number> --min <nim-sample> --max <max-sample> --step <sample-step> --repeat <number> --order <0/1/2> --scorebonus --profile --output file-name player-name [player-name]..." << endl;
  exit(2);
}

/**
   @param classname the name of the player's type
   @return an instance of name type
*/
SosPlayer* createPlayer(string classname, SosGame *game, double samples){
  if (classname.compare("random") == 0)
    return new SosRandomPlayer(game);
  if (classname.compare("left") == 0)
    return new SosLeftPlayer(game);
  if (classname.compare("UCT") == 0)
    return new SosUctPlayer(game, static_cast<SgUctValue>(samples));
}

double twoPlayersGame(SosPlayer *firstplayer, SosPlayer *secondplayer, 
                      int repeat, SosGame *game)
{

  //cout << "on twoPlayersGame" << endl;
   double sum = 0.0;

   for (int i = 0; i < repeat; i++)
   {
     sum = sum + game->twoPlayersGame(firstplayer, secondplayer);
   }
   //cout << "done repetitions" << endl;
   return sum;
}

vector<double> simulation(Conf *conf, double samples)
{
  int playersNum = conf->players.size();
  vector<double> scores;
  //initiate scores:
  for(int i = 0; i < playersNum;i++)
    {
      scores.push_back(0.0);
    }

  //initiate game.
  SosGame* game = new SosGame(conf->size, conf->scorebonus, conf->order);
  //simulate games
  for (int first = 0; first < playersNum; first++)
    {
      for (int second = 0; second < playersNum; second++)
        {
          //cout << "inner loop" << endl;
          if (first == second){
            continue;
          }
          SosPlayer *firstPlayer = createPlayer(conf->players.at(first),
                                                game, samples);
          SosPlayer *secondPlayer = createPlayer(conf->players.at(second),
                                                 game, samples);
          double firstPlayerScore = twoPlayersGame(firstPlayer, secondPlayer, 
                                        conf->repeat, game);
          //cout << "Before updating scores" << endl;
          scores.at(first) += (firstPlayerScore / conf->repeat);
          scores.at(second) += 1 - (firstPlayerScore / conf->repeat);
          //cout << "Updating scores" << endl;
          delete secondPlayer;
          delete firstPlayer;
        }
    }
  delete game;
  return scores;
}

void runTournament(Conf *conf)
{
  ofstream outfile;
  outfile.open(conf->outputfilename.c_str(), ios::trunc);
  //print first row of results table.
  outfile << setw(10) <<"Samples";
  vector<string>::iterator it;
  for ( it = conf->players.begin(); it != conf->players.end(); it++)
    {
      outfile << setw(10) << *it;
    }
  outfile << endl;
  int gamesPerPlayer = (conf->players.size()-1)*2;
  //every player play against n-1 other players twice: as first and as second
  double samples = conf->min_sample;
  while (samples <= conf->max_sample)
    {
      vector<double> scores = simulation(conf, samples);
      //print scores of this round:
      outfile << setw(10) << round(samples);
      vector<double>::iterator it = scores.begin();
      for(; it != scores.end(); it++)
        {
          outfile << setw(10) << (*it)/gamesPerPlayer;
        }
      outfile << endl;
      samples = samples*conf->sample_step;
    }
}




int main(int argc, char *argv[])
{
  Conf *conf = new Conf();

  const struct option longOpts[] = {
  {"size", required_argument, 0, 's'},
  {"repeat", required_argument, 0, 'r'},
  {"scorebonus", no_argument, &conf->scorebonus, 1},
  {"order", required_argument, 0, 'o'},
  {"min", required_argument, 0, 'n'},
  {"max", required_argument, 0, 'm'},
  {"step", required_argument, 0, 'p'},
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
        if ((order == SosGame::RANDOM) || (order == SosGame::ASCENDING) 
            || (order == SosGame::DESCENDING))
          conf->order = static_cast<SosGame::ValuesOrder>(order);
        else 
          usage();
        break;
        }
      case 'n':
        conf->min_sample = atoi(optarg);
        break;
      case 'm':
        conf->max_sample = atoi(optarg);
        break;
      case 'p':
        conf->sample_step = atof(optarg);
        break;
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
    runTournament(conf);

    delete conf;
}     

