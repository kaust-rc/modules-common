#!/bin/bash

mode=''
name=''
path=''

# Let's read in the inputs
while [ $# -gt 0 ]; do
    case "$1" in
        --mode)
            shift
            mode="$1"
            shift
        ;;

        --name)
            shift
            name="$1"
            shift
        ;;

        --path)
            shift
            path="$1"
            shift
        ;;

        --help|-h)
cat << EOF
usage: $0
    --mode        <command>, Specify command user passed to module
    --name        <name>, Specify module user wants to load
    --path        <fullpath>, Specify path of module file being loaded
EOF
            exit 0
        ;;

        -*)
            echo "$0: error - unrecognized option $1" 1>&2
            exit 1
        ;;

        *)  break
        ;;
    esac
done

kaust_id=$(id -u)
hostname=$(hostname -s)

echo "KAUST ID is $kaust_id" 1>&2
echo "Host is $hostname" 1>&2
echo "Mode is $mode" 1>&2
echo "Name is $name" 1>&2
echo "Path is $path" 1>&2

curl --connect-timeout 1 http://myws.kaust.edu.sa/logs?mode=$mode&name=$name&path=$path&hostname=$hostname&id=$kaust_id/ 1>&2 2>/dev/null
