---
phase: quick
plan: 2
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/app/dependencies.py
  - backend/app/routers/admin.py
  - backend/app/main.py
  - frontend/src/components/admin/AdminRoute.tsx
  - frontend/src/components/admin/AdminDashboard.tsx
  - frontend/src/pages/Admin.tsx
  - frontend/src/App.tsx
  - frontend/src/api/auth.ts
autonomous: true
requirements:
  - ADMIN-01
  - ADMIN-02
  - ADMIN-03
must_haves:
  truths:
    - Admin user exists with credentials admin@audiophile.com / admin123
    - Backend validates is_admin field on protected routes
    - /admin route is accessible only to admin users
    - Non-admin users are redirected from /admin
    - Admin panel displays admin dashboard UI
  artifacts:
    - path: backend/app/dependencies.py
      provides: require_admin dependency
      exports: ["require_admin"]
    - path: backend/app/routers/admin.py
      provides: Admin API endpoints
      exports: ["router"]
    - path: frontend/src/components/admin/AdminRoute.tsx
      provides: Protected route wrapper for admin routes
    - path: frontend/src/components/admin/AdminDashboard.tsx
      provides: Admin dashboard UI component
    - path: frontend/src/pages/Admin.tsx
      provides: Admin page component
  key_links:
    - from: frontend/src/App.tsx
      to: /admin route
      via: Route component with AdminRoute wrapper
    - from: AdminRoute.tsx
      to: useCurrentUser hook
      via: React Query auth state
    - from: backend/admin.py
      to: require_admin dependency
      via: FastAPI Depends()
---

<objective>
Create an admin panel with separate admin login and management capabilities.

Purpose: Allow admin users to access a protected admin interface for managing the application.
Output: Working /admin route accessible only to users with is_admin=true, with admin dashboard UI.
</objective>

<execution_context>
@/Users/raaif/.config/opencode/get-shit-done/workflows/execute-plan.md
@/Users/raaif/.config/opencode/get-shit-done/templates/summary.md
</execution_context>

<context>
@backend/app/dependencies.py
@backend/app/routers/auth.py
@backend/app/models/user.py
@frontend/src/App.tsx
@frontend/src/hooks/useAuth.ts
@frontend/src/api/auth.ts

## Key Interfaces

From backend User model:
```python
class User(Document):
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False  # Admin flag available
```

From frontend auth API:
```typescript
export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  created_at: string
  // Note: is_admin will be added
}
```

From useAuth hook:
```typescript
export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: getCurrentUser,
    retry: false,
  })
}
```

## Admin Credentials (pre-defined)
- Email: admin@audiophile.com
- Password: admin123
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add backend admin protection and ensure admin user exists</name>
  <files>backend/app/dependencies.py, backend/app/routers/admin.py, backend/app/main.py</files>
  <action>
    1. Add `require_admin` dependency to backend/app/dependencies.py:
       - Import get_current_user as a base
       - Create require_admin that checks current_user.is_admin
       - Return 403 Forbidden if not admin
    
    2. Create backend/app/routers/admin.py with:
       - GET /admin/users endpoint (list all users, admin only)
       - GET /admin/stats endpoint (basic stats, admin only)
       - All endpoints use require_admin dependency
    
    3. Update backend/app/main.py:
       - Include admin router with prefix /admin
       - Add startup event to ensure admin user exists:
         - Check if admin@audiophile.com exists
         - If not, create with username="admin", password="admin123", is_admin=true
         - Use hash_password from app.services
    
    4. Update UserResponse schema to include is_admin field (check/add to schemas.py if needed)
  </action>
  <verify>
    <automated>cd backend && python -c "from app.dependencies import require_admin; print('OK')"</automated>
  </verify>
  <done>
    - require_admin dependency exists and validates is_admin field
    - Admin router created with protected endpoints
    - Admin user auto-created on startup if missing
    - User schema includes is_admin in response
  </done>
</task>

<task type="auto">
  <name>Task 2: Create admin dashboard components and protected route</name>
  <files>frontend/src/components/admin/AdminRoute.tsx, frontend/src/components/admin/AdminDashboard.tsx, frontend/src/pages/Admin.tsx, frontend/src/api/auth.ts</files>
  <action>
    1. Update frontend/src/api/auth.ts:
       - Add is_admin to User interface
       - Add getAdminStats() and getAdminUsers() API functions
    
    2. Create frontend/src/components/admin/AdminRoute.tsx:
       - Accept children prop
       - Use useCurrentUser hook to check auth state
       - If loading: show loading spinner
       - If not logged in: redirect to /login
       - If logged in but not admin: redirect to /
       - If admin: render children
    
    3. Create frontend/src/components/admin/AdminDashboard.tsx:
       - Display "Admin Dashboard" header
       - Show admin user info (email, username)
       - Add placeholder sections for:
         - User Management (list users from API)
         - Product Management (placeholder)
         - Stats/Overview section
       - Style with existing CSS patterns from App.css
    
    4. Create frontend/src/pages/Admin.tsx:
       - Import AdminRoute wrapper
       - Import AdminDashboard component
       - Export Admin page component wrapped with AdminRoute
  </action>
  <verify>
    <automated>cd frontend && npm run build 2>&1 | head -20</automated>
  </verify>
  <done>
    - AdminRoute component protects admin routes
    - AdminDashboard displays admin UI with user management placeholder
    - Admin page combines route protection with dashboard
    - API functions for admin endpoints exist
  </done>
</task>

<task type="auto">
  <name>Task 3: Wire admin route into App and add navigation</name>
  <files>frontend/src/App.tsx</files>
  <action>
    1. Update frontend/src/App.tsx:
       - Import Admin page component
       - Add Route for /admin path rendering Admin component
       - Add "Admin" link in navbar (only visible when user.is_admin is true)
       - Style the admin link distinctly (e.g., different color or badge)
    
    2. Ensure admin link appears:
       - In desktop navbar between existing links and user section
       - In mobile menu when admin
       - Only when user?.is_admin === true
    
    3. Test flow:
       - Regular user: no admin link, /admin redirects to home
       - Admin user: sees admin link, can access /admin
  </action>
  <verify>
    <automated>cd frontend && npm run build 2>&1 | grep -E "(error|Error|failed)" || echo "Build successful"</automated>
  </verify>
  <done>
    - /admin route is registered in App.tsx
    - Admin link visible only to admin users in navbar
    - Build passes without errors
  </done>
</task>

</tasks>

<verification>
1. Backend startup creates admin user if missing
2. Admin endpoints return 403 for non-admin users
3. Frontend /admin route redirects non-admins to home
4. Admin link only visible to admin users
5. Admin can access dashboard and see user list
</verification>

<success_criteria>
- Admin user exists with email admin@audiophile.com and password admin123
- Backend has require_admin dependency protecting admin routes
- Frontend /admin route is protected and only accessible to admins
- Admin dashboard displays with user management section
- Regular users cannot see admin link or access /admin
</success_criteria>

<output>
After completion, create `.planning/quick/2-create-admin-panel-with-admin-login-and-management/2-SUMMARY.md`
</output>
