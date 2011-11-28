# file: makefile
# next line has to be changed to the installation-path of CppUnit
BOOST_CPPFLAGS = -pthread -I/usr/include
BOOST_DATE_TIME_LIB = -lboost_date_time-mt
BOOST_FILESYSTEM_LIB = -lboost_filesystem-mt
BOOST_LDFLAGS = -L/usr/lib
BOOST_PROGRAM_OPTIONS_LIB = -lboost_program_options-mt
BOOST_SYSTEM_LIB = -lboost_system-mt
BOOST_THREAD_LIB = -lboost_thread-mt
BOOST_UNIT_TEST_FRAMEWORK_LIB = -lboost_unit_test_framework-mt

SOS_SMARTGAME_TEST=tests
FTEST_OBJECTS=${SOS_SMARTGAME_TEST}/ftest.o ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.o SosUctSearch.o ${SOS_SMARTGAME_TEST}/SosUctPlayerTest.o ${SOS_SMARTGAME_TEST}/SosGameTest.o SosGame.o SosPlayer.o SosUctPlayer.o
TOUR_OBJECTS=SosSgTournament.o SosGame.o SosPlayer.o SosUctPlayer.o SosUctSearch.o
OPTIMAL_OBJECTS = SosGame.o SosPlayer.o SosRavePlayer.o SosUctPlayer.o SosUctSearch.o OptimalFirstPlay.o
CFLAGS=-I../fuego-1.1/smartgame $(BOOST_CPPFLAGS) -O -g
LIBS=\
../fuego-1.1/smartgame/libfuego_smartgame.a \
../fuego-1.1/gtpengine/libfuego_gtpengine.a \
$(BOOST_PROGRAM_OPTIONS_LIB) \
$(BOOST_FILESYSTEM_LIB) \
$(BOOST_SYSTEM_LIB) \
$(BOOST_THREAD_LIB)

%.o: %.cpp
	g++ -c $(CFLAGS) -o $@ $<

%.o: %.cc
	g++ -c $(CFLAGS) -o $@ $<

ftest:  ${FTEST_OBJECTS}
	gcc -o ftest ${FTEST_OBJECTS} $(LIBS) -L${CPPUNIT_PATH}/lib -lstdc++ -lcppunit -ldl 
tour: ${TOUR_OBJECTS}
	gcc -o tour ${TOUR_OBJECTS} $(LIBS) -lstdc++ -ldl
optimal: ${OPTIMAL_OBJECTS} 
	gcc -o optimal ${OPTIMAL_OBJECTS} $(LIBS) -lstdc++ -ldl

SosGame.o: SosGame.cpp SosPlayer.h SosGame.h

SosPlayer.o: SosPlayer.cpp SosPlayer.h

SosRavePlayer.o: SosRavePlayer.cpp SosRavePlayer.h

SosUctPlayer.o: SosUctPlayer.cpp SosUctPlayer.h

SosUctSearch.o: SosUctSearch.cpp SosUctSearch.h

${SOS_SMARTGAME_TEST}/SosUctPlayerTest.o: ${SOS_SMARTGAME_TEST}/SosUctPlayerTest.cpp ${SOS_SMARTGAME_TEST}/SosUctPlayerTest.h 

${SOS_SMARTGAME_TEST}/SosGameTest.o: ${SOS_SMARTGAME_TEST}/SosGameTest.cc ${SOS_SMARTGAME_TEST}/SosGameTest.h

${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.o: ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.cc ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.h

${SOS_SMARTAME_TEST}/ftest.o: ${SOS_SMARTGAME_TEST}/ftest.cc

SosSgTournament.o: SosSgTournament.cpp

OptimalFirstPlay.o: OptimalFirstPlay.cpp

clean_ftest:
	rm -f *.o ftest

clean_tour:
	rm -f *.o tour

clean_optimal:
	rm -f *.o optimal
