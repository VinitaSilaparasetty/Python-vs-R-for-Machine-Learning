@echo off
echo Checking for accidental secrets...
git grep -n "API_KEY"
if errorlevel 1 (
    echo No secrets found
)
