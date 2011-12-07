#include "../SosGame.h"
#include "../SosUctSearch.h"
#include "SgMove.h"
#include "SgUctTree.h"
#include "SgBlackWhite.h"
#include "SosUctThreadStateTest.h"
#include <vector>

CPPUNIT_TEST_SUITE_REGISTRATION (SosUctThreadStateTest);

void SosUctThreadStateTest::setUp(void)
{
  this->game = new SosGame(4, false, SosGame::ASCENDING);
  this->state = new SosState(4);
  this->threadState = new SosUctThreadState(0, 
                              SG_BLACK, this->game, this->state); 
}

void SosUctThreadStateTest::tearDown(void)
{
  delete this->state;
  delete this->game;
  delete this->threadState;
}

void SosUctThreadStateTest::StartSearchTest(void)
{
  this->state->play(static_cast<SgMove>(2));
  this->threadState->StartSearch();
  std::vector<SgUctMoveInfo> moves;
  SgUctProvenType type;
  this->threadState->GenerateAllMoves(static_cast<SgUctValue>(0), moves, type);
  CPPUNIT_ASSERT(moves.size() == 3);
}

void SosUctThreadStateTest::EvaluateTest(void)
{
  this->threadState->GameStart();
  this->threadState->Execute(static_cast<SgMove>(2));//black's move
  this->threadState->Execute(static_cast<SgMove>(1));//white's move
  this->threadState->Execute(static_cast<SgMove>(3));//black's move
  this->threadState->Execute(static_cast<SgMove>(0));//white's move
  CPPUNIT_ASSERT(static_cast<double>(this->threadState->Evaluate()) 
                 == 1);
}

void SosUctThreadStateTest::ExecuteTest(void)
{
  this->threadState->GameStart();
  this->threadState->Execute(static_cast<SgMove>(2));
  std::vector<SgMove> blacks = this->state->blackMoves();
  //shoult not change origin state
  CPPUNIT_ASSERT(blacks.size() == 0);
  SgUctProvenType type;
  std::vector<SgUctMoveInfo> moves;
  this->threadState->GenerateAllMoves(0, moves, type);
  CPPUNIT_ASSERT(moves.size() == 3);
}
 
void SosUctThreadStateTest::ExecutePlayoutTest(void)
{
  this->threadState->GameStart();
  this->threadState->StartPlayouts();
  this->threadState->ExecutePlayout(static_cast<SgMove>(2));
  std::vector<SgMove> blacks = this->state->blackMoves();
  //shoult not change origin state
  CPPUNIT_ASSERT(blacks.size() == 0);
  SgUctProvenType type;
  std::vector<SgUctMoveInfo> moves;
  this->threadState->GenerateAllMoves(0, moves, type);
  CPPUNIT_ASSERT(moves.size() == 3);
}
 
void SosUctThreadStateTest::GenerateAllMovesTest(void)
{
  this->threadState->GameStart();
  std::vector<SgUctMoveInfo> moves;
  SgUctProvenType provenType;
  CPPUNIT_ASSERT(!this->threadState->GenerateAllMoves(0, moves, provenType));
  CPPUNIT_ASSERT(moves.size() == 4);
  CPPUNIT_ASSERT(provenType == SG_NOT_PROVEN);
  this->threadState->Execute(static_cast<SgMove>(2));//white's move
  this->threadState->Execute(static_cast<SgMove>(1));//black's move
  this->threadState->Execute(static_cast<SgMove>(3));//white's move
  this->threadState->Execute(static_cast<SgMove>(0));//black's move
  CPPUNIT_ASSERT(!this->threadState->GenerateAllMoves(0, moves, provenType));
  CPPUNIT_ASSERT(moves.size() == 0);
  CPPUNIT_ASSERT(provenType == SG_NOT_PROVEN);
}

void SosUctThreadStateTest::GeneratePlayoutMoveTest(void)
{
  this->threadState->GameStart();
  bool rave;
  SgMove move = this->threadState->GeneratePlayoutMove(rave);
  std::vector<SgMove> avails = this->state->availableMoves();
  CPPUNIT_ASSERT(find(avails.begin(), avails.end(), move) != avails.end());
}

void SosUctThreadStateTest::TakeBackInTreeTest(void)
{
  this->threadState->GameStart();
  this->threadState->Execute(static_cast<SgMove>(2));//white's move
  this->threadState->Execute(static_cast<SgMove>(1));
  this->threadState->TakeBackInTree(2);
  CPPUNIT_ASSERT(this->state->availableMoves().size() == 4);
}

void SosUctThreadStateTest::TakeBackPlayoutTest(void)
{
  this->threadState->GameStart();
  this->threadState->Execute(static_cast<SgMove>(2));//white's move
  this->threadState->Execute(static_cast<SgMove>(1));
  this->threadState->TakeBackPlayout(2);
  CPPUNIT_ASSERT(this->state->availableMoves().size() == 4);
}

