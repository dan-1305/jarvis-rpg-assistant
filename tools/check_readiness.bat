@echo off
REM Change to project root directory (parent of tools/)
cd /d "%~dp0.."

REM Quick alias for public readiness check
python tools\public_readiness_check.py %*
