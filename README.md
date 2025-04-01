# Building Dropbox_lite (MVP) from Scratch

This tutorial walks you through creating a minimal viable product (MVP) called **Dropbox_lite** using Python and Flask. It demonstrates basic file hosting, syncing, user authentication, and simple sharing capabilities. By the end, you’ll have a working skeleton of a Dropbox-like service that includes user sign-up/login, file upload/download, basic folder structures, simple conflict resolution for syncing, and share links.

---

## 1. Overview

In this tutorial, you will:

1. Set up a Python/Flask application (or FastAPI if you prefer) with the necessary routes for authentication, file management, syncing, and sharing.
2. Configure an environment (database, storage paths, etc.).
3. Implement minimal logic for each module so you can see how the pieces fit together.
4. Test the MVP with a small example that ensures your code is functional (upload, sync, share, etc.).
5. Learn about potential pitfalls and best practices along the way.

---

## 2. Project Structure

Below is the high-level directory structure for our Dropbox_lite MVP. You can create these folders and files as a starter skeleton. Each section of this tutorial will reference these files:

```
dropbox_lite/
├── app.py
├── config.py
├── auth/
│   ├── auth_controller.py
│   └── auth_service.py
├── files/
│   ├── file_controller.py
│   └── file_service.py
├── sync/
│   ├── sync_controller.py
│   └── sync_service.py
├── sharing/
│   ├── share_controller.py
│   └── share_service.py
├── utils/
│   ├── logger.py
│   └── auth_helpers.py
└── examples/
    └── basic_sync_demo/
        ├── demo_app.py
        ├── demo_config.py
        └── README.md
```

### What Each Directory/File Does

- **app.py**: Main entry point. Creates and runs the Flask server, ties together all controllers (routes).
- **config.py**: Configuration logic (DB connection settings, environment variables, file paths).
- **auth***: User signup, login, and logout. Password hashing and verification.
- **files***: Handling file uploads, downloads, folder structures, and metadata.
- **sync***: Basic file versioning and simple conflict resolution when multiple clients sync.
- **sharing***: Generates and validates share links or direct shares.
- **utils***: General-purpose utilities (logging, authentication helpers).
- **examples/basic_sync_demo***: Demonstrates a minimal working example using the modules above.

---

## 3. Prerequisites and Setup

### 3.1 Requirements

- Python 3.8+  
- A package manager (pip, Poetry, etc.)  
- A relational (Postgres, MySQL) or NoSQL database (MongoDB) of your choice  
- Local filesystem or an S3-like storage service for file data  

### 3.2 Virtual Environment

It’s a best practice to keep your Python dependencies isolated:

```bash
python3 -m venv venv
source venv/bin/activate  # (Linux/Mac)
# or
venv\Scripts\activate  # (Windows)
```

### 3.3 Install Necessary Packages

Install Flask, a database driver, and other libraries you might need:

```bash
pip install flask sqlalchemy bcrypt
# or
pip install fastapi uvicorn sqlalchemy bcrypt
```

Depending on your chosen DB, install the appropriate driver (e.g., `psycopg2` for Postgres, `pymongo` for MongoDB). For asynchronous features, you may also install Twisted if you want to experiment with real-time syncing:

```bash
pip install twisted
```

---

## 4. Step-by-Step Implementation

### 4.1 config.py

**Goal**: Store and manage environment variables or file-based settings such as the database URI, storage paths, or debug flags.

<details open>
<summary>Example config.py</summary>

```python
# config.py

import os

def load_config():
    """Gathers environment variables and merges them with default values."""
    config = {
        "DB_URI": os.getenv("DB_URI", "sqlite:///dropbox_lite.db"),
        "STORAGE_PATH": os.getenv("STORAGE_PATH", "./storage"),
        "DEBUG": os.getenv("DEBUG", "False").lower() == "true",
        "SECRET_KEY": os.getenv("SECRET_KEY", "supersecretkey"),
    }
    return config

def get_db_uri(config):
    """Returns the database connection string from the loaded config."""
    return config["DB_URI"]
```
</details>

- **Potential Pitfall**: Use environment variables for sensitive info (e.g., secret keys, DB credentials). Don’t commit secrets to version control.

---

### 4.2 app.py

**Goal**: Create a Flask (or FastAPI) application, tie it to your controllers (routes), and run the server.

<details>
<summary>Example app.py</summary>

```python
# app.py

from flask import Flask
from config import load_config
from auth.auth_controller import auth_bp
from files.file_controller import file_bp
from sync.sync_controller import sync_bp
from sharing.share_controller import share_bp

def create_app():
    """Configures Flask, registers blueprints, and returns the app instance."""
    config = load_config()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config["SECRET_KEY"]

    # Register Blueprints (controllers)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(file_bp, url_prefix="/files")
    app.register_blueprint(sync_bp, url_prefix="/sync")
    app.register_blueprint(share_bp, url_prefix="/share")

    return app

def run_app():
    """Starts the Flask development server on a specified port."""
    app = create_app()
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    run_app()
```
</details>

- **Best Practice**: Use `Blueprint` for modular code in Flask.
- **Pitfall**: Avoid running a production site with Flask’s built-in dev server. Use Gunicorn or similar in production.

---

### 4.3 Authentication (auth/)

User signup, login, password hashing, and session or token creation. For simplicity, we’ll store users in a database table `users` with a username and hashed password.

#### 4.3.1 auth_service.py

<details>
<summary>Example auth_service.py</summary>

```python
# auth/auth_service.py

import bcrypt
# from your_db_connection import db  # hypothetical DB session/connection helper

def create_user(username, password):
    """
    Inserts a new user record with a hashed password.
    Returns True if created successfully, False if username is taken.
    """
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Example pseudo-DB operation:
    # result = db.insert("users", {"username": username, "password": hashed_pw})
    # if not successful, handle duplication or errors
    return True

def verify_user(username, password):
    """
    Checks credentials against DB, returns user data if correct or None if invalid.
    """
    # Example retrieval from DB
    # user_record = db.query("SELECT * FROM users WHERE username = ?", [username])
    user_record = {
        "id": 1,
        "username": "testuser",
        "password": bcrypt.hashpw(b"testpassword", bcrypt.gensalt()),
    }
    if user_record and bcrypt.checkpw(password.encode('utf-8'),
                                      user_record["password"]):
        return user_record
    return None
```
</details>

- **Pitfall**: Never store passwords in plaintext. Always use a salted hash.
- **Pitfall**: Rate-limit login attempts to mitigate brute-force attacks.

#### 4.3.2 auth_controller.py

<details>
<summary>Example auth_controller.py</summary>

```python
# auth/auth_controller.py

from flask import Blueprint, request, jsonify, session
from auth.auth_service import create_user, verify_user

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup_endpoint():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if create_user(username, password):
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"error": "User creation failed"}), 400

@auth_bp.route("/login", methods=["POST"])
def login_endpoint():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user_record = verify_user(username, password)
    if user_record:
        # Use server-side session or JWT
        session["user_id"] = user_record["id"]
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
def logout_endpoint():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"}), 200
```
</details>

- **Best Practice**: Use secure session cookies (HTTPS only). Consider JWT if building a stateless API.
- **Pitfall**: Make sure to sanitize input to prevent injection attacks.

---

### 4.4 File Management (files/)

Here we handle uploading/downloading files, storing them locally or on a cloud service, plus maintaining metadata in the database.

#### 4.4.1 file_service.py

<details>
<summary>Example file_service.py</summary>

```python
# files/file_service.py

import os
import uuid
from config import load_config

def store_file(user_id, file_obj, folder_id=None):
    """
    Saves file bytes + updates DB metadata.
    Returns file_id if successful.
    """
    config = load_config()
    storage_path = config["STORAGE_PATH"]

    # Generate a unique file name
    unique_filename = str(uuid.uuid4()) + "_" + file_obj.filename
    file_path = os.path.join(storage_path, unique_filename)

    # Write the file to disk
    file_obj.save(file_path)

    # Insert metadata into DB (pseudo-code):
    # db.insert("files", {
    #     "user_id": user_id,
    #     "filename": file_obj.filename,
    #     "storage_name": unique_filename,
    #     "folder_id": folder_id
    # })

    file_id = 123  # Suppose we get an ID from DB
    return file_id

def fetch_file(file_id):
    """
    Retrieves file bytes/metadata if user has access.
    Returns (file_path, original_filename) if found, else None.
    """
    # Pseudo-code to get metadata from DB
    # file_record = db.query("SELECT * FROM files WHERE id = ?", [file_id])
    file_record = {
        "storage_name": "some-unique-file-uuid.jpg",
        "filename": "original.jpg"
    }
    if not file_record:
        return None

    config = load_config()
    storage_path = config["STORAGE_PATH"]
    file_path = os.path.join(storage_path, file_record["storage_name"])
    return file_path, file_record["filename"]

def list_user_files(user_id, folder_id=None):
    """
    Returns a list of file/folder metadata for that user in a given folder.
    """
    # Example pseudo-DB query
    # files = db.query("SELECT * FROM files WHERE user_id = ? AND folder_id = ?", [user_id, folder_id])
    files = [
        {"id": 1, "filename": "doc1.txt", "folder_id": folder_id},
        {"id": 2, "filename": "photo.jpg", "folder_id": folder_id}
    ]
    return files
```
</details>

- **Pitfall**: Storing huge files in memory before saving can cause out-of-memory issues. Stream uploads if possible.
- **Pitfall**: Validate file types and size to avoid malicious uploads.

#### 4.4.2 file_controller.py

<details>
<summary>Example file_controller.py</summary>

```python
# files/file_controller.py

from flask import Blueprint, request, send_file, jsonify, session
from files.file_service import store_file, fetch_file, list_user_files

file_bp = Blueprint("file_bp", __name__)

@file_bp.route("/upload", methods=["POST"])
def upload_file_endpoint():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file_obj = request.files["file"]
    folder_id = request.form.get("folder_id")
    file_id = store_file(session["user_id"], file_obj, folder_id)
    return jsonify({"message": "File uploaded", "file_id": file_id}), 201

@file_bp.route("/download/<int:file_id>", methods=["GET"])
def download_file_endpoint(file_id):
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    fetched = fetch_file(file_id)
    if not fetched:
        return jsonify({"error": "File not found or unauthorized"}), 404

    file_path, original_filename = fetched
    return send_file(file_path, as_attachment=True, attachment_filename=original_filename)

@file_bp.route("/list", methods=["GET"])
def list_files_endpoint():
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    folder_id = request.args.get("folder_id")
    files = list_user_files(session["user_id"], folder_id)
    return jsonify(files), 200
```
</details>

---

### 4.5 Sync Logic (sync/)

This provides basic version tracking and conflict resolution. Full real-time syncing can be achieved via websockets or Twisted, but we’ll keep it simple for our MVP.

#### 4.5.1 sync_service.py

<details>
<summary>Example sync_service.py</summary>

```python
# sync/sync_service.py

def get_updated_files(user_id, last_sync_ts):
    """
    Fetches files changed after a certain timestamp.
    last_sync_ts can be stored in the client to detect changes.
    """
    # Pseudo-code:
    # changed_files = db.query("SELECT * FROM file_versions WHERE user_id = ? AND updated_at > ?", [user_id, last_sync_ts])
    changed_files = [
        {"file_id": 1, "version": 3, "updated_at": "2023-01-01 10:00"},
        {"file_id": 2, "version": 1, "updated_at": "2023-01-01 10:05"}
    ]
    return changed_files

def detect_conflicts(local_version, remote_version):
    """
    Determines if a conflict exists, merges or flags it.
    Return a dict describing the conflict or None if none.
    """
    # If local_version != remote_version, we have a conflict
    if local_version["version"] != remote_version["version"]:
        return {
            "conflict": True,
            "local_version": local_version,
            "remote_version": remote_version
        }
    return None
```
</details>

#### 4.5.2 sync_controller.py

<details>
<summary>Example sync_controller.py</summary>

