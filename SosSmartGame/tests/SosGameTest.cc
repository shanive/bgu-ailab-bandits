// file: SosGameTest.cc

#include "SosGameTest.h"
#include <vector>
#include "SgMove.h"
#include <algorithm>
#include "../SosGame.h"
#include "../SosPlayer.h"

CPPUNIT_TEST_SUITE_REGISTRATION (SosStateTest);

void SosStateTest::setUp(void)
{
	this->state = new SosState(10);
}

void SosStateTest::tearDown(void)
{
	delete this->state;
}

void SosStateTest::availableMovesTest(void)
{
	std::vector<SgMove> avails = this->state->availableMoves();
	CPPUNIT_ASSERT(static_cast<int>(avails.size()) == 10);
	this->state->play(static_cast<SgMove>(5));
	avails = this->state->availableMoves();
	std::vector<SgMove>::iterator it;
	it = find(avails.begin(), avails.end(), static_cast<SgMove>(5));
	CPPUNIT_ASSERT(it == avails.end());
	CPPUNIT_ASSERT(static_cast<int>(avails.size()) == 9);
}
	
void SosStateTest::isWhiteTurnTest(void)
{
	CPPUNIT_ASSERT(!this->state->isWhiteTurn());
	this->state->play(static_cast<SgMove>(5));
	CPPUNIT_ASSERT(this->state->isWhiteTurn());
}

void SosStateTest::playTest(void)
{
	this->state->play(static_cast<SgMove>(5));
	std::vector<SgMove> blacks = this->state->blackMoves();
	CPPUNIT_ASSERT(blacks.size() == 1);
	CPPUNIT_ASSERT_EQUAL(static_cast<int>(blacks.at(0)),5);
	CPPUNIT_ASSERT(static_cast<int>(this->state->availableMoves().size()) == 9);
	CPPUNIT_ASSERT(this->state->isWhiteTurn());
}

void SosStateTest::whiteMovesTest(void)
{
  this->state->setTurn(SG_WHITE);
	this->state->play(static_cast<SgMove>(5));
	std::vector<SgMove> whites = this->state->whiteMoves();
	CPPUNIT_ASSERT(whites.size() == 1);
	CPPUNIT_ASSERT_EQUAL(static_cast<int>(whites.at(0)),5);
}

void SosStateTest::blackMovesTest(void)
{
	this->state->play(static_cast<SgMove>(1));//black's move
	std::vector<SgMove> blacks = this->state->blackMoves();
	CPPUNIT_ASSERT(blacks.size() == 1);
	CPPUNIT_ASSERT_EQUAL(static_cast<int>(blacks.at(0)),1);
}

void SosStateTest::sizeTest(void)
{
	CPPUNIT_ASSERT_EQUAL(static_cast<int>(this->state->size()),10);
}

void SosStateTest::undoTest(void)
{	 
	this->state->play(static_cast<SgMove>(5));//BLACK's move
	this->state->play(static_cast<SgMove>(1));//white's move

	this->state->undo(1);
	std::vector<SgMove> avails = this->state->availableMoves();
	std::vector<SgMove>::iterator it;
	it = find(avails.begin(), avails.end(), static_cast<SgMove>(1));
	CPPUNIT_ASSERT(it != avails.end());
	it = find(avails.begin(), avails.end(), static_cast<SgMove>(5));
	CPPUNIT_ASSERT(it == avails.end());
}


CPPUNIT_TEST_SUITE_REGISTRATION (SosGameTest);

void SosGameTest::setUp(void)
{
        this->game = new SosGame(4, false, SosGame::ASCENDING);
	this->state = new SosState(4);
}

void SosGameTest::tearDown(void)
{
	delete this->game;
	delete this->state;
}

void SosGameTest::isFinalStateTest(void)
{	
	CPPUNIT_ASSERT (!this->game->isFinalState(*this->state)); 
	this->state->play(static_cast<SgMove>(2));//white's move
	this->state->play(static_cast<SgMove>(1));//black's move
	this->state->play(static_cast<SgMove>(3));//white's move
	this->state->play(static_cast<SgMove>(0));//black's move
	CPPUNIT_ASSERT (this->game->isFinalState(*this->state));
}

void SosGameTest::twoPlayersGameTest(void)
{
	SosPlayer *first = new SosLeftPlayer(this->game);
	SosPlayer *second = new SosLeftPlayer(this->game);
	double score = game->twoPlayersGame(first, second);
	CPPUNIT_ASSERT (score == 0);
	delete first;
	delete second;
}

void SosGameTest::gameScoreTest(void)
{
	this->state->play(static_cast<SgMove>(1));//black's move
	this->state->play(static_cast<SgMove>(2));//white's move
	this->state->play(static_cast<SgMove>(3));//black's move
	this->state->play(static_cast<SgMove>(0));//white's move
	CPPUNIT_ASSERT (this->game->gameScore(*this->state) == 0.0);
        //difference not bigget than komi = 2
}

void SosGameTest::scoreBonusTest(void)
{
	this->state->play(static_cast<SgMove>(1));//white's move
	this->state->play(static_cast<SgMove>(2));//black's move
	this->state->play(static_cast<SgMove>(3));//white's move
	this->state->play(static_cast<SgMove>(0));//black's move
	CPPUNIT_ASSERT (this->game->scoreBonus(*this->state) == 2);
}

void SosGameTest::winLossTest(void)
{
	this->state->play(static_cast<SgMove>(0));
	this->state->play(static_cast<SgMove>(2));
	this->state->play(static_cast<SgMove>(1));
	this->state->play(static_cast<SgMove>(3));
	CPPUNIT_ASSERT (this->game->winLoss(*this->state) == 0);
}
