#!/bin/bash
killall firefox
firefox -P "Bril_DOC_instructions" --no-remote &
firefox -P "Bril_DOC_tunneled" --no-remote &
