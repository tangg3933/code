#!/bin/sh
rm output.txt
export DISPLAY=:0.0
javac Council.java Member.java 
java Council 4020 &
java Member M6 4020 &

sleep 12s
if comm -12 "output.txt" "test3_actual_output.txt"
then
    clear
    printf 'passed\n' 
else
    clear
    printf 'failed\n'  
fi

$SHELL