# Project: dropbox

## Overview
This project, “Dropbox_lite,” is a simplified version of a file-hosting service, echoing core features of Dropbox. The primary goal of this project is to teach you how to handle file uploads, downloads, user authentication, sharing links, and basic syncing across multiple devices.

### Architecture and Design Rationale
• The system is divided into logical modules (Core, Auth, Files, Sync, and Sharing) to keep functionality separated and maintainable.  
• Python (3.8+) is used as the programming language, providing a robust ecosystem.  
• Flask or FastAPI serves as the web framework to handle HTTP endpoints, chosen for simplicity and clarity.  
• A relational or NoSQL database (e.g., Postgres, MySQL, or MongoDB) stores user information and metadata.  
• Local storage (or an S3-like storage) manages file content.  
• Optional Twisted can be used for asynchronous operations in the syncing engine to handle concurrent file updates efficiently.

### Key Technologies and Concepts
• Flask/FastAPI for RESTful endpoints.  
• Database for persistent data storage.  
• Local or cloud-based file storage.  
• User authentication and authorization using session management or JWT tokens.  
• File version control and conflict resolution logic for multi-device syncing.  
• Public or user-to-user link sharing for flexibility.

---

## Core
The Core module is the foundation of the project. It initializes and runs the server, loads configurations, and provides utility functions like database URI assembly. It is critical for setting up the environment and ensuring all other modules can be plugged in smoothly.

### Task: Create App
Responsible for creating and configuring the Flask/FastAPI application. This includes registering blueprints or routers for each module.

• Inputs: Configuration parameters (optional), references to module blueprints/routers.  
• Outputs: A Flask/FastAPI app object ready to run.  
• Expected Behavior: Initialize app with the correct routes, configuration, and potential middleware (e.g., CORS, session handling).

Conceptual steps might include:  
1. Instantiate the web framework application object.  
2. Link authentication, file handling, sync, and sharing routes.  
3. Load configuration into the application context.  

<details>
<summary>Hint: General pattern for Create App</summary>

1. Initialize the framework object (e.g., Flask or FastAPI).  
2. Register blueprints/routers for each module.  
3. Configure app settings (e.g., database connections, secret keys).  
4. Return the initialized application object.  

</details>

### Task: Run App
Handles actually starting the server on a specified host and port. It may also integrate optional Twisted or Gunicorn for production-level concurrency.

• Inputs: The app object, host, port, optional concurrency parameters.  
• Outputs: Running web server listening on the specified network interface.  
• Expected Behavior: Listens for incoming requests, routes them appropriately.  

Conceptual steps might include:  
1. Read environment variables or use defaults for host/port.  
2. Determine if running in development or production mode.  
3. Start the Flask/FastAPI app with the chosen server mechanism.  

<details>
<summary>Hint: General pattern for Run App</summary>

1. Define host, port, and debug settings.  
2. If using Flask’s built-in server, call app.run(host, port, debug).  
3. If using Twisted or Gunicorn, create a service or worker pointing to your app instance.  

</details>

### Task: Load Config
Retrieves necessary environment variables, merges them with defaults, and creates a cohesive configuration object or dictionary.

• Inputs: Environment variables, default settings.  
• Outputs: A dictionary or object with the final configuration.  
• Expected Behavior: Successfully loads required environment variables (e.g., DB credentials, secret keys), sets defaults if not found.

Conceptual steps might include:  
1. Check for environment variables (e.g., using os.environ).  
2. Merge the environment variables with default values.  
3. Validate essential configs (like DB URI) to ensure they are set.  

<details>
<summary>Hint: General pattern for Load Config</summary>

1. Initialize a config dictionary with default values.  
2. For each required environment variable, update the dictionary if found.  
3. Validate the final dictionary to ensure all necessary keys are present.  

</details>

### Task: Get Db Uri
Constructs and returns the database connection string used by the application.

