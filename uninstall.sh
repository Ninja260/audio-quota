#! /bin/bash

# uninstall audio-quota.service
sudo systemctl stop audio-quota.service
sudo systemctl disable audio-quota.service
sudo rm /etc/systemd/system/audio-quota.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

# remove symmetric link
sudo rm /usr/bin/audio-quota

# remove audio_quota_on_suspend from system-sleep
sudo rm /lib/systemd/system-sleep/audio_quota_on_suspend

# remove audio-quota script directory
sudo rm -r /etc/scripts/audio-quota/

echo "Uninstallation successful!"
