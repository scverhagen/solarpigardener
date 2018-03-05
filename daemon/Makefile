CXX=g++

all: 
	$(CXX) -std=c++11 -lwiringPi gardener.cpp -o gardener

clean:
	rm -f $(obj) gardener

install:
	cp -f gardener /usr/bin/gardener
	
