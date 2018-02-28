#!/bin/bash
./scripts/mksymlinks.sh
cd ./daemon
make
sudo make install
cd ..
