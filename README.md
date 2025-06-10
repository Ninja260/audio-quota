# audio-quota

Linux cli app to control audio output time by daily quota.

Currently, only tested for the Ubuntu.

You need to have `pyalsaaudio` package installed on your system before installing the script.

```console
foo@bar:~$ pip install pyalsaaudio
```

To check the remaining audio quota of the day.

```console
foo@bar:~$ audio-quota
Quota: 4.0 hours
Used: 23 minutes 2 seconds
```

To set the daily audio quota.

```console
foo@bar:~$ audio-quota --hour 4.5
```

Quota can only be set in term of hour.

## Installation

```console
foo@bar:~$ git clone https://github.com/Ninja260/audio-quota.git
foo@bar:~$ cd audio-quota
foo@bar:~/audio-quota$ ./install.sh
```

## Uninstall

```console
foo@bar:~$ cd audio-quota
foo@bar:~/audio-quota$ ./uninstall.sh
```
