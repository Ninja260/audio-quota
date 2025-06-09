#!/usr/bin/env python

import argparse
import alsaaudio

quota_minutes_file = '/etc/scripts/audio-quota/quota_minutes'
total_seconds_file = "/etc/scripts/audio-quota/today_total_seconds"

parser = argparse.ArgumentParser()
parser.add_argument("--hour", type=float,help="set hour quota in float")
args = parser.parse_args()

hourval = args.hour

def unmute_audio():
    mixer = alsaaudio.Mixer('Master')
    mixer.setmute(False)

# if hourval is not null
if hourval is not None:
    unmute_audio()
    with open(quota_minutes_file, "w") as file:
        file.write(str(int(args.hour * 60)))
else:
    with open(quota_minutes_file, "r") as file:
        quota = int(file.read())
        print('Quota: '+ str(quota / 60) + ' hours')
    try:
        with open(total_seconds_file, "r") as file:
            try:
                total_seconds = int(file.read())
            except ValueError:
                total_seconds = 0

            hour = total_seconds // 3600
            minute = (total_seconds - (hour * 3600)) // 60
            seconds = total_seconds - (hour * 3600) - (minute * 60)

            detailed_time = '' if hour == 0 else str(hour) + ' hours '
            detailed_time += '' if minute == 0 else str(minute) + ' minutes '
            detailed_time += '' if seconds == 0 else str(seconds) + ' seconds'

            if detailed_time == '':
                detailed_time = '0 seconds'

            print('Used: '+ detailed_time)
    except FileNotFoundError:
        print('Used: 0 hours')
