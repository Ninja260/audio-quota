#!/bin/bash

case "$1" in
pre)
	echo 1 >/etc/scripts/audio-quota/suspended
	# "$logsr" suspend
	;;
post)
	# nothing
	;;
*)
	# nothing
	;;
esac
