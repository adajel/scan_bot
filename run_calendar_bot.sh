#!/usr/bin/env python3

# run only on odd weeks
WEEK=`date +%V`
nozero=$(echo $WEEK | sed 's/^0*//')
if ! [ $(($nozero%2)) -eq 0 ];
then
    cd /home/ada/repos/scan_bot/
    python3 calendar_bot.py $1
fi
