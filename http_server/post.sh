#!/bin/sh
curl -X POST http://0.0.0.0:$1/cgi-bin/env.cgi -H 'cache-control: no-cache'