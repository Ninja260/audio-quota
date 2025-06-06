#! /bin/bash

CWD="$(cd "$(dirname "$(realpath "${BASH_SOURCE[0]}")")" && pwd)"

# move script files
[ -e /etc/scripts/audio-quota ] || sudo mkdir -p /etc/scripts/audio-quota
sudo cp $CWD/src/* /etc/scripts/audio-quota/
sudo chmod 666 /etc/scripts/audio-quota/quota_minutes
sudo chmod 666 /etc/scripts/audio-quota/today_date
sudo chmod 666 /etc/scripts/audio-quota/today_total_seconds
sudo chmod 666 /etc/scripts/audio-quota/suspended

# move audio_quota_on_suspend.sh
sudo cp $CWD/src/audio_quota_on_suspend.sh /lib/systemd/system-sleep/audio_quota_on_suspend

# make symmetric link
sudo ln -s /etc/scripts/audio-quota/audio-quota.py /usr/bin/audio-quota

# install audio-quota.service
sudo cp $CWD/src/audio-quota.service /etc/systemd/system/audio-quota.service
sudo systemctl start audio-quota
sudo systemctl enable audio-quota

echo "Installation successful!"
