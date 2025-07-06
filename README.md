# Square Game Fundraiser Platform

A flexible Flask-based web application for managing square grid fundraising games. Create interactive fundraising campaigns where supporters can sponsor squares in a grid, optionally contributing songs or other content to build collaborative collections. Administrators can fully customize the content type, terminology, and contact information to suit any fundraising purpose - from animal sponsorships to prize drawings to community projects.

## Features

- **Customizable Content**: Configure content type (Animal, Prize, Item, etc.), terminology, and messaging
- **Song/Content Contributions**: Optional feature to collect songs, book titles, or other content from sponsors
- **Public View**: Beautiful public-facing pages for viewing grids and collaborative collections
- **Admin Interface**: Complete admin panel for managing fundraisers, squares, and winners
- **Configurable Contact**: Editable contact URLs with automatic protocol handling (supports web, email, phone)
- **Data Export**: Export fundraiser data, playlists, and purchaser lists as CSV
- **Random Winner Drawing**: Built-in winner selection tools with full history tracking
- **Responsive Design**: Mobile-friendly interface with hover effects and animations
- **Smart Photo Management**: Upload and manage square images with intelligent auto-cropping
- **Archive & Delete**: Archive completed fundraisers and permanently delete archived ones
- **Progress Tracking**: Real-time visual progress bars showing sponsorship status

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/square-game-fundraiser.git
cd square-game-fundraiser
```

2. Copy the environment template:
```bash
cp env.example .env
```

3. Edit `.env` with your settings:
```bash
# Basic configuration
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password

# Database
POSTGRES_PASSWORD=your-db-password
```

4. Start the application:
```bash
docker compose up -d
```

5. Initialize the database:
```bash
docker compose exec web flask db upgrade
```

6. Access the application:
   - Public view: http://localhost:5000
   - Admin login: http://localhost:5000/admin/login

