#!/usr/bin/env python

import time
import subprocess
import datetime
import alsaaudio

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
    mixer = alsaaudio.Mixer('Master')
    mixer.setmute(True)

def is_audio_muted():
    mixer = alsaaudio.Mixer('Master')
    mute_list = mixer.getmute()

    return all(x == 1 for x in mute_list)

def read_total_seconds_file():
    try:
        with open(total_seconds_file, "r") as file:
            content = file.read()
        try:
            total_seconds = int(content)
        except ValueError:
            total_seconds = 0
    except FileNotFoundError:
        total_seconds = 0
        print("Error: File not found.")

    return total_seconds

def write_total_seconds_file(total_seconds):
    with open(total_seconds_file, "w") as file:
        file.write(str(int(total_seconds)))

def read_today_date_file():
    today_date = ""

    with open(today_date_file, "r") as file:
        today_date = file.read()

    return today_date

def write_today_date_file(today_date):
    with open(today_date_file, "w") as file:
        file.write(today_date)

def read_quota_minutes_file():
    quota_minutes = 0

    with open(quota_minutes_file, "r") as file:
        quota_minutes = float(file.read())

    return quota_minutes

def read_suspended_file():
    suspended = 0

    with open(suspended_file, "r") as file:
        try:
            suspended = int(file.read())
            print('suspend read: '+ str(suspended))
        except ValueError:
            print('suspend read failed')
            suspended = 0

    return suspended

def write_suspended_file(suspended):
    with open(suspended_file, "w") as file:
        file.write(str(int(suspended)))

while True:
    if audio_state == AudioState.UNDEFINED:
        sub_total_seconds = read_total_seconds_file()

    suspended = read_suspended_file()

    if suspended == 1:
        start_time = None
        sub_total_seconds = read_total_seconds_file()
        write_suspended_file('0');

    today_date = read_today_date_file()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    if today_date != current_date:
        write_today_date_file(current_date)

        sub_total_seconds = 0
        write_total_seconds_file(sub_total_seconds)

        if(start_time is not None):
            start_time = datetime.datetime.now()

    if is_audio_playing() and not is_audio_muted():
        print("audio is playing")
        audio_state = AudioState.PLAYING

        current = datetime.datetime.now();

        if start_time is None:
            start_time = current

        total_seconds = sub_total_seconds + (current - start_time).total_seconds()

        write_total_seconds_file(total_seconds)

        quota_minutes = read_quota_minutes_file()

        if total_seconds > quota_minutes * 60:
            print("audio is muted")
            mute_audio()
            audio_state = AudioState.OFF
    else:
        print("audio is not playing")

        if start_time is not None:
            start_time = None
            sub_total_seconds = read_total_seconds_file()

        audio_state = AudioState.OFF

    time.sleep(6)
