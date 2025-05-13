# Create and activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install

# Create necessary directories
mkdir -p logs
mkdir -p frontend/src/components
mkdir -p frontend/src/pages

Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "To start the backend server, run: uvicorn app.main:app --reload" -ForegroundColor Yellow
Write-Host "To start the frontend development server, run: cd frontend && npm run dev" -ForegroundColor Yellow 