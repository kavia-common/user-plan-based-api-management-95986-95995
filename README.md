# user-plan-based-api-management-95986-95995

## Plan-Based API Backend

A FastAPI backend that manages user authentication (with JWT), user CRUD, plan CRUD, plan assignment, and exposes resource endpoints whose response changes depending on the requesting user's assigned plan.

- **Register/Login:** `/auth/register`, `/auth/login`
- **JWT-protected routes** (require `Authorization: Bearer <token>` in requests):
    - `/users/me`
    - `/users`
    - `/plans`
    - `/assign-plan`
    - `/resource` (plan-aware API endpoint)

Set up `.env` as described in `plan_based_api_backend/.env.example`.