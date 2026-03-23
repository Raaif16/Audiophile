---
phase: quick
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/app/database.py
  - backend/app/config.py
  - backend/.env.example
  - frontend/src/App.tsx
  - frontend/src/App.css
autonomous: true
requirements:
  - QUICK-01: Update MongoDB configuration for local development
  - QUICK-02: Improve frontend responsiveness and interactivity
must_haves:
  truths:
    - Backend properly closes async MongoDB connections on shutdown
    - Backend handles MongoDB connection failures gracefully
    - Frontend has responsive navigation with mobile support
    - Frontend loading states are visually polished
  artifacts:
    - path: backend/app/database.py
      provides: Fixed async MongoDB close with retry logic
      min_lines: 60
    - path: backend/.env.example
      provides: Updated environment template with better comments
    - path: frontend/src/App.tsx
      provides: Responsive navigation and improved loading states
    - path: frontend/src/App.css
      provides: Mobile-responsive navbar styles
---

<objective>
Fix MongoDB async close deprecation and add connection resilience, plus improve frontend responsiveness with mobile-friendly navigation and polished loading states.

Purpose: Resolve technical debt (PyMongo Async deprecation warning) and improve user experience across device sizes.
Output: Updated database module with proper async close, improved CSS for mobile responsiveness.
</objective>

<execution_context>
@/Users/raaif/.config/opencode/get-shit-done/workflows/execute-plan.md
</execution_context>

<context>
@backend/app/database.py
@backend/app/config.py
@backend/.env.example
@frontend/src/App.tsx
@frontend/src/App.css

**Technical Debt from STATE.md:**
- PyMongo Async deprecation warning for client.close() - needs await in close_db()

**Current Architecture:**
- FastAPI with Beanie ODM using PyMongo Async (Motor deprecated May 2026)
- React 19 + Vite frontend with TanStack Query
- httpOnly cookie authentication working
</context>

<tasks>

<task type="auto">
  <name>Task 1: Fix MongoDB async close and add connection resilience</name>
  <files>backend/app/database.py, backend/.env.example</files>
  <action>
    Fix the close_db() function to properly await client.close() for PyMongo Async compatibility.
    Add connection retry logic with exponential backoff in init_db() for local MongoDB development.
    Update .env.example with inline comments explaining MongoDB URL format options (localhost, Docker, etc.).
    
    Changes to make:
    1. Change `client.close()` to `await client.close()` in close_db()
    2. Add try/except with retry logic (3 attempts, 1s delay) in init_db() for connection failures
    3. Add logging for connection attempts and failures
    4. Update .env.example with better documentation for MONGODB_URL options
  </action>
  <verify>
    <automated>cd /Users/raaif/Desktop/Demo/backend && python -c "import ast; ast.parse(open('app/database.py').read())" && echo "Syntax OK"</automated>
  </verify>
  <done>close_db() uses await, init_db() has retry logic with logging, .env.example has clear comments</done>
</task>

<task type="auto">
  <name>Task 2: Add mobile-responsive navbar and improved loading UI</name>
  <files>frontend/src/App.tsx, frontend/src/App.css</files>
  <action>
    Update App.tsx navbar to be responsive with a hamburger menu for mobile.
    Replace simple "Loading..." text with a styled loading spinner.
    Add responsive CSS for navbar collapse on small screens.
    
    Changes to make:
    1. Add mobile menu state (useState) and hamburger button in App.tsx
    2. Create responsive navbar that collapses to hamburger menu on screens < 768px
    3. Replace "Loading..." with styled spinner animation
    4. Add smooth transitions for menu open/close
    5. Ensure all auth buttons remain accessible on mobile
  </action>
  <verify>
    <automated>cd /Users/raaif/Desktop/Demo/frontend && npm run build 2>&1 | grep -q "error TS" && echo "TypeScript errors found" || echo "Build OK"</automated>
  </verify>
  <done>Navbar collapses to hamburger on mobile, loading spinner replaces text, transitions are smooth</done>
</task>

</tasks>

<verification>
- Backend database.py has `await client.close()`
- Backend init_db() has retry logic with try/except
- Backend logs connection attempts
- Frontend navbar has hamburger menu on mobile (< 768px)
- Frontend has styled loading spinner instead of plain text
- Frontend build completes without TypeScript errors
</verification>

<success_criteria>
- MongoDB connections close properly on shutdown (no deprecation warnings)
- Connection failures show clear retry attempts in logs
- Mobile users see hamburger menu and can access all auth actions
- Loading states are visually polished and responsive
</success_criteria>

<output>
After completion, work is complete - no SUMMARY needed for quick tasks.
</output>
