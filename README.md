# Expense Tracker

A modern, feature-rich desktop application for personal expense tracking with intuitive visualizations and robust data management.

## Features

- **Expense Management**
  - Add expenses with date, description, category, and amount
  - Automatic currency support (USD, EUR, INR, etc.)
  - Persistent data storage using CSV files
  - Real-time expense table updates

- **Category System**
  - Predefined categories (Food, Transport, etc.)
  - Create custom categories
  - Category-based expense tracking

- **Visual Analytics**
  - Interactive summary dashboard
  - Category-wise expense breakdown
  - Visual progress bars for spending distribution
  - Real-time total expense calculation

- **User Experience**
  - Modern dark theme UI
  - Responsive layout
  - Form validation and error handling
  - Cross-platform compatibility

## Technologies

- **Frontend**: 
  - Python Tkinter
  - ttk widgets
  - Custom theme styling

- **Backend**:
  - CSV data storage
  - File-based configuration
  - Data persistence layer

- **Tools**:
  - PIL/Pillow (for future icon support)
  - datetime for date handling
  - CSV module for data management

## Installation

### Prerequisites
- Python 3.6+
- Pillow library (for image support)

```bash
pip install Pillow
```

### Running the Application

Clone the repository:

```bash
git clone https://github.com/abhijjeeet/Expense-tracker.git
```

Navigate to project directory:

```bash
cd Expense-tracker
```

Run the application:

```bash
python main.py
```

## Usage

### First Launch
- Set your preferred currency when prompted
- Default categories are pre-loaded

### Adding Expenses
- Select date (default: current date)
- Enter description
- Choose category from dropdown
- Enter amount (positive numbers only)
- Click "Add Expense"

### Managing Categories
- Click "Create New Category" to add custom categories
- Categories persist between sessions

### Viewing Summary
- Click "View Summary" to see spending breakdown
- Interactive progress bars show category distribution
- Total expenses displayed in header

### Data Management
- Data automatically saved in `expenses.csv`
- Categories stored in `categories.txt`
- Currency preference stored in `currency.txt`

## File Structure

```
expense-tracker-pro/
├── main.py             # Main application code
├── expenses.csv        # Expense records
├── categories.txt      # Custom categories
├── currency.txt        # Currency preference
├── README.md           # Documentation
└── screenshot.png      # Application screenshot
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- Inspired by modern personal finance apps
- UI design influenced by Material Design principles
- Built with Python's Tkinter library

---
