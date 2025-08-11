# Database Migration Guide

This project will automatically create the necessary tables at FastAPI app startup using SQLAlchemy's `Base.metadata.create_all()`.

**First Time Setup:**
- Ensure your database is empty or has no conflicting table names.
- The following tables will be created: `users`, `plans`, `user_plans`.

**Manual Migrations:**
- For schema changes, use tools like Alembic or drop/recreate the tables as needed.
- For production consider integrating Alembic for migrations.
