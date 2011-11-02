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
SOS_OBJECTS=${SOS_SMARTGAME_TEST}/ftest.o ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.o SosUctSearch.o ${SOS_SMARTGAME_TEST}/SosGameTest.o SosGame.o SosPlayer.o
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

ftest:  ${SOS_OBJECTS}
	gcc -o ftest ${SOS_OBJECTS} $(LIBS) -L${CPPUNIT_PATH}/lib -lstdc++ -lcppunit -ldl 

SosGame.o: SosGame.cpp SosPlayer.h SosGame.h

SosPlayer.o: SosPlayer.cpp SosPlayer.h

SosUctSearch.o: SosUctSearch.cpp SosUctSearch.h

${SOS_SMARTGAME_TEST}/SosGameTest.o: ${SOS_SMARTGAME_TEST}/SosGameTest.cc ${SOS_SMARTGAME_TEST}/SosGameTest.h

${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.o: ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.cc ${SOS_SMARTGAME_TEST}/SosUctThreadStateTest.h

${SOS_SMARTAME_TEST}/ftest.o: ${SOS_SMARTGAME_TEST}/ftest.cc

clean:
	rm -f *.o ftest

