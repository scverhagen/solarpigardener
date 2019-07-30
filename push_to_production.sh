#!/bin/bash

git checkout testing
git push origin
git push github
git checkout production
git merge testing
git push origin
git push github

git checkout testing
