#!/usr/bin/env python

import time
import subprocess
import datetime

from enum import Enum

class AudioState(Enum):
    PLAYING = 1
    OFF = 2
    UNDEFINED = 3

audio_state = AudioState.UNDEFINED
start_time = None
sub_total_seconds = 0
total_seconds = 0
total_seconds_file = '/etc/scripts/audio-quota/today_total_seconds'
today_date_file = "/etc/scripts/audio-quota/today_date"
quota_minutes_file = '/etc/scripts/audio-quota/quota_minutes'
suspended_file = '/etc/scripts/audio-quota/suspended'


def is_audio_playing():
    output = subprocess.getoutput("cat /proc/asound/card*/pcm0p/sub0/status | grep -i running")
    if len(output) > 0:
        return True
    else:
        return False

def mute_audio():
    subprocess.getoutput("amixer set Master mute")

def is_audio_muted():
    output = subprocess.getoutput("amixer get Master")
    if "[off]" in output:
        return True
    else:
        return False


while True:
    if audio_state == AudioState.UNDEFINED:
        try:
            with open(total_seconds_file, "r") as file:
                content = file.read()
            try:
                sub_total_seconds = int(content)
            except ValueError:
                sub_total_seconds = 0
        except FileNotFoundError:
            sub_total_seconds = 0
            print("Error: File not found.")

    suspended = 0

    with open(suspended_file, "r") as file:
        try:
            coo = file.read();
            print('coo value: ' + coo + 'xx')
            suspended = int(coo)
            print('read successful')
        except ValueError:
            print('read failed')
            suspended = 0

    if suspended == 1:
        start_time = None

        try:
            with open(total_seconds_file, "r") as file:
                content = file.read()
            try:
                sub_total_seconds = int(content)
            except ValueError:
                sub_total_seconds = 0
        except FileNotFoundError:
            sub_total_seconds = 0
            print("Error: File not found.")

        with open(suspended_file, "w") as file:
            file.write(str(0))


    if is_audio_playing() and not is_audio_muted():
        print("audio is playing")
        audio_state = AudioState.PLAYING

        if start_time is None:
            start_time = datetime.datetime.now()
        else:
            # get today_date from file
            # if today_date is not today, we need to reset sub_total_seconds, start_time, and total_seconds
            today_date = ""

            with open(today_date_file, "r") as file:
                today_date = file.read()

            current = datetime.datetime.now()

            if today_date != current.strftime("%Y-%m-%d"):
                sub_total_seconds = 0
                start_time = current
                total_seconds = 0

                with open(today_date_file, "w") as file:
                    file.write(start_time.strftime("%Y-%m-%d"))
            else:
                total_seconds = sub_total_seconds + (current - start_time).total_seconds()

            with open(total_seconds_file, "w") as file:
                file.write(str(int(total_seconds)))

            # get quota_minutes from file,
            # if the total_seconds is greater than the quota_minutes, we need to mute the audio
            quota_minutes = 0

            with open(quota_minutes_file, "r") as file:
                quota_minutes = float(file.read())

            if total_seconds > quota_minutes * 60:
                print("audio is muted")
                mute_audio()
                audio_state = AudioState.OFF

    else:
        print("audio is not playing")
        audio_state = AudioState.OFF
    time.sleep(6)
