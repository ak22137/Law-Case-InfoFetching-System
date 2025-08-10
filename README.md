# Law Case InfoFetching System




https://github.com/user-attachments/assets/123e8f4b-0c05-454c-a3c6-77bd959d6f7a




This project is a Court Dashboard web application designed to fetch, display, and manage law case information. It provides a user-friendly interface for viewing case details and demo data, and includes a scraper for gathering case information.

## Features
- Dashboard for viewing law case details
- Demo data for testing and demonstration
- Scraper to fetch case information
- SQLite database for storing queries
- HTML templates for UI rendering

## Project Structure
```
court_dashboard/
├── app.py                # Main Flask application
├── demo_data.py          # Demo data for testing
├── queries.db            # SQLite database
├── scraper.py            # Scraper for case info
├── templates/
│   ├── case_details.html # Case details page
│   └── index.html        # Dashboard home page
└── __pycache__/          # Python cache files
```

## Getting Started
1. **Install Requirements**
   - Ensure you have Python 3.11+ installed.
   - Install Flask: `pip install flask`
2. **Run the Application**
   - Navigate to the `court_dashboard` directory.
   - Start the app



: `python app.py`
3. **Access the Dashboard**
   - Open your browser and go to `http://localhost:5000`

## Usage
- View the dashboard and case details via the web interface.
- Use the scraper to fetch new case information.
- Demo data is available for testing purposes.

## License
This project is licensed under the MIT License.
