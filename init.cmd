@echo off
if not exist OmniSetup mkdir OmniSetup && cd OmniSetup
curl -fsSL https://raw.githubusercontent.com/Jessiebrig/OmniSetup/refs/heads/main/setup.cmd -o setup.cmd
call setup.cmd
