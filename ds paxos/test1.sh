#!/bin/sh
rm output.txt
export DISPLAY=:0.0
javac Council.java Member.java 
java Council 2050 &
java Member M3 2050 &

sleep 10s
if comm -12 "output.txt" "test1_actual_output.txt"
then
    clear
    printf 'passed\n' 
else
    clear
    printf 'failed\n'  
fi

$SHELL