CXX=g++

all: 
	make -C daemon

clean:
	make -C daemon clean

install:
	make -C daemon install
	./scripts/mksymlinks.sh
	./scripts/installservice.sh
	
