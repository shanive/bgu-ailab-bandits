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

SosUctThreadState::SosUctThreadState(unsigned int threadId, SgBlackWhite color, SosGame* game, SosState* state)
    : SgUctThreadState(threadId, state->size()),
      m_game(game),
      m_color(color),
      m_gameState(state),
      m_isInPlayout(false)
{
}

SosUctThreadState::~SosUctThreadState()
{
}

SgUctValue SosUctThreadState::Evaluate()
{
	assert(this->m_game->isFinalState(*this->m_gameState));
	return static_cast<SgUctValue>(this->m_game->gameScore(*this->m_gameState));
}

void SosUctThreadState::Execute(SgMove move)
{
    assert(! this->m_isInPlayout);
    this->m_gameState->play(move);
}

void SosUctThreadState::ExecutePlayout(SgMove move)
{
    assert(this->m_isInPlayout);
    this->m_gameState->play(move);
}

bool SosUctThreadState::GenerateAllMoves(SgUctValue count, 
                                  std::vector<SgUctMoveInfo>& moves,
                                  SgUctProvenType& provenType)
{
    moves.clear();
    provenType = SG_NOT_PROVEN;
    // if (this->m_game->isFinalState(*this->m_gameState)){
    //     double scoreBonus = this->m_game->scoreBonus(*this->m_gameState);
    //     if ((( scoreBonus > this->m_game->komi()) && (this->m_color == SG_WHITE)) 
    //     	|| ((scoreBonus < this->m_game->komi()) && (this->m_color == SG_BLACK)))
    //     	provenType = SG_PROVEN_WIN;
    //     else
    //     	provenType = SG_PROVEN_LOSS;	
    //     return true;
    // }
    
    std::vector<SgMove> availableMoves = this->m_gameState->availableMoves();
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
        if (this->m_game->isFinalState(*this->m_gameState))
            return SG_NULLMOVE;

        SgDebug()<<"not end of game"<<endl;
	std::vector<SgMove> availableMoves = this->m_gameState->availableMoves();
       
	int index =  rand() % availableMoves.size();
        assert(index < availableMoves.size());
        SgDebug()<<"move num:"<<index<<endl;
	skipRaveUpdate = false;
	return availableMoves.at(index);
}

void SosUctThreadState::GameStart()
{
    this->m_isInPlayout = false;
}

// void SosUctThreadState::StartPlayout()
// {
//    
// }

void SosUctThreadState::StartPlayouts()
{
    this->m_isInPlayout = true;
    SgDebug()<<"leaving State::StartPlayouts"<<endl;
}

void SosUctThreadState::StartSearch()
{

}

void SosUctThreadState::TakeBackInTree(std::size_t nuMoves)
{
    this->m_gameState->undo(static_cast<int>(nuMoves));
}

void SosUctThreadState::TakeBackPlayout(std::size_t nuMoves)
{
    this->m_gameState->undo(static_cast<int>(nuMoves));
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
			   int moveRange): SgUctSearch(threadStateFactory, moveRange)
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
