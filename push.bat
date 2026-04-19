@echo off
echo.
echo ========================================
echo  Pushing Starlogic Prediction Engine
echo ========================================
echo.
cd /d C:\Users\Allen\starlogic_prediction_engine
git add .
git commit -m %1
git push origin main
echo.
echo ========================================
echo  Railway will redeploy in ~2 minutes
echo ========================================
echo.
pause
