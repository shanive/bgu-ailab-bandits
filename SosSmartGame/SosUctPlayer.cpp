//------------------------------------------------------------
/**
@file SosUctPlayer.cpp
UCT based SOS player.
*/
//-------------------------------------------------------------
#include <limits>
#include <iostream>
#include <vector>
#include "SosPlayer.h"
#include "SosUctPlayer.h"
#include "SosGame.h"
#include "SosUctSearch.h"
#include "SgUctTree.h"
#include "SgUctValue.h"
#include "SgMove.h"
#include "SgDebug.h"
#include "SgBlackWhite.h"
using namespace std;

SosUctPlayer::SosUctPlayer(SosGame *game, SgUctValue maxGames)
  : m_game(game), m_maxGames(maxGames)
{
}

SosUctPlayer::~SosUctPlayer()
{
}

SgMove SosUctPlayer::genMove(SosState *state)
{
  SgMove nextMove;
  vector<SgMove> *sequence = new vector<SgMove>(); 
  SgBlackWhite color;
  double maxTime = numeric_limits<double>::max();
  if (state->isWhiteTurn())
    color = SG_WHITE;
  else
    color = SG_BLACK;
	
  SosUctThreadStateFactory *factory = 
    new SosUctThreadStateFactory(this->m_game, color, state);
  SosUctSearch *search = new SosUctSearch(factory, state->size());
  search->Search(this->m_maxGames, maxTime,*sequence);
  if (sequence->empty()){
    SgDebug() << "Empty Sequence" << endl;
    exit(1);
  }
  nextMove = sequence->at(0);
  delete search;
  delete sequence;
  //SosUctSearch deletes factory using smart pointers!
  //do no delete factory!
  return nextMove;
      
}
