# Waste Management System

## Project-Overview

The Waste Management System is a Django-based web application designed to enhance
efficiency in waste management and promote environmental sustainability. 
This application allows users to track waste collection and  manage recycling processes.


## Features

- **User Registration and Login: Secure user authentication system.**
- **Waste Collection Tracking: Users can track waste collection and disposal/recycling.**
- **Recycling Management: Information and management tools for recycling processes.**  




## Technology Stack
- **Backend: Django (Python)** 
- **Database: Postgresql** 
- **Frontend: HTML, CSS**
- **Dependency Management: Poetry**


## Getting Started

These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes.

## Prerequisites
- **Python 3.8+** 
- **Poetry (for dependency management)** 
- **Django 4.2+**

## Installation

### 1.Clone the repository
- **git clone https://github.com/yourusername/WasteManagement.git**
- **cd** WasteManagement

### 2.Set up a Poetry environment
```bash
    poetry shell
    poetry install
```

### 3.Initialize the database
```bash
python manage.py migrate
```

### 4.Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### 5.Run the development server
```bash
python manage.py runserver
```

### 6.Access the application
- **Open your web browser and navigate to http://127.0.0.1:8000/.**

## Testing
```bash
python manage.py test
```

## License
- **This project is licensed under the MIT License.**


### Versioning
- ** This application is at version 0.1.0 and subjected to future changes.**
- 