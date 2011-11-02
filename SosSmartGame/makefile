# file: makefile
# next line has to be changed to the installation-path of CppUnit
CPPUNIT_PATH=/users/studs/bsc/2011/shanive/freespace/cppunit-1.12.1/install
SOS_SMARTGAME_TEST=/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/SosSmartGame/tests
SOS_SMARTGAME=/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/SosSmartGame
SMARTGAMELIB=/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/fuego-1.1/smartgame
SOS_OBJECTS=ftest.o SosUctThreadStateTest.o SosUctSearch.o SosGameTest.o SosGame.o SosPlayer.o SgUctSearch.o

ftest:  ${SOS_OBJECTS}
	gcc -o ftest ${SOS_OBJECTS} -L${CPPUNIT_PATH}/lib -lstdc++ -lcppunit -ldl

SosGame.o: SosGame.cpp SosPlayer.h SosGame.h
	g++ -c  SosGame.cpp 

SosPlayer.o: SosPlayer.cpp SosPlayer.h
	g++ -c SosPlayer.cpp

SosUctSearch.o: SosUctSearch.cpp SosUctSearch.h
	g++ -c SosUctSearch.cpp

SgUctSearch.o: ${SMARTGAMELIB}/SgUctSearch.cpp ${SMARTGAMELIB}/SgUctSearch.h
	g++ -c ${SMARTGAMELIB}/SgUctSearch.cpp

SosGameTest.o: ${SOS_SMARTGAME_TEST}/SosGameTest.cc ${SOS_SMARTGAME_TEST}/SosGameTest.h
	g++ -c ${SOS_SMARTGAME_TEST}/SosGameTest.cc -I${CPPUNIT_PATH}/include

SosUctThreadStateTest.o: ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.cc ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.h
	g++ -c ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.cc -I${CPPUNIT_PATH}/include

ftest.o: ${SOS_SMARTGAME_TEST}/ftest.cc
	g++ -c ${SOS_SMARTGAME_TEST}/ftest.cc -I${CPPUNIT_PATH}/include

clean:
	rm -f *.o ftest