• Inputs: Configuration data with DB host, port, user, password, database name.  
• Outputs: A string (e.g., “postgresql://user:password@host:port/dbname”).  
• Expected Behavior: Returns a valid URI that, when used, allows a successful database connection.

Conceptual steps might include:  
1. Retrieve database parameters from the loaded config.  
2. Validate components (e.g., no missing username).  
3. Construct the string in the supported format.  

<details>
<summary>Hint: General pattern for Get Db Uri</summary>

1. Retrieve host, port, user, password, db name from config.  
2. Construct a URI (e.g., “postgresql://{user}:{password}@{host}:{port}/{dbname}”).  
3. Return the URI.  

</details>

---

## Auth
The Auth module deals with user signup, login, logout, and verification. It interfaces with the database to store and validate user credentials and tokens/sessions. This module is fundamental to controlling application access and ensuring security.

### Task: Signup Endpoint
Registers a new user in the system. Typically expects a username and password in the request.

• Inputs: HTTP request (e.g., JSON with “username” and “password”).  
• Outputs: Success or error messages indicating sign-up status.  
• Expected Behavior: Creates a new user record if validations pass, returns an indication of success.

Conceptual steps might include:  
1. Validate input fields (username, password).  
2. Pass to create_user to insert into DB with a hashed password.  
3. Return a status indicating success or error.  

<details>
<summary>Hint: General pattern for Signup Endpoint</summary>

1. Parse username and password from request.  
2. Perform validations (e.g., password length, uniqueness of username).  
3. Call create_user(username, password).  
4. Return an HTTP response indicating success or failure.  

</details>

### Task: Login Endpoint
Handles user authentication, establishing a session or returning a token.

• Inputs: HTTP request (e.g., JSON with “username” and “password”).  
• Outputs: A session cookie or a JWT token, plus success/error messages.  
• Expected Behavior: Validates credentials, starts a session or generates a token on success.

Conceptual steps might include:  
1. Parse input data.  
2. Verify user credentials with verify_user.  
3. On success, generate a session or JWT token.  
4. Return token or set cookie.  

<details>
<summary>Hint: General pattern for Login Endpoint</summary>

1. Parse credentials.  
2. Call verify_user(username, password).  
3. If valid, return session or token data. Else, return error.  

</details>

### Task: Logout Endpoint
Logs the user out by invalidating the session or token.

• Inputs: The current session or token.  
• Outputs: Confirmation the session/token is invalidated.  
• Expected Behavior: The user cannot make further authenticated requests without logging in again.

Conceptual steps might include:  
1. Retrieve session info or token.  
2. Mark it as invalid in the server/session store.  
3. Return a success response.  

<details>
<summary>Hint: General pattern for Logout Endpoint</summary>

1. Obtain user session or token from request.  
2. Invalidate that session or token in your authentication store.  
3. Response with a success message.  

</details>

### Task: Create User(username, password)
A service-level function that actually registers a new user in the database, hashing the password.

• Inputs: Plaintext username and password.  
• Outputs: A user record insertion result or success indicator.  
• Expected Behavior: Stores a hashed password, not the plaintext, for security.

Conceptual steps might include:  
1. Hash the password using a secure algorithm (e.g., bcrypt).  
2. Insert the new user record into the DB.  
3. Return success/failure result.  

<details>
<summary>Hint: General pattern for Create User(username, password)</summary>

1. Apply a hashing function on the password (e.g., bcrypt.hashpw()).  
2. Construct a query to insert into “users” table.  
3. Return an indication of success (user ID or a boolean).  

</details>

### Task: Verify User(username, password)
Checks that the provided credentials match a stored user record.

• Inputs: Plaintext username and password.  
• Outputs: User data if valid, or an error/None if invalid.  
• Expected Behavior: Ensures that the hashed password matches the provided password.

Conceptual steps might include:  
1. Query the DB for the user by username.  
2. Compare the stored hashed password with the provided one using the hashing library.  
3. Return user object if valid or None otherwise.  

<details>
<summary>Hint: General pattern for Verify User(username, password)</summary>

1. Fetch stored hashed password for user from DB.  
2. Use a hashing tool to compare plaintext + salt with the stored hash.  
3. Return user object if match succeeds, otherwise return None.  

</details>

---

## Files
The Files module manages operations like uploading, downloading, listing, and storing file metadata. It connects with either a local or remote storage solution and updates the database with the necessary file/folder organization data.

### Task: Upload File Endpoint(request)
Accepts a file upload from the client, calls the file service to store the file bytes and metadata.

• Inputs: HTTP request with file data and optional folder information.  
• Outputs: File metadata and status of the upload.  
• Expected Behavior: Successfully stores file content and updates the database with metadata.

Conceptual steps might include:  
1. Parse the uploaded file object from the request.  
2. Confirm the user’s authentication/authorization to upload.  
3. Call store_file to save bytes and record metadata.  
4. Return success response with file metadata (e.g., file ID).  

<details>
<summary>Hint: General pattern for Upload File Endpoint(request)</summary>

1. Extract file from the incoming form-data or request body.  
2. Validate user permissions.  
3. Call store_file(user_id, file_obj, folder_id).  
4. Return the newly created file ID or similar metadata.  

</details>

### Task: Download File Endpoint(file Id)
Retrieves the requested file from storage and streams it back to the client.

• Inputs: file_id in the request path or query parameter.  
• Outputs: The raw file data (binary) or an error if unauthorized.  
• Expected Behavior: Sends the correct file or returns an error if the user is not allowed to access it.

Conceptual steps might include:  
1. Validate user’s access rights to the file.  
2. Call fetch_file(file_id) to retrieve the file data.  
3. Stream or return the file contents in the response.  

<details>
<summary>Hint: General pattern for Download File Endpoint(file Id)</summary>

1. Extract file_id.  
2. Check user ownership or permission.  
3. Fetch file bytes from storage.  
4. Return a file response with correct headers.  

</details>

### Task: List Files Endpoint(folder Id)
Displays the files and subfolders within a given folder for the authenticated user.

• Inputs: folder_id in the request path or query.  
• Outputs: A structured list of file/folder metadata.  
• Expected Behavior: Returns all files/folders that the user can access within the specified parent folder.

Conceptual steps might include:  
1. Verify that user can access the folder.  
2. Call list_user_files to retrieve the metadata.  
3. Return a JSON response with the file/folder structure.  

<details>
<summary>Hint: General pattern for List Files Endpoint(folder Id)</summary>

1. Extract folder_id from request.  
2. Check permissions for the folder.  
3. Retrieve file/folder metadata from DB.  
4. Return them in a structured JSON format.  

</details>

### Task: Store File(user Id, file Obj, folder Id)
Handles the actual storage of the file bytes on the filesystem or remote storage, as well as updating metadata in the database.

• Inputs: user_id, the file object (file bytes, filename), folder_id.  
• Outputs: The metadata record or a success indicator.  
• Expected Behavior: Properly saves the file data to storage and records file metadata (e.g., name, size, location).

Conceptual steps might include:  
1. Generate a unique ID or path for the file.  
2. Write the file bytes to local or cloud storage.  
3. Insert a record in the database associating the file with the user and folder.  

<details>
<summary>Hint: General pattern for Store File(user Id, file Obj, folder Id)</summary>

1. Generate a random ID or path for the file.  
2. Perform the actual write to disk or S3-like storage.  
3. Store the record (file name, size, path, user ID, folder ID) in DB.  

</details>

### Task: Fetch File(file Id)
Retrieves file data and metadata if the user is authorized.

• Inputs: file_id.  
• Outputs: The file bytes or an error if not found or unauthorized.  
• Expected Behavior: Locates the file path/storage key in metadata, reads the file from storage, returns the raw data.

Conceptual steps might include:  
1. Look up file metadata in the DB.  
2. Verify permission for the requesting user.  
3. Fetch the actual file bytes from local or remote storage.  

<details>
<summary>Hint: General pattern for Fetch File(file Id)</summary>

1. Query DB for file record.  
2. Validate ownership or permission.  
3. Read the file from the stored location.  
4. Return file bytes.  

</details>

### Task: List User Files(user Id, folder Id)
Collects and returns all file/folder entries belonging to a user in a specific folder.

• Inputs: user_id, folder_id.  
• Outputs: A list of metadata objects for each file or folder.  
• Expected Behavior: Provides a structured representation of the user’s directory, enabling easy navigation.

Conceptual steps might include:  
1. Query the DB for all items matching user_id and folder_id.  
2. Return the set of file and folder metadata in a structured format.  

<details>
<summary>Hint: General pattern for List User Files(user Id, folder Id)</summary>

1. Construct a database query filtering by user_id and parent folder_id.  
2. Return a list or JSON object with file/folder details.  

</details>

---

## Sync
The Sync module handles basic version tracking and conflict resolution. It helps synchronize files across multiple devices, ensuring that changes are propagated appropriately.

### Task: Init Sync Endpoint(request)
Kicks off synchronization for a client, returning files changed since the user’s last sync.

• Inputs: HTTP request (containing last sync timestamp or version info).  
• Outputs: List of updated files and possibly a reference to track the sync.  
• Expected Behavior: Provides the client with all relative changes so they can update their local copies.

Conceptual steps might include:  
1. Parse the user’s last sync timestamp.  
2. Use get_updated_files to retrieve a list of changed files.  
3. Return the changes to the client.  

<details>
<summary>Hint: General pattern for Init Sync Endpoint(request)</summary>

1. Extract user’s last sync timestamp from request data.  
2. Call get_updated_files(user_id, last_sync_ts).  
3. Send back the list of changed or new files.  

</details>

### Task: Resolve Conflict Endpoint(request)
Allows the user to pick a version or handle a conflict that arises when multiple updates happen at once.

• Inputs: HTTP request containing conflict details (local vs remote versions).  
• Outputs: Confirmation of which version was chosen or how it was merged.  
• Expected Behavior: Addresses the conflict, merges or discards changes as appropriate, updates the file record.

Conceptual steps might include:  
1. Retrieve local and remote file versions from the request.  
2. Call detect_conflicts or a dedicated function to see if conflict resolution is needed.  
3. Save the user’s choice (e.g., keep local, keep remote, or merge).  

<details>
<summary>Hint: General pattern for Resolve Conflict Endpoint(request)</summary>

1. Parse conflict details from the request.  
2. Compare local vs remote versions.  
3. Update the record in DB or storage with the chosen version.  

</details>

### Task: Get Updated Files(user Id, last Sync Ts)
Queries for all files that have changed since the provided timestamp.

• Inputs: user_id, last_sync_ts.  
• Outputs: A list of file metadata representing new or updated files.  
• Expected Behavior: Efficiently fetch only what has changed to minimize data transfer and processing.

Conceptual steps might include:  
1. Query the file metadata table for records updated after last_sync_ts.  
2. Filter by user_id to ensure only the user’s files are returned.  
3. Return the relevant metadata.  

<details>
<summary>Hint: General pattern for Get Updated Files(user Id, last Sync Ts)</summary>

1. Construct a query on file metadata with updated_at > last_sync_ts.  
2. Return the list of updated entries.  

</details>

### Task: Detect Conflicts(local Version, remote Version)
Checks whether a conflict exists between the local and remote versions and, if so, merges or flags it for user intervention.

• Inputs: local_version, remote_version.  
• Outputs: A result indicating if there is a conflict, and the recommended action.  
• Expected Behavior: Compares versions and determines conflict (e.g., both updated after last sync) or no conflict.

Conceptual steps might include:  
1. Compare last_modified timestamps or version counters.  
2. Decide if both versions changed concurrently.  
3. Either mark as conflict or automatically merge (if trivial).  

<details>
<summary>Hint: General pattern for Detect Conflicts(local Version, remote Version)</summary>

1. Check timestamps of both local and remote versions.  
2. If both are changed and out of sync, declare a conflict.  
3. Otherwise, prefer the newer version or automatically merge changes.  

</details>

---

## Sharing
The Sharing module enables users to create share links for files and folders, revoke those links, and validate tokens for external access.

### Task: Create Share Link Endpoint(file Id)
Generates a public or restricted link for a file/folder, allowing others to access it.

• Inputs: file_id in the request.  
• Outputs: A URL or token representing the share link.  
• Expected Behavior: Confirms the user’s right to share, then returns a link that grants appropriate file access.

Conceptual steps might include:  
1. Verify the file_id belongs to or is shared by the requesting user.  
2. Call create_share_link(user_id, file_id, permission_level).  
3. Return the newly generated link or token.  

<details>
<summary>Hint: General pattern for Create Share Link Endpoint(file Id)</summary>

1. Validate user ownership of file.  
2. Generate a unique share token or link.  
3. Store it in the DB or memory with associated permissions.  
4. Return the link/token.  

</details>

### Task: Revoke Share Link Endpoint(share Id)
Cancels an existing share link to prevent further access.

• Inputs: share_id referencing the link/token.  
• Outputs: Confirmation that the share link was removed.  
• Expected Behavior: Removes the share link from the system, making it invalid.

Conceptual steps might include:  
1. Locate the share link record using share_id.  
2. Validate the user’s rights to revoke it.  
3. Delete or mark the link as inactive.  

<details>
<summary>Hint: General pattern for Revoke Share Link Endpoint(share Id)</summary>

1. Fetch share record by share_id.  
2. Check user permissions.  
3. Delete or expire the record.  
4. Return a success message.  

</details>

### Task: Create Share Link(user Id, file Id, permission Level)
Service-level logic that generates the token/URL, storing it for future validation.

• Inputs: user_id, file_id, permission_level.  
• Outputs: A share link or token with an associated record.  
• Expected Behavior: Links a user, file, and access permissions into a secure token or URL.

Conceptual steps might include:  
1. Verify correct user ownership of file.  
2. Create a unique token with permissions embedded.  
3. Store link data (file_id, user_id, permission_level) for validation.  

<details>
<summary>Hint: General pattern for Create Share Link(user Id, file Id, permission Level)</summary>

1. Generate a secure random token.  
2. Store share config in DB (token, user_id, file_id, permission_level, expiry).  
3. Return the token or constructed URL.  

</details>

### Task: Validate Share Token(token)
Checks if a provided share token is valid and returns the associated file if authorized.

• Inputs: token (often from a URL query parameter).  
• Outputs: File metadata or an error if invalid/expired.  
• Expected Behavior: Grants or denies access based on the token’s validity and permission settings.

Conceptual steps might include:  
1. Look up the share record by token.  
2. Check if token is valid and not expired.  
3. Return file metadata or error accordingly.  

<details>
<summary>Hint: General pattern for Validate Share Token(token)</summary>

1. Query DB for the token.  
2. Confirm it hasn’t expired.  
3. Return file details or an unauthorized error.  

</details>

---

## Testing and Validation
To ensure the application works correctly, you should test each endpoint (Auth, Files, Sync, Sharing) independently and then as an integrated system. For instance:  
• Unit test individual functions (create_user, verify_user, store_file, etc.) using mock database connections.  
• Integration test endpoints with a test database or a carefully controlled environment.  
• Check that user permissions are enforced by attempting unauthorized actions (e.g., uploading to another user’s folder).  
• Validate file version conflicts by simulating concurrent edits.  
• Verify share links’ correctness and expiration logic.

Edge cases to consider:  
• Very large file uploads or corrupted file data.  
• Multiple devices syncing the same file within seconds.  
• Expired or invalid share links access attempts.  
• Database connection loss or configuration errors.

---

## Common Pitfalls and Troubleshooting
1. Not hashing passwords or incorrectly verifying them, creating a security risk.  
2. Neglecting file ownership checks, allowing unauthorized access to files.  
3. Incorrect database URI or uninitialized environment variables leading to connection failures.  
4. Overlooking concurrency conflict handling in sync, leading to lost updates.  
5. Forgetting to revoke share links, resulting in perpetual access for outsiders.

Solving typical errors often involves:  
• Double-checking environment variables.  
• Confirming database table structures.  
• Reviewing permission checks for file ownership or sharing.  
• Implementing robust logging to track issues during request handling.

---

## Next Steps and Extensions
• Implement full text search on filenames and metadata for easier file discovery.  
• Integrate advanced access control models (e.g., read-only links).  
• Add a UI (web or mobile) for a richer user experience.  
• Expand collaboration features like folder sharing with granular permissions.  
• Improve the sync engine with automated conflict resolution merges (e.g., for text files).  
• Integrate external authentication providers (OAuth, SSO).  

By carefully following this design and architecture, you will have a clean, modular codebase mimicking essential Dropbox-like functionalities. Focus on testing each component thoroughly and progressively add features to extend the platform’s capabilities.