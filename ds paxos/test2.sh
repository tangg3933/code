#!/bin/sh
rm output.txt
export DISPLAY=:0.0
javac Council.java Member.java 
java Council 3000 &
java Member M6 3000 &

sleep 10s
if comm -12 "output.txt" "test2_actual_output.txt"
then
    clear
    printf 'passed\n' 
else
    clear
    printf 'failed\n'  
fi

$SHELL