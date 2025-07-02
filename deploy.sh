#!/bin/bash

# Square Game Fundraiser - Homelab Deployment Script
echo "🚀 Square Game Fundraiser - Homelab Deployment"
echo "=============================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    
    echo ""
    echo "🔧 IMPORTANT: Please edit the .env file with your secure passwords:"
    echo "   - Change SECRET_KEY to a random string"
    echo "   - Change ADMIN_PASSWORD to a secure password"
    echo "   - Change POSTGRES_PASSWORD to a secure database password"
    echo "   - Update DATABASE_URL with the same POSTGRES_PASSWORD"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p static/uploads
mkdir -p instance

# Set proper permissions
echo "🔒 Setting directory permissions..."
chmod 755 static/uploads
chmod 755 instance

# Pull latest images
echo "📦 Pulling Docker images..."
docker-compose pull

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database to initialize..."
sleep 10

# Run database migrations
echo "🗃️  Running database migrations..."
docker-compose exec web flask db upgrade

# Show status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🌐 Your fundraiser platform should be available at:"
echo "   http://localhost:5000"
echo "   http://YOUR_SERVER_IP:5000"
echo ""
echo "🔑 Default admin login (update in .env file):"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Update app: docker-compose up -d --build"
echo "" 