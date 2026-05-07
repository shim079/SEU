# Activate virtual environment (if you have one)
# .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..."
pip install -r requirements.txt

Write-Host "Applying migrations..."
python manage.py migrate

Write-Host "Collecting static files..."
python manage.py collectstatic --noinput

Write-Host "Build complete!"