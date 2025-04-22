from app.backends.users.models import create_users_table, add_user

def initialize_db():
    """Initialize database and add an admin user if empty."""
    create_users_table()

    # Add default admin user (modify password in production)
    add_user("admin@xtrium.com", "SecurePass123")
    add_user("raghumathur", "xtr!um")

#if __name__ == "__main__":
#    initialize_db()
#    print("Database initialized.")