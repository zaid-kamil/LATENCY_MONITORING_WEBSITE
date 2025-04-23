# Latency Monitoring Website

This project is a Django-based web application that allows users to monitor the latency and availability of websites. It features a dashboard for managing websites, viewing monitoring data, and scheduling tasks.

## Features

- **User Dashboard**: View and manage the list of websites being monitored.
- **Notifications**: View notifications related to website performance.
- **Website Management**:
  - Add new websites for monitoring.
  - View latency and status information for websites.
  - Edit or delete existing websites.
- **Feedback and Issues**:
  - Submit feedback and view existing feedback.
  - Report issues related to the monitoring service.
- **Task Scheduling**:
  - Schedule monitoring tasks for websites using Celery and Django-Celery-Beat.
  - Run tasks manually.
- **Contact and Subscription**:
  - Contact form for reaching out to the team.
  - Subscribe to receive updates.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zaid-kamil/LATENCY_MONITORING_WEBSITE.git
   cd LATENCY_MONITORING_WEBSITE
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

### URLs

The application provides the following URLs for navigation:

- **Dashboard**: `/dashboard/` - View the user dashboard.
- **Feedback**:
  - `/feedback/` - Submit new feedback.
  - `/feedback/` - View existing feedback.
- **Issues**: `/issue/` - Submit a new issue.
- **Notifications**: `/notification/` - View notifications.
- **Website Management**:
  - `/website/new/` - Add a new website for monitoring.
  - `/website/<id>/view/` - View details of a monitored website.
  - `/website/<id>/edit/` - Edit details of an existing website.
  - `/website/<id>/delete/` - Delete a monitored website.
- **About**: `/about/` - About the application.
- **Services**: `/services/` - Information about services provided.
- **Contact**: `/contact/` - Contact form for reaching out.
- **Subscription**: `/subscriber/` - Subscribe to updates.
- **Run Tasks**: `/run/task/` - Run a monitoring task manually.
- **Schedule Tasks**: `/schedule/task/` - Schedule monitoring tasks.

### Views

- **Dashboard View**: Displays the list of websites monitored by the logged-in user.
- **Notification View**: Renders the notifications page.
- **Website Views**:
  - Add, edit, delete, and view monitoring details of websites.
  - View latency and status information.
- **Feedback Views**:
  - Create and view feedback entries.
- **Task Management**:
  - Schedule monitoring tasks based on user-defined intervals.
  - Run tasks manually.
- **Contact and Subscription**:
  - Send a message using the contact form.
  - Subscribe to updates using the subscription form.

## Technology Stack

- **Backend**: Django, Django-Celery-Beat
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default)
- **Task Queue**: Celery

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries, please contact [zaid-kamil](https://github.com/zaid-kamil).

### special instruction for celery

```
install gevent and eventlet using conda
```
conda install -c conda-forge gevent -y
```

### start redis server using WSL in windows
```
redis-server
```
### run the django server
```
python manage.py runserver
```

### start celery worker
```
celery -A config worker --pool=solo -l INFO
```

### start celery beat
```
celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

