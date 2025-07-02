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

## Usage

### Admin Configuration

1. **Create a Fundraiser**: Set up basic info, grid size, and customize content
2. **Configure Content Type**: Define what each square represents (Animal, Prize, Item, etc.)
3. **Set Contact Information**: Configure contact URLs and messaging
4. **Manage Squares**: Add photos, names, and descriptions for each square
5. **Track Progress**: Monitor sponsorship progress and manage sales

### Customization Options

Each fundraiser can be customized with:
- **Content Type**: What squares represent (e.g., "Animal", "Prize", "Scholarship")
- **Square Label**: What to call individual squares (e.g., "Square", "Spot", "Entry")  
- **Collection Name**: What to call the overall collection (e.g., "Playlist", "Gallery", "List")
- **Song/Content Contributions**: Enable/disable optional content contributions from sponsors
- **Contact Text**: Custom messaging to encourage participation
- **Contact URL**: Link to Facebook, email, or contact form (supports facebook.com or https://facebook.com)
- **Contact Button Text**: Customize call-to-action button text
- **Success Message**: Thank you message for supporters

### Public Features

1. **Browse Active Fundraisers**: View all available fundraising campaigns
2. **Explore Grids**: Interactive grid showing available and sponsored squares
3. **View Collections**: See contributed items/songs/content (if applicable)
4. **Contact Integration**: Direct links to sponsor squares via configured contact methods

### Admin Features

- **Dashboard**: Overview of all fundraisers with status badges (Active, Inactive, Archived)
- **Square Management**: Edit individual squares with photos, details, and optional song contributions
- **Winner Drawing**: Random selection tools with complete history tracking
- **Data Export**: Multiple CSV export options (playlist/collection data, full grid, purchasers list)
- **Progress Tracking**: Real-time sponsorship statistics with visual progress bars
- **Archive Management**: Archive completed fundraisers and permanently delete archived ones
- **Smart Image Cropping**: Intelligent auto-cropping that focuses on important areas of photos
- **URL Validation**: Automatic protocol handling for contact URLs

## Examples

This platform can be used for various fundraising purposes:

- **Animal Shelter**: Sponsor animals in need of homes
- **School Fundraiser**: Win prizes while supporting education
- **Community Garden**: Sponsor garden plots or plants
- **Music Fundraiser**: Create collaborative playlists while raising funds
- **Art Project**: Sponsor pieces of a community mural
- **Sports Team**: Support equipment purchases with team member sponsorships

## Technical Details

- **Framework**: Flask with PostgreSQL
- **Core Technologies**: SQLAlchemy ORM, Flask-Login, Flask-Migrate, Flask-WTF, Pillow
- **Frontend**: Bootstrap 5, JavaScript, responsive CSS with animations
- **Deployment**: Docker containerization with environment-based configuration
- **Image Processing**: Smart cropping with Pillow, automatic thumbnail generation
- **Security**: CSRF protection, secure admin authentication, input validation
- **File Structure**:

```
square-game-fundraiser/
├── app/
│   ├── models.py           # Database models
│   ├── forms.py           # WTForms definitions  
│   ├── routes/            # Application routes
│   └── utils/             # Helper utilities
├── templates/             # Jinja2 templates
├── static/
│   ├── css/              # Styles
│   ├── js/               # JavaScript
│   └── uploads/          # Uploaded images
├── migrations/           # Database migrations
└── docker-compose.yml   # Container configuration
```

## Configuration

Key configuration options in the fundraiser setup:

- **Grid Size**: Rows x Columns (cannot be changed after creation)
- **Content Type**: Type of items in squares (e.g., "Animal", "Prize", "Item")
- **Terminology**: How to refer to squares and collections
- **Song/Content Contributions**: Enable/disable content contributions per fundraiser
- **Contact Integration**: URLs and messaging for sponsorship contact (auto-protocol handling)
- **Visual Customization**: Photos and descriptions for each square
- **Smart Image Cropping**: Automatic intelligent cropping for better photo display
- **Archive/Delete**: Archive completed fundraisers, delete only archived ones

## API

The application includes a REST API for:
- Fundraiser progress data
- Square details and images
- Dynamic content loading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues or questions, please contact us via the GitHub repository.

## Recent Updates

- **Enhanced Song/Content Contributions**: Flexible system for collecting songs, books, or any content type
- **Smart Image Cropping**: Intelligent auto-cropping that focuses on important areas of photos
- **Delete Functionality**: Safely delete archived fundraisers with double confirmation
- **URL Protocol Handling**: Automatic https:// prefix for contact URLs
- **Improved UI/UX**: Hover effects, animations, and better visual feedback
- **Generic Platform**: Fully customizable for any type of square game fundraiser

---

Made with ❤️ for fundraising success 