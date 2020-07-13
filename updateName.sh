#! /bin/bash
a="\"$1\""
sed -i -e "s/\(MY_DEV_NAME = \).*/\1$a/" server/btk_server.py
