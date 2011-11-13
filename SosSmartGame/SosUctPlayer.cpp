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
using namespace std;
SosUctPlayer::SosUctPlayer(SosGame *game)
		: m_game(game)
{
}

SosUctPlayer::~SosUctPlayer()
{
}

SgMove SosUctPlayer::genMove(SosState *state)
{
  cout<< "In SosUctPlayer::genMove"<< endl;
  SgMove nextMove;
  vector<SgMove> sequence; 
  SgBlackWhite color;
  double maxTime = numeric_limits<double>::max();
  SgUctValue maxGames = static_cast<SgUctValue>(maxTime);
	
  if (state->isWhiteTurn())
    color = SG_WHITE;
  else
    color = SG_BLACK;
	
  SosUctThreadStateFactory factory(this->m_game, color, state);
  SosUctSearch search(&factory, state->size());
  //setings of this->m_search
  cout<< "Player Start searching"<< endl;
  search.Search(maxGames, maxTime, sequence);
  nextMove = sequence.at(0);
  SgDebug()<<"end genMove"<<endl;
  SgDebug()<<"After delete search"<<endl;
  SgDebug().flush();
  return nextMove;
      
}
