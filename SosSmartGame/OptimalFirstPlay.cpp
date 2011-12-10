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
#include "SosRavePlayer.h"
#include "SosUctPlayer.h"
#include "SosUctSearch.h"
#include "math.h"

const int MAX_SIMULATIONS = 2 << 16;
const int ITERATIONS = 1000;

using namespace std;

int isOptimalFirstPlay(SgMove move)
{
  return (static_cast<int>(move) == 9);
} 

double runSimulation(SosPlayer *player)
{
  int count = 0;
  for (int i = 0; i < ITERATIONS; i++){
    SosState *state = new SosState(10);
    SgMove move = player->genMove(state);
    count += isOptimalFirstPlay(move);
    delete state;
  }
  return count;
}
  

int main(int argc, char *argv[])
{
  ofstream outfile;
  outfile.open("optimal.txt", ios::trunc);
  SosGame *game = new SosGame(10);
  //print first row:
  outfile << setw(10) << "Simulations" << setw(10) << "UCT" << setw(10) << "RAVE" <<endl;
  //for every number of simulations, print how many times the agent picked the 
  //optimal play among 1000 trials.
  int simulations = 4;
  while (simulations <= MAX_SIMULATIONS)
    {
      SosUctPlayer *uct = new SosUctPlayer(game, simulations);
      SosRavePlayer *rave = new SosRavePlayer(game, simulations, 16);
      int count = 0;
      outfile << setw(10) << simulations;
      count = runSimulation(uct);
      outfile << setw(10) << count;
      count = runSimulation(rave);
      outfile << setw(10) << count << endl;
      
      delete rave;
      delete uct;
      
      
      simulations *= 2;
    }

    delete game;
}
