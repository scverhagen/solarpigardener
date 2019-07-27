#!/bin/bash

#current commit hash:
git log --pretty=format:'%H' -n 1 > commit.txt

#build docker image:
docker build -t scverhagen/solarpigardener .
