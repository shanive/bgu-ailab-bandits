//----------------------------------------------------------------------------
/** @file SosUctSearch.cpp */
//----------------------------------------------------------------------------
#include <vector>
#include <string>
#include "SosUctSearch.h"
#include "SgBlackWhite.h"
#include "SgUctTree.h"
#include "SgUctValue.h"
#include "SgUctSearch.h"
#include "assert.h"
#include "SosGame.h"
#include "SgDebug.h"
#include "SgMove.h"
#include <stdlib.h>
#include <sstream>
#include <iostream>

using namespace std;

SosUctThreadState::SosUctThreadState(unsigned int threadId, SgBlackWhite color, SosGame *originGame, SosState *originState)
  : SgUctThreadState(threadId, originState->size()),
    m_evalColor(SG_BLACK),
    m_color(color),
    m_isInPlayout(false),
    m_originGame(originGame), 
    m_originState(originState),
    m_threadState(0)
{

}

SosUctThreadState::~SosUctThreadState()
{
  if (this->m_threadState != 0)
    delete this->m_threadState;
}

SgUctValue SosUctThreadState::Evaluate()
{
	assert(this->m_originGame->isFinalState(*this->m_threadState));
	SgUctValue score = static_cast<SgUctValue>(this->m_originGame->
                                     gameScore(*this->m_threadState));
        if (this->m_evalColor == SG_BLACK)
          return score;
        return (1 - score);
}

void SosUctThreadState::Execute(SgMove move)
{
    assert(! this->m_isInPlayout);
    this->m_threadState->play(move);
}

void SosUctThreadState::ExecutePlayout(SgMove move)
{
    assert(this->m_isInPlayout);
    this->m_threadState->play(move);
}

bool SosUctThreadState::GenerateAllMoves(SgUctValue count, 
                                  std::vector<SgUctMoveInfo>& moves,
                                  SgUctProvenType& provenType)
{
    moves.clear();
    provenType = SG_NOT_PROVEN;
    std::vector<SgMove> availableMoves = this->m_threadState->
      availableMoves();
    if (availableMoves.size()!=0){
      std::vector<SgMove>::const_iterator it;
	
      for (it = availableMoves.begin(); it != availableMoves.end(); ++it){
        moves.push_back(SgUctMoveInfo(*it));
      }
    }
   
    return false; 
}  

SgMove SosUctThreadState::GeneratePlayoutMove(bool& skipRaveUpdate)
{
        if (this->m_originGame->isFinalState(*this->m_threadState))
            return SG_NULLMOVE;

        //SgDebug()<<"not end of game"<<endl;
	std::vector<SgMove> availableMoves = this->m_threadState->
          availableMoves();
       
	int index =  rand() % availableMoves.size();
        assert(index < availableMoves.size());
        //SgDebug()<<"move num:"<<index<<endl;
	skipRaveUpdate = false;
	return availableMoves.at(index);
}

void SosUctThreadState::GameStart()
{
  
}

// void SosUctThreadState::StartPlayout()
// {
//    
// }

void SosUctThreadState::StartPlayouts()
{
    this->m_isInPlayout = true;
    //SgDebug()<<"leaving State::StartPlayouts"<<endl;
}

void SosUctThreadState::StartSearch()
{
  //sync m_threadState with m_originState
  if (this->m_threadState != 0){
    delete this->m_threadState;
    this->m_threadState = 0;
  }
  this->m_threadState = new SosState(*this->m_originState);
}

void SosUctThreadState::TakeBackInTree(std::size_t nuMoves)
{
    this->m_threadState->undo(static_cast<int>(nuMoves));
}

void SosUctThreadState::TakeBackPlayout(std::size_t nuMoves)
{
    this->m_threadState->undo(static_cast<int>(nuMoves));
}

//---------------------------------------------------------------------------------------

SosUctThreadStateFactory::SosUctThreadStateFactory(SosGame *game, 
					SgBlackWhite color, 
					SosState *state)
				: m_game(game),
				  m_color(color), 
				  m_state(state)
{
}

SosUctThreadStateFactory::~SosUctThreadStateFactory()
{

}

SgUctThreadState* SosUctThreadStateFactory:: Create(unsigned int threadId,
                                     		const SgUctSearch& search)
{
	return new SosUctThreadState(threadId, this->m_color,
                                                          this->m_game, 
                                                          this->m_state);

}

//----------------------------------------------------------------------------

SosUctSearch::SosUctSearch(SosUctThreadStateFactory *threadStateFactory, 
			   int moveRange, SgUctValue provenWinRate,
                           SgUctValue provenLossRate)
  : SgUctSearch(threadStateFactory, moveRange, provenWinRate, provenLossRate)
{
  
}

SosUctSearch::~SosUctSearch()
{
}

std::string SosUctSearch::MoveString(SgMove move) const
{
  std::ostringstream outs;
  outs<<static_cast<int>(move);
  return outs.str();
}

SgUctValue SosUctSearch::UnknownEval() const
{
  return 0.0;
}
