@echo off
if not exist omnisetup mkdir omnisetup && cd omnisetup
curl -fsSL https://raw.githubusercontent.com/Jessiebrig/OmniSetup/refs/heads/main/setup.cmd -o setup.cmd
call setup.cmd
