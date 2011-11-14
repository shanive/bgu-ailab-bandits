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
#include <string.h>
#include <stdio.h>
#include <GetOpt.h>
#include <vector>
using namespace std;

enum Order{
  RANDOM,  
  ASCENDING,
  DESCENDING
} ;

struct Conf {
  int size;
  vector<string> players;
  int repeat;
  int scorebonus;
  Order order;
  int profile;
} Conf;

static const struct option longOpts[] = {
  {"size", required_argument, 0, 0},
  {


int main(int argc, char *argv[])
{

  GetOpt getopt(argc, argv, "   
