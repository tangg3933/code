#!/bin/sh
rm output.txt
export DISPLAY=:0.0
javac Council.java Member.java 
java Council 5090 &
java Member M1 5090 &
java Member M2 5090 &
java Member M3 5090 &
java Member M4 5090 &
java Member M5 5090 &
java Member M6 5090 &
java Member M7 5090 &
java Member M8 5090 &
java Member M9 5090 &
sleep 15s
clear
$SHELL