#!/bin/bash
mkdir -p OmniSetup && cd OmniSetup
curl -fsSL https://raw.githubusercontent.com/Jessiebrig/OmniSetup/refs/heads/main/setup.sh -o setup.sh

chmod +x setup.sh && ./setup.sh
