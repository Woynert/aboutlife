#!/usr/bin/env bash

# TODO: Check binary exists
# create symlink on random temporary folder
# this is required, otherwise the process could be found with `ps -eo pid,cmd`
# suggestion: steal the comm name from another process instead of using uuidgen (it's only 15 chars)

rootdir=$(echo /tmp /dev/shm | xargs shuf -n1 -e)

workdir=$rootdir/$(uuidgen)
mkdir $workdir

binpath=$workdir/$(uuidgen)
ln -s `which $1` $binpath

# get a random process that doesn't include '['
# TODO: why?
# possible answer: it's because user process don't have it, so if the process has a [ it would stand out
procname=$(ps ax | grep -v '\[' | awk -v p='COMMAND' 'NR==1 {n=index($0, p); next} {print substr($0, n)}' | shuf -n 1)

echo $binpath
echo $procname
ls -l $workdir

# launch with a different process name
bash -c "exec -a '$procname' $binpath --preferences &" &

# remove launcher
# TODO: don't use rm -r use more safe commands
sleep 1 && rm "$binpath"; rmdir "$workdir"
exit 0


