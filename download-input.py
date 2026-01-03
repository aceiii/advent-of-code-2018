#!/bin/sh

year=2018
num="$1"

if ! [[ "$num" -gt 0 ]] 2>/dev/null; then
    echo "Usage: $0 [DAY_NUM]"
    exit 1
fi


env_file="$PWD/.env"
if [[ -f $env_file ]]; then
    source $env_file
fi

mkdir -p input

curl "https://adventofcode.com/$year/day/$num/input" \
    -H 'User-Agent: github.com/aceiii/advent-of-code-2025' \
    -H "Cookie: session=$AOC_SESSION" \
    --silent \
    -o "$PWD/input/day`printf %02d $num`"

