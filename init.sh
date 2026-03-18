#!/bin/bash
mkdir -p omnisetup && cd omnisetup
curl -fsSL https://raw.githubusercontent.com/Jessiebrig/OmniSetup/refs/heads/main/setup.sh -o setup.sh
exec < /dev/tty
bash setup.sh
