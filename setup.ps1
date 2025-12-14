# Pizza Bot Setup Script for Windows

Write-Host "Pizza Bot Setup Initiated..."

# Check for Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker is not installed. Please install Docker Desktop and try again." -ForegroundColor Red
    exit 1
}

# Check for Docker Compose
# Note: Modern Docker Desktop includes 'docker compose'. We'll check for the command availability.
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    # Fallback check for 'docker compose' subcommand if docker-compose standalone isn't found
    $dockerComposeCheck = docker compose version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker Compose is not installed. Please install Docker Desktop and try again." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Docker and Docker Compose found." -ForegroundColor Green

# Environment Configuration
if (-not (Test-Path .env)) {
    Write-Host ".env file not found. Creating from .env.example..."
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host ".env created. Please update it with your GROQ_API_KEY." -ForegroundColor Yellow
    } else {
        Write-Host ".env.example not found. Cannot create configuration." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host ".env file already exists."
}

# Build and Run
Write-Host "Building and starting containers..." -ForegroundColor Cyan
docker-compose up --build

Write-Host "Setup complete! Access the application at http://localhost:3000" -ForegroundColor Green
