@echo off
setlocal
chcp 65001 >nul

cd /d "%~dp0"

set "COMMIT_MSG=Update CFA notes"
if not "%~1"=="" set "COMMIT_MSG=%~1"

echo.
echo === CFA notes: one-click GitHub upload ===
echo Repository: %CD%
echo.

git --version >nul 2>nul
if errorlevel 1 (
  echo ERROR: Git is not available. Install Git for Windows first.
  goto fail
)

git rev-parse --is-inside-work-tree >nul 2>nul
if errorlevel 1 (
  echo ERROR: This folder is not a Git repository.
  goto fail
)

git remote get-url origin >nul 2>nul
if errorlevel 1 (
  echo ERROR: Git remote "origin" is not configured.
  echo Run this once if needed:
  echo   git remote add origin https://github.com/guai6mmt/CFA-notes.git
  goto fail
)

for /f "usebackq delims=" %%B in (`git branch --show-current`) do set "BRANCH=%%B"
if not defined BRANCH (
  echo ERROR: Git is in detached HEAD state. Check out the branch you want to upload first.
  goto fail
)

if exist ".git\MERGE_HEAD" (
  echo ERROR: A merge is in progress. Finish or abort it before uploading.
  goto fail
)
if exist ".git\rebase-merge" (
  echo ERROR: A rebase is in progress. Finish or abort it before uploading.
  goto fail
)
if exist ".git\rebase-apply" (
  echo ERROR: A rebase is in progress. Finish or abort it before uploading.
  goto fail
)

echo [1/4] Staging local changes...
git add -A
if errorlevel 1 (
  echo ERROR: git add failed.
  goto fail
)

echo.
git -c core.quotepath=false status --short

git diff --cached --quiet
if errorlevel 2 (
  echo ERROR: git diff failed.
  goto fail
)

if errorlevel 1 (
  echo.
  echo [2/4] Creating commit...
  git commit -m "%COMMIT_MSG%"
  if errorlevel 1 (
    echo ERROR: git commit failed.
    goto fail
  )
) else (
  echo.
  echo [2/4] No local changes to commit.
)

echo.
echo [3/4] Pulling latest remote changes with rebase...
git pull --rebase origin "%BRANCH%"
if errorlevel 1 (
  echo ERROR: git pull --rebase failed.
  echo If Git reports conflicts, resolve them, then run:
  echo   git rebase --continue
  echo After that, run this bat again.
  goto fail
)

echo.
echo [4/4] Pushing to GitHub...
git push -u origin "%BRANCH%"
if errorlevel 1 (
  echo ERROR: git push failed.
  echo If GitHub asks for login, sign in through Git Credential Manager and run again.
  goto fail
)

echo.
echo SUCCESS: Uploaded to GitHub branch "%BRANCH%".
goto success

:fail
echo.
echo Upload did not finish. Read the error message above.
echo.
pause
endlocal
exit /b 1

:success
echo.
pause
endlocal
exit /b 0
