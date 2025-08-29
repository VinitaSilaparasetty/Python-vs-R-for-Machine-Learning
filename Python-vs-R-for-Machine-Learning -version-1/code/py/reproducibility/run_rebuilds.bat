@echo off
REM Windows batch equivalent of run_rebuilds.sh
REM Runs reproducibility test 10 times using pipenv

FOR /L %%i IN (1,1,10) DO (
    echo Rebuild %%i...
    REM Remove any existing virtualenv
    pipenv --rm >nul 2>&1

    REM Reinstall environment based on Pipfile.lock
    pipenv install --ignore-pipfile >nul 2>&1

    REM Run a quick test to check if numpy, pandas, sklearn import
    pipenv run python -c "import numpy, pandas, sklearn; print('ok')" >nul 2>&1

    IF ERRORLEVEL 1 (
        echo Rebuild %%i failed
    ) ELSE (
        echo Rebuild %%i succeeded
    )
)
