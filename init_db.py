from database import init_db, create_default_user, create_default_rules

init_db()
create_default_user()
create_default_rules()

print("Database initialized!")