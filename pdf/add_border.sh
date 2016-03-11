#!/bin/bash

for i in `cat ../rarity.txt`
do
	if [ ${#i} == 1 ]
	then
		if [ $i == C ]
		then
			convert images_original/$f.png -background black -alpha remove -bordercolor gray -border 7x7 images/$f.png
		elif [ $i == U ]
		then
			convert images_original/$f.png -background black -alpha remove -bordercolor limegreen -border 7x7 images/$f.png
		elif [ $i == R ]
		then
			convert images_original/$f.png -background black -alpha remove -bordercolor cyan -border 7x7 images/$f.png
		elif [ $i == E ]
		then
			convert images_original/$f.png -background black -alpha remove -bordercolor indigo -border 7x7 images/$f.png
		fi
	else
		f=$i
	fi
done
