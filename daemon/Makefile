CXX=g++

all: 
	$(CXX) -std=c++11 -lwiringPi gardener_cmd.h gardener.cpp -o gardener

clean:
	rm -f $(obj) gardener

install:
	cp -f gardener /usr/bin/gardener
	
