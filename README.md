
# Auto-CV

Auto-CV is a powerful Django-based web application that enables users to generate personalized Curriculum Vitae (CV) and cover letters tailored to specific job descriptions. Leveraging the capabilities of OpenAI's API and advanced prompt engineering, Auto-CV streamlines the resume creation process, ensuring each document is professionally crafted to meet individual career goals and job requirements.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Steps](#setup-steps)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Google OAuth Setup](#google-oauth-setup)
  - [OpenAI API Key](#openai-api-key)
- [Usage](#usage)
  - [Running the Server](#running-the-server)
  - [Using the Application](#using-the-application)
- [Project Structure](#project-structure)
- [Templates](#templates)
- [Testing](#testing)
- [License](#license)

## Features

- **User Authentication:** Secure user registration and login using Google OAuth via `django-allauth`.
- **Profile Management:** Users can create and edit their profiles, including personal information, education, and work experience.
- **Document Generation:** Generate professional CVs and cover letters in LaTeX format, tailored to specific job descriptions.
- **LaTeX Compilation:** Convert generated LaTeX code into downloadable PDF documents using `pdflatex`.
- **OpenAI Integration:** Utilize OpenAI's API for advanced prompt engineering to ensure high-quality, personalized documents.
- **Responsive Design:** User-friendly interface optimized for various devices and screen sizes.
- **Admin Interface:** Manage users, profiles, and generated documents through Django's robust admin panel.

## Technologies Used

- **Backend:** Django 4.2.16
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Django Allauth (Google OAuth)
- **Database:** SQLite
- **APIs:** OpenAI API
- **Document Processing:** LaTeX, pdflatex
- **Other Libraries:** Pydantic, dotenv

## Installation

### Prerequisites

Before setting up Auto-CV, ensure you have the following installed on your system:

- **Python 3.8+**
- **pip** (Python package installer)
- **virtualenv** (Recommended for creating a virtual environment)
- **LaTeX Distribution:** Ensure `pdflatex` is installed and accessible in your system's PATH.
  - **For Windows:** Install [MiKTeX](https://miktex.org/download)
  - **For macOS:** Install [MacTeX](https://www.tug.org/mactex/)
  - **For Linux:** Install TeX Live (`sudo apt-get install texlive-full`)

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/auto-cv.git
   cd auto-cv
   ```

2. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser (Optional)**

   To access Django's admin interface:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://127.0.0.1:8000/`.

## Configuration

### Environment Variables

Auto-CV requires several environment variables for configuration. Create a `.env` file in the root directory and add the following variables:

```env
# .env

# Django Settings
SECRET_KEY=your_django_secret_key
DEBUG=True  # Set to False in production

# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your_google_oauth_client_id
GOOGLE_OAUTH_SECRET=your_google_oauth_secret
```

*Ensure that the `.env` file is excluded from version control to protect sensitive information.*

### Google OAuth Setup

1. **Create a Google Cloud Project**

   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.

2. **Configure OAuth Consent Screen**

   - Navigate to **APIs & Services > OAuth consent screen**.
   - Configure the consent screen with required details.

3. **Create OAuth Credentials**

   - Go to **APIs & Services > Credentials**.
   - Click on **Create Credentials > OAuth client ID**.
   - Select **Web application**.
   - Set the **Authorized redirect URIs** to `http://127.0.0.1:8000/accounts/google/login/callback/` (adjust based on your deployment).
   - Save and note the **Client ID** and **Client Secret**.

4. **Update `.env` File**

   Add the obtained **Client ID** and **Client Secret** to your `.env` file:

   ```env
   GOOGLE_OAUTH_CLIENT_ID=your_google_oauth_client_id
   GOOGLE_OAUTH_SECRET=your_google_oauth_secret
   ```

### OpenAI API Key

1. **Obtain API Key**

   - Sign up or log in to your [OpenAI account](https://platform.openai.com/).
   - Navigate to the API section and generate a new API key.

2. **Update `.env` File**

   Add the **OpenAI API Key** to your `.env` file:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

### Running the Server

Ensure your virtual environment is activated and all dependencies are installed. Then, run:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

### Using the Application

1. **Sign Up / Log In**

   - Click on the **Sign Up** or **Log In** button.
   - Authenticate using your Google account.

2. **Complete Your Profile**

   - Navigate to **Edit Profile**.
   - Fill in your personal information, education, and work experience.
   - Save your profile.

3. **Generate Documents**

   - Go to **Generate Documents**.
   - Enter the job description for which you are applying.
   - Select whether to generate a CV, a cover letter, or both.
   - Submit the form.

4. **View and Download Generated Documents**

   - After generation, navigate to **Documents**.
   - View the generated LaTeX code and a preview of the PDF.
   - Download the PDF files as needed.

## Project Structure

Understanding the project structure is essential for navigating and extending the application. Below is an overview of the main components:

```
auto-cv/
├── core/
│   ├── admin.py            # Admin interface configurations
│   ├── apps.py             # App configuration
│   ├── forms.py            # Django forms for user input
│   ├── models.py           # Database models
│   ├── signals.py          # Signal handlers for user profile creation
│   ├── templatetags/
│   │   └── custom_filters.py # Custom template filters
│   ├── templates/
│   │   └── core/
│   │       ├── view_profile.html
│   │       ├── edit_profile.html
│   │       ├── generate_documents.html
│   │       ├── document_list.html
│   │       └── render_latex.html
│   ├── tests.py            # Unit tests
│   ├── urls.py             # URL routing for the core app
│   ├── utils.py            # Utility functions
│   ├── views.py            # View functions handling HTTP requests
│   └── prompts.py          # Prompt templates for OpenAI
├── cv_app/
│   ├── __init__.py
│   ├── asgi.py             # ASGI configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Project-level URL configurations
│   └── wsgi.py             # WSGI configuration
├── manage.py               # Django's command-line utility
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (excluded from version control)
└── README.md               # Project documentation
```

### Explanation of Key Components

- **core/**: The main application directory containing all the core functionalities.
  - **models.py**: Defines the database schema with models like `UserProfile`, `Education`, `Experience`, and `Generation`.
  - **forms.py**: Contains Django forms and formsets for user input and profile management.
  - **views.py**: Handles HTTP requests and orchestrates the logic for profile viewing/editing, document generation, and PDF handling.
  - **templates/core/**: HTML templates for rendering the frontend pages.
  - **admin.py**: Configures the Django admin interface for managing

 models.
  - **signals.py**: Automatically creates and updates user profiles upon user creation and sign-up via Google OAuth.
  - **utils.py**: Utility functions for processing user data, escaping LaTeX characters, formatting information for prompts, and handling LaTeX compilation.
  - **prompts.py**: Contains the prompt templates used to interact with the OpenAI API for generating CVs and cover letters.
  - **templatetags/custom_filters.py**: Custom template filters used within Django templates.
  - **tests.py**: Unit tests ensuring the reliability of functionalities like job detail extraction and document generation.

- **cv_app/**: The project-level directory containing configurations.
  - **settings.py**: Centralized configuration for the Django project, including installed apps, middleware, database settings, authentication backends, and logging.
  - **urls.py**: Routes URLs to the appropriate views, including admin and core app URLs.
  - **asgi.py** and **wsgi.py**: ASGI and WSGI configurations for deploying the application.

- **manage.py**: Django's command-line utility for administrative tasks like running the server, applying migrations, and executing tests.

- **requirements.txt**: Lists all Python dependencies required to run the application.

- **.env**: Stores sensitive environment variables like secret keys and API keys (should be excluded from version control).

## Templates

Auto-CV uses LaTeX templates for generating CVs and cover letters. These templates are defined within the `core/templates.py` file and can be customized to fit your design preferences.

- **CV Template (`cv_template`)**: Defines the structure and styling of the generated CV. It includes sections like Professional Summary, Education, Professional Experience, Skills, and a Flexible Section for Projects or Publications.

- **Cover Letter Template (`cover_letter_template`)**: Defines the layout and formatting of the generated cover letter. It includes sections for contact information, salutation, body paragraphs, and closing remarks.

### Customizing Templates

To customize the LaTeX templates:

1. **Locate the Templates**

   Open the `core/templates.py` file where the `cv_template` and `cover_letter_template` are defined.

2. **Modify the LaTeX Code**

   Adjust the LaTeX code to change the layout, fonts, sections, or any other stylistic elements as per your requirements.

3. **Save Changes**

   After modifying the templates, save the file. The changes will reflect the next time documents are generated.

*Ensure that any modifications maintain valid LaTeX syntax to prevent compilation errors.*

## Testing

Auto-CV includes unit tests to ensure the reliability of key functionalities.

### Running Tests

To execute the tests, run the following command:

```bash
python manage.py test
```

This command runs all tests within the `core` application, verifying components like job detail extraction and document generation.

### Writing Tests

Tests are written using Django's built-in testing framework. To add more tests:

1. **Open `core/tests.py`**

2. **Define Test Cases**

   Create new test classes inheriting from `django.test.TestCase` and define methods to test specific functionalities.

3. **Run Tests**

   Use the `python manage.py test` command to execute your tests and ensure they pass.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
