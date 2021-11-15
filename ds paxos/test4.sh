#!/bin/sh
rm output.txt
export DISPLAY=:0.0
javac Council.java Member.java 
java Council 5060 &
java Member M1 5060 &
java Member M4 5060 &

sleep 10s
if comm -12 "output.txt" "test4_actual_output.txt"
then
    clear
    printf 'passed\n' 
else
    clear
    printf 'failed\n'  
fi

$SHELL