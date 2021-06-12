#!/bin/sh

blocklist.py && gzip -f "${OUTPUT_DIR}/blocklist.p2p"
