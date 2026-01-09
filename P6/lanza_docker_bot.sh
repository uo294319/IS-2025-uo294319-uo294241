#!/bin/bash

docker run -d \
  --name bot-prosody \
  --network pruebas \
  -e CLAVEBOT="bot" \
  -e IP_SERVIDOR="prosody" \
  -v $(pwd)/etc:/etc \
  prosody_bot_image