@echo off
REM Always run Django with the project's virtualenv, not the global Python.
"%~dp0env\Scripts\python.exe" "%~dp0manage.py" runserver %*
