#!/bin/bash

# Get current timestamp in different formats
get_date_ymd() {
    date '+%Y-%m-%d'
}

get_date_ymd_hms() {
    date '+%Y-%m-%d %H:%M:%S'
}

get_iso_8601() {
    date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# Default to ISO 8601 if no format specified
if [ -z "$1" ]; then
    get_iso_8601
else
    case "$1" in
        "ymd") get_date_ymd ;;
        "full") get_date_ymd_hms ;;
        "iso") get_iso_8601 ;;
        *) get_iso_8601 ;;
    esac
fi 