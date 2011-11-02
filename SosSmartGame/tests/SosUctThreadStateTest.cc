#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/SosSmartGame/SosGame.h"
#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/SosSmartGame/SosUctSearch.h"
#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/fuego-1.1/smartgame/SgMove.h"
#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/fuego-1.1/smartgame/SgUctTree.h"
#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/fuego-1.1/smartgame/SgBlackWhite.h"
#include "SosUctThreadStateTest.h"
#include <vector>

CPPUNIT_TEST_SUITE_REGISTRATION (SosUctThreadStateTest);

void SosUctThreadStateTest::setUp(void)
{
	this->game = new SosGame(4, false, ASCENDING);
	this->state = new SosState(4);
	this->threadState = new SosUctThreadState(0, SG_WHITE, this->game, this->state); 
}

void SosUctThreadStateTest::tearDown(void)
{
	delete this->state;
	delete this->game;
	delete this->threadState;
}

void SosUctThreadStateTest::EvaluateTest(void)
{
	this->state->play(static_cast<SgMove>(2));//white's move
	this->state->play(static_cast<SgMove>(1));//black's move
	this->state->play(static_cast<SgMove>(3));//white's move
	this->state->play(static_cast<SgMove>(0));//black's move
	CPPUNIT_ASSERT(static_cast<double>(this->threadState->Evaluate()) 
				== 1);
}

void SosUctThreadStateTest::ExecuteTest(void)
{
	this->threadState->Execute(static_cast<SgMove>(2));
	std::vector<SgMove> whites = this->state->whiteMoves();
	CPPUNIT_ASSERT(whites.size() == 1);
	CPPUNIT_ASSERT(static_cast<int>(whites.at(0)) == 2);
}
 
void SosUctThreadStateTest::ExecutePlayoutTest(void)
{
	this->threadState->ExecutePlayout(static_cast<SgMove>(2));
	std::vector<SgMove> whites = this->state->whiteMoves();
	CPPUNIT_ASSERT(whites.size() == 1);
	CPPUNIT_ASSERT(static_cast<int>(whites.at(0)) == 2);
}
 
void SosUctThreadStateTest::GenerateAllMovesTest(void)
{
	std::vector<SgUctMoveInfo> moves;
	SgUctProvenType provenType;
	CPPUNIT_ASSERT(!this->threadState->GenerateAllMoves(0, moves, provenType));
	CPPUNIT_ASSERT(moves.size() == 4);
	CPPUNIT_ASSERT(provenType == SG_NOT_PROVEN);
	this->state->play(static_cast<SgMove>(2));//white's move
	this->state->play(static_cast<SgMove>(1));//black's move
	this->state->play(static_cast<SgMove>(3));//white's move
	this->state->play(static_cast<SgMove>(0));//black's move
	CPPUNIT_ASSERT(this->threadState->GenerateAllMoves(0, moves, provenType));
	CPPUNIT_ASSERT(moves.size() == 0);
	CPPUNIT_ASSERT(provenType == SG_PROVEN_WIN);
}

void SosUctThreadStateTest::GeneratePlayoutMoveTest(void)
{
	bool rave;
	SgMove move = this->threadState->GeneratePlayoutMove(rave);
	std::vector<SgMove> avails = this->state->availableMoves();
	CPPUNIT_ASSERT(find(avails.begin(), avails.end(), move) == avails.end());
}

void SosUctThreadStateTest::TakeBackInTreeTest(void)
{
	this->state->play(static_cast<SgMove>(2));//white's move
	this->state->play(static_cast<SgMove>(1));
	this->threadState->TakeBackInTree(2);
	CPPUNIT_ASSERT(this->state->availableMoves().size() == 4);
}

void SosUctThreadStateTest::TakeBackPlayoutTest(void)
{
	this->state->play(static_cast<SgMove>(2));//white's move
	this->state->play(static_cast<SgMove>(1));
	this->threadState->TakeBackInTree(2);
	CPPUNIT_ASSERT(this->state->availableMoves().size() == 4);
}

