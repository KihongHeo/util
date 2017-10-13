#!/bin/bash

# count LOC for java byte codes

count=0
for c in `find classes -name "*.class"`
do
  # drop ".class"
  name="${c%.*}"
  echo $name
  l=`javap -c $name | wc -l`
  count=`expr $count + $l`
done
echo $count
