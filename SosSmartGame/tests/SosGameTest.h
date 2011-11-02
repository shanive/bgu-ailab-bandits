// file: SosGameTest.h
#ifndef SOSGAMETEST_H
#define SOSGAMETEST_H

#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>
#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/SosSmartGame/SosGame.h"

using namespace std;

class SosState;

class SosStateTest : public CPPUNIT_NS :: TestFixture
{
    CPPUNIT_TEST_SUITE (SosStateTest);
    CPPUNIT_TEST (availableMovesTest);
    CPPUNIT_TEST (isWhiteTurnTest);
    CPPUNIT_TEST (playTest);
    CPPUNIT_TEST (whiteMovesTest);
    CPPUNIT_TEST (blackMovesTest);
    CPPUNIT_TEST (sizeTest);
    CPPUNIT_TEST (undoTest);
    CPPUNIT_TEST_SUITE_END ();

    public:
        void setUp (void);
        void tearDown (void);

    protected:
        void availableMovesTest (void);
        void isWhiteTurnTest (void);
        void playTest (void);
        void whiteMovesTest (void);
     	void blackMovesTest (void);
	void sizeTest (void);
	void undoTest (void);

    private:
        SosState* state;
};


class SosGame;

class SosGameTest : public CPPUNIT_NS :: TestFixture
{
	CPPUNIT_TEST_SUITE (SosGameTest);
	CPPUNIT_TEST (isFinalStateTest);
	CPPUNIT_TEST (twoPlayersGameTest);	
	CPPUNIT_TEST (gameScoreTest);
	CPPUNIT_TEST (scoreBonusTest);
	CPPUNIT_TEST (winLossTest);
	CPPUNIT_TEST_SUITE_END ();

    public:
        void setUp (void);
        void tearDown (void);

    protected:
	void isFinalStateTest (void);
	void twoPlayersGameTest (void);
	void gameScoreTest (void);
	void scoreBonusTest (void);
	void winLossTest (void);

    private:
	SosGame* game;
	SosState* state;

};

#endif
