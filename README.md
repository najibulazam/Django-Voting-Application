# 🗳️ Django Voting Application

A simple, responsive web-based voting platform built with Django and Bootstrap. Users can register using Student ID, email, nickname, log in, vote for candidates, and view real-time animated results with percentage bars.

---

## 🚀 Features

- ✅ Student registration with nickname, email & password
- ✅ Login with 7-digit Student ID and password
- ✅ Vote once per position (enforced at DB level)
- ✅ Clean Bootstrap 5 UI with dark mode toggle
- ✅ Real-time vote percentage display
- ✅ Animated result bars with winner highlight
- ✅ Admin panel for managing positions, candidates, votes
- ✅ Custom Django template filter for vote percentage
- ✅ Font Awesome icons integration
- ✅ Displays nickname in dashboard and votes list

---

## 📁 Project Structure

```
voting_project/
├── core/
│   ├── templates/core/         # HTML templates
│   ├── templatetags/           # Custom filters (e.g., vote_percentage)
│   ├── static/                 # Static files (CSS/JS/icons)
│   ├── forms.py                # Custom forms with validation and placeholders
│   ├── admin.py                # Model registration with nickname display
│   ├── models.py               # Position, Candidate, Vote, Profile
│   ├── views.py                # App logic
│   └── urls.py                 # App routing
├── voting_project/
│   └── settings.py             # Django settings
├── db.sqlite3                  # Default database
├── manage.py
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/najibulazam/Django-Voting-Application.git
cd Django-Voting-Application
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (admin access)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

---

## 🧪 Test Credentials

You can create a superuser to access the admin dashboard at `/admin`. Regular users can register via `/register` with Student ID, email, nickname, and password.

---

## 🔧 Custom Template Filters

Defined in `core/templatetags/math_filters.py`:

```python
@register.filter
def vote_percentage(votes, total):
    return (votes / total) * 100 if total > 0 else 0
```

Used in dashboard and result templates for safe percentage rendering.

---

## 📊 Admin Access

Once logged in as superuser, you can manage:

* Positions
* Candidates
* Votes (shows student ID and nickname)

---

## 🎨 UI Technologies

* Bootstrap 5
* Font Awesome (CDN)
* Responsive design with dark mode

---

## 🙌 Contributions

Pull requests are welcome! If you'd like to add features or fix bugs, feel free to fork the repo and submit a PR.

---

```
Let me know if you'd like a [badge section](f), [screenshots](f), or [GitHub Actions CI setup](f) added to this README.
```
