---
phase: 1
slug: foundation-auth
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2025-03-23
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8+ with pytest-asyncio (backend), vitest (frontend) |
| **Config file** | `backend/pytest.ini`, `frontend/vitest.config.ts` |
| **Quick run command** | `pytest backend/tests/ -x -v` (< 10s), `npm test` (< 15s) |
| **Full suite command** | `pytest backend/tests/ -v --cov=app && npm run test:ci` |
| **Estimated runtime** | ~45 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_{module}.py -x -v` or `npm test -- {pattern}`
- **After every plan wave:** Run full suite command
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 20 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | BACK-08 | smoke | `ls backend/ frontend/` | ❌ W0 | ⬜ pending |
| 01-01-02 | 01 | 1 | FRNT-03 | smoke | `cd frontend && npm run dev` | ❌ W0 | ⬜ pending |
| 01-01-03 | 01 | 1 | BACK-01, BACK-02 | integration | `pytest tests/test_db.py -x` | ❌ W0 | ⬜ pending |
| 01-02-01 | 02 | 1 | BACK-03, BACK-04 | unit | `pytest tests/test_auth.py::test_password_hashing -x` | ❌ W0 | ⬜ pending |
| 01-02-02 | 02 | 1 | AUTH-01 | unit | `pytest tests/test_auth.py::test_register -x` | ❌ W0 | ⬜ pending |
| 01-02-03 | 02 | 1 | AUTH-01 | unit | `pytest tests/test_auth.py::test_register_duplicate -x` | ❌ W0 | ⬜ pending |
| 01-03-01 | 03 | 1 | AUTH-02 | unit | `pytest tests/test_auth.py::test_login_success -x` | ❌ W0 | ⬜ pending |
| 01-03-02 | 03 | 1 | AUTH-02 | unit | `pytest tests/test_auth.py::test_login_sets_cookie -x` | ❌ W0 | ⬜ pending |
| 01-03-03 | 03 | 1 | AUTH-04 | integration | `pytest tests/test_auth.py::test_token_expiration -x` | ❌ W0 | ⬜ pending |
| 01-04-01 | 04 | 1 | AUTH-03 | unit | `pytest tests/test_auth.py::test_logout_clears_cookie -x` | ❌ W0 | ⬜ pending |
| 01-04-02 | 04 | 1 | FRNT-04, FRNT-05 | integration | `npm test -- Auth` | ❌ W0 | ⬜ pending |
| 01-05-01 | 05 | 1 | ALL | e2e | `pytest tests/test_e2e.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `backend/tests/conftest.py` — async client fixture, test DB setup
- [ ] `backend/tests/test_auth.py` — covers AUTH-01, AUTH-02, AUTH-03, AUTH-04
- [ ] `backend/tests/test_db.py` — covers BACK-02 (MongoDB connection)
- [ ] `backend/pytest.ini` — pytest configuration with asyncio mode
- [ ] `frontend/src/test/setup.ts` — vitest configuration with React Testing Library
- [ ] `frontend/src/test/auth.test.tsx` — TanStack Query hooks testing
- [ ] Framework install: `pip install pytest pytest-asyncio httpx` (backend)
- [ ] Framework install: `npm install -D vitest @testing-library/react @testing-library/jest-dom` (frontend)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Cross-origin cookie flow | AUTH-02 | Browser-specific CORS handling | 1. Start backend on :8000, frontend on :5173 2. Login from frontend 3. Verify cookie visible in DevTools 4. Refresh page 5. Verify still authenticated |
| Session persistence across refresh | AUTH-02 | Requires browser context | Same as above, verify user stays logged in after F5 |
| UI responsive design | FRNT-03 | Visual/layout testing | 1. Open app at various viewport sizes 2. Verify forms are usable 3. Check mobile/desktop breakpoints |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 20s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
