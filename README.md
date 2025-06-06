# audio-quota

Linux cli app to control audio output time by daily quota.

Currently, only tested for the Ubuntu Linux.

To check the remaining audio quota of the day.

```console
foo@bar:~$ audio-quota 
```

To set the daily audio quota.

```console
foo@bar:~$ audio-quota --hour 4.5
```

Currently, we can only set quota in term of hours.

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