```python
# sync/sync_controller.py

from flask import Blueprint, request, jsonify, session
from sync.sync_service import get_updated_files, detect_conflicts

sync_bp = Blueprint("sync_bp", __name__)

@sync_bp.route("/init", methods=["POST"])
def init_sync_endpoint():
    """
    When a client starts syncing, it sends its last_sync_ts and we return any changed files.
    """
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    last_sync_ts = data.get("last_sync_ts", "1970-01-01 00:00")
    changed_files = get_updated_files(session["user_id"], last_sync_ts)
    return jsonify({"changed_files": changed_files}), 200

@sync_bp.route("/resolve", methods=["POST"])
def resolve_conflict_endpoint():
    """
    Allows the client to indicate which version to keep if there's a conflict.
    """
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    local_version = data.get("local_version")
    remote_version = data.get("remote_version")

    conflict = detect_conflicts(local_version, remote_version)
    if conflict:
        # Decide on a conflict resolution strategy:
        # keep remote, keep local, or merge
        chosen_version = data.get("chosen_version", "remote")
        return jsonify({"status": "Conflict resolved", "chosen_version": chosen_version}), 200

    return jsonify({"status": "No conflict"}), 200
```
</details>

- **Best Practice**: Keep a version history to revert if needed.
- **Pitfall**: Conflict resolution is tricky. Try a strategy that’s simplest for your MVP (e.g., “last writer wins”).

---

### 4.6 Sharing (sharing/)

Lets users share files via public links or direct share with other users.

#### 4.6.1 share_service.py

<details>
<summary>Example share_service.py</summary>

```python
# sharing/share_service.py

import uuid

def create_share_link(user_id, file_id, permission_level="read"):
    """
    Generates a share link (token) for a file/folder with specified access (read/write).
    """
    token = str(uuid.uuid4())
    # Insert into DB: db.insert("shares", { user_id, file_id, token, permission_level })
    return token

def validate_share_token(token):
    """
    Checks if a token is valid, returns associated file or an error.
    """
    # Example DB lookup
    # share_record = db.query("SELECT * FROM shares WHERE token=?", [token])
    share_record = {
        "file_id": 1,
        "permission_level": "read"
    }
    if not share_record:
        return None
    return share_record
```
</details>

#### 4.6.2 share_controller.py

<details>
<summary>Example share_controller.py</summary>

```python
# sharing/share_controller.py

from flask import Blueprint, request, jsonify, session
from sharing.share_service import create_share_link, validate_share_token

share_bp = Blueprint("share_bp", __name__)

@share_bp.route("/create/<int:file_id>", methods=["POST"])
def create_share_link_endpoint(file_id):
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json or {}
    permission_level = data.get("permission_level", "read")
    token = create_share_link(session["user_id"], file_id, permission_level)
    return jsonify({"share_link": f"/share/access/{token}"}), 201

@share_bp.route("/access/<string:token>", methods=["GET"])
def access_share_link_endpoint(token):
    share_record = validate_share_token(token)
    if not share_record:
        return jsonify({"error": "Invalid or expired link"}), 404

    return jsonify({"file_id": share_record["file_id"], 
                    "permission": share_record["permission_level"]}), 200

@share_bp.route("/revoke/<string:token>", methods=["DELETE"])
def revoke_share_link_endpoint(token):
    if "user_id" not in session:
        return jsonify({"error": "Not authenticated"}), 401

    # Pseudo: db.delete("shares", { token })
    return jsonify({"status": "Share link revoked"}), 200
```
</details>

---

### 4.7 Utilities (utils/)

#### 4.7.1 logger.py

<details>
<summary>Example logger.py</summary>

```python
# utils/logger.py

def log_debug(message):
    print(f"[DEBUG] {message}")

def log_info(message):
    print(f"[INFO] {message}")

def log_error(message):
    print(f"[ERROR] {message}")
```
</details>

- **Pitfall**: For large-scale apps, use a dedicated logging library (e.g., `logging` module, Logstash, etc.).

#### 4.7.2 auth_helpers.py

<details>
<summary>Example auth_helpers.py</summary>

```python
# utils/auth_helpers.py

import bcrypt

def extract_user_id(token):
    """
    Parses a JWT or session data to find user ID.
    Placeholder for demonstration.
    """
    # Typically decode JWT and extract user_id
    return 1

def hash_password(password):
    """
    Creates a salted hash for password storage.
    Straight pass to bcrypt here.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_session_valid(user_id):
    """
    Verifies user's session validity. 
    For demonstration, always return True.
    """
    return True
```
</details>

---

