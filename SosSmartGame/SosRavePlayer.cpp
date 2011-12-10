//------------------------------------------------------------
/**
@file SosRavePlayer.cpp
RAVE based SOS player.
*/
//-------------------------------------------------------------
#include <limits>
#include <iostream>
#include <vector>
#include "SosPlayer.h"
#include "SosRavePlayer.h"
#include "SosGame.h"
#include "SosUctSearch.h"
#include "SgUctTree.h"
#include "SgUctValue.h"
#include "SgMove.h"
#include "SgBlackWhite.h"
using namespace std;

SosRavePlayer::SosRavePlayer(SosGame *game, SgUctValue maxGames, int raveWeightFinal)
  :m_game(game), m_maxGames(maxGames), m_raveWeightFinal(raveWeightFinal)
{
}

SosRavePlayer::~SosRavePlayer()
{
}

SgMove SosRavePlayer::genMove(SosState *state)
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
  //rave setings:
  search->SetRave(true); //enable rave
  search->SetRaveWeightFinal(this->m_raveWeightFinal);
  search->SetMoveSelect(SG_UCTMOVESELECT_ESTIMATE);//use the weighted sum of UCT- 
  //and rave value without bias term
  
  search->Search(this->m_maxGames, maxTime, *sequence);
  if (sequence->empty())
    {
      cerr << "Returned Empty Sequence." << endl;
      exit(1);
    }

  nextMove = sequence->at(0);
  
  delete search;
  delete sequence;

  return nextMove;
}
