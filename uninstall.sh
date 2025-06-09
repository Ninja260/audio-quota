#! /bin/bash

# remove audio-quota service startup file
sudo rm /etc/xdg/autostart/audio-quota.desktop

# remove symmetric link
sudo rm /usr/bin/audio-quota

# remove audio_quota_on_suspend from system-sleep
sudo rm /lib/systemd/system-sleep/audio_quota_on_suspend

# remove audio-quota script directory
sudo rm -r /etc/scripts/audio-quota/

# kill the running service script
ps aux | grep "audio-quota-service" | grep -v "grep" | awk '{print $2}' | xargs kill > /dev/null

echo "Uninstallation successful!"