## 5. Example: Basic Sync Demo

We will test our modules with a minimal Flask server that simulates file uploads and sync calls. In a real environment, you’d build a proper client or UI. This example just demonstrates that everything is wired up.

### 5.1 File Structure

```
examples/
└── basic_sync_demo/
    ├── demo_app.py
    ├── demo_config.py
    └── README.md
```

### 5.2 demo_config.py

<details>
<summary>Example demo_config.py</summary>

```python
# examples/basic_sync_demo/demo_config.py

import os

def load_demo_config():
    """
    Loads environment variables or sets defaults specifically for this demo.
    """
    return {
        "DB_URI": os.getenv("DEMO_DB_URI", "sqlite:///demo_dropbox_lite.db"),
        "STORAGE_PATH": os.getenv("DEMO_STORAGE_PATH", "./demo_storage"),
        "DEBUG": True,
        "SECRET_KEY": "demo_secret_key"
    }
```
</details>

### 5.3 demo_app.py

<details>
<summary>Example demo_app.py</summary>

```python
# examples/basic_sync_demo/demo_app.py

from flask import Flask, request
from auth.auth_controller import auth_bp
from files.file_controller import file_bp
from sync.sync_controller import sync_bp
from sharing.share_controller import share_bp
from demo_config import load_demo_config

def init_demo_app():
    """
    Configures the Flask app for demo, registers routes from Dropbox_lite modules.
    """
    config = load_demo_config()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config["SECRET_KEY"]
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(file_bp, url_prefix="/files")
    app.register_blueprint(sync_bp, url_prefix="/sync")
    app.register_blueprint(share_bp, url_prefix="/share")

    return app

def demo_upload_file(app):
    """
    Simple demonstration: start the server, then manually do a POST to /files/upload.
    This function could also show a direct request using 'requests' library if desired.
    """
    pass

def demo_sync_cycle(app):
    """
    Simulates a client sync request and prints server’s response.
    """
    pass

if __name__ == "__main__":
    demo_app = init_demo_app()
    demo_app.run(debug=True, port=5001)
```
</details>

### 5.4 README.md

<details>
<summary>Example README.md</summary>

```markdown
# Basic Sync Demo

This README helps you run the demo application for Dropbox_lite. 

1. Install Requirements
   ```bash
   pip install flask bcrypt
   ```
2. Run Demo App
   ```bash
   python demo_app.py
   ```
3. Create a User and Login
   - POST /auth/signup
   - POST /auth/login
4. Upload a File
   - POST /files/upload with a file form-data field called "file"
5. Sync
   - POST /sync/init with `last_sync_ts` to see updates
6. Sharing
   - POST /share/create/<file_id> to generate a link
7. Download
   - GET /files/download/<file_id>

Use an API testing tool (Postman, cURL, etc.) to make the above requests.
```
</details>

---

## 6. Potential Pitfalls & Best Practices

1. **Security**: Always hash passwords. Use HTTPS in production.  
2. **Concurrency**: Large file uploads or multiple sync operations can overwhelm memory or cause race conditions in versioning.  
3. **Database Migrations**: Handling schema changes over time.  
4. **File Storage**: Storing large files local vs. using a cloud (S3) can drastically affect performance and cost.  
5. **Conflict Resolution**: Decide on a strategy early—“last writer wins” or automatic merges.  
6. **Scalability**: This MVP is not production-ready. You’d need caching, load balancing, and advanced logging solutions for real-world scale.

---

## 7. Complete Your MVP

1. **Create the directory structure**: Follow the layout described.  
2. **Populate each file with the skeleton code**: Adjust for your database and environment.  
3. **Configure database**: Replace pseudo-code for DB operations with actual queries (SQLAlchemy, raw SQL, or ORM usage).  
4. **Test each endpoint**: Use Postman or cURL to confirm signup, login, upload, download, sharing, and sync.  
5. **Iterate**: Expand your conflict resolution, add better error handling, integrate a real asynchronous approach if desired (Twisted or websockets).  

Congratulations! You now have a minimal Dropbox_lite MVP that demonstrates core features—user auth, file handling, basic sync, and shareable links. Feel free to extend it with more robust real-time syncing, permission controls, or user interfaces as you grow your application.