# Square Game Fundraiser - Homelab Deployment Script (PowerShell)
Write-Host "🚀 Square Game Fundraiser - Homelab Deployment" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker found" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Docker Compose is available
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose found" -ForegroundColor Green
} catch {
    try {
        docker compose version | Out-Null
        Write-Host "✅ Docker Compose (v2) found" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker Compose is not available." -ForegroundColor Red
        exit 1
    }
}

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    
    Write-Host ""
    Write-Host "🔧 IMPORTANT: Please edit the .env file with your secure passwords:" -ForegroundColor Cyan
    Write-Host "   - Change SECRET_KEY to a random string" -ForegroundColor White
    Write-Host "   - Change ADMIN_PASSWORD to a secure password" -ForegroundColor White
    Write-Host "   - Change POSTGRES_PASSWORD to a secure database password" -ForegroundColor White
    Write-Host "   - Update DATABASE_URL with the same POSTGRES_PASSWORD" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter after you've updated the .env file"
}

# Create necessary directories
Write-Host "📁 Creating required directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "static\uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "instance" | Out-Null

# Pull latest images
Write-Host "📦 Pulling Docker images..." -ForegroundColor Yellow
docker-compose pull

# Build and start services
Write-Host "🔨 Building and starting services..." -ForegroundColor Yellow
docker-compose up -d --build

# Wait for database to be ready
Write-Host "⏳ Waiting for database to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Run database migrations
Write-Host "🗃️  Running database migrations..." -ForegroundColor Yellow
docker-compose exec web flask db upgrade

# Show status
Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "🌐 Your fundraiser platform should be available at:" -ForegroundColor Cyan
Write-Host "   http://localhost:5000" -ForegroundColor White
Write-Host "   http://YOUR_SERVER_IP:5000" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Default admin login (update in .env file):" -ForegroundColor Cyan
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin" -ForegroundColor White
Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Cyan
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop services: docker-compose down" -ForegroundColor White
Write-Host "   Update app: docker-compose up -d --build" -ForegroundColor White
Write-Host "" 