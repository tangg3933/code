#!/bin/sh
rm output.txt
export DISPLAY=:0.0
javac Council.java Member.java 
java Council 6010 &
sleep 2s
java Member M1 6010 &
java Member M2 6010 &
java Member M3 6010 &
java Member M4 6010 &
java Member M5 6010 &
java Member M6 6010 &
java Member M7 6010 &
java Member M8 6010 &
java Member M9 6010 &

sleep 15s
if comm -12 "output.txt" "test5_actual_output.txt"
then
    clear
    printf 'passed\n' 
else
    clear
    printf 'failed\n'  
fi

$SHELL