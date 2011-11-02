// file: SosUctThreadStateTest.h
#ifndef SOS_UCTTHREADSTATE_TEST_H
#define SOS_UCTTHREADSTATE_TEST_H

#include <cppunit/TestFixture.h>
#include <cppunit/extensions/HelperMacros.h>
#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/SosSmartGame/SosUctSearch.h"

using namespace std;

class SosGame;
class SosState;

class SosUctThreadStateTest : public CPPUNIT_NS :: TestFixture
{
	CPPUNIT_TEST_SUITE (SosUctThreadStateTest);
	CPPUNIT_TEST (EvaluateTest);
	CPPUNIT_TEST (ExecuteTest);
	CPPUNIT_TEST (ExecutePlayoutTest);
	CPPUNIT_TEST (GenerateAllMovesTest);
	CPPUNIT_TEST (GeneratePlayoutMoveTest);
	CPPUNIT_TEST (TakeBackInTreeTest);
	CPPUNIT_TEST (TakeBackPlayoutTest);
	CPPUNIT_TEST_SUITE_END ();

	public:
		void setUp (void);
        	void tearDown (void);
	
	protected:
		void EvaluateTest(void);
		void ExecuteTest(void);
		void ExecutePlayoutTest(void);
		void GenerateAllMovesTest(void);
		void GeneratePlayoutMoveTest(void);
		void TakeBackInTreeTest(void);
		void TakeBackPlayoutTest(void);
	
	private:
		SosUctThreadState *threadState;
		SosGame *game;
		SosState *state;
};
	
#endif //SOS_UCTTHREADSTATE_TEST_H
