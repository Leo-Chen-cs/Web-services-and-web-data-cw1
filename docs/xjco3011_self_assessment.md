# XJCO3011 Self-Assessment Checklist

This note maps the project to the coursework brief and highlights likely strengths and remaining risks before the oral exam.

## Clear Strengths

- Full relational CRUD is implemented for `teams`, `players`, and `matches`.
- The API exposes more than the minimum endpoint count and includes five analytics endpoints.
- Authentication is implemented with JWT access tokens and hashed passwords.
- Swagger UI and ReDoc are generated automatically, and PDF documentation is included in `docs/`.
- A technical report PDF is included and contains architecture rationale, testing, limitations, and a GenAI declaration.
- The repository contains visible commit history and a public GitHub remote.
- The code now includes stronger validation for password quality, match consistency, sort parameters, and duplicate updates.
- Security posture is improved through controlled CORS defaults, secure response headers, and automatic password-hash upgrading.
- Automated tests cover both success paths and edge cases for auth, CRUD, analytics, and validation regressions.

## Rubric-Based Honest Assessment

- `60-69` should now be comfortably achievable from the codebase quality alone because the project is runnable, documented, tested, and better validated.
- `70-79` is realistic if the oral presentation is clear and the demo is smooth, because the project is modular, has multiple advanced analytics features, and now demonstrates stronger engineering discipline.
- `80+` is possible but not guaranteed from code alone. That band also depends on highly polished oral delivery, stronger originality, and being able to discuss trade-offs with confidence.
- `90+` is unlikely without genuinely novel research-style features, stronger external integration/deployment polish, and a more exceptional presentation narrative.

## Remaining Risks To Watch In The Oral Exam

- The current visible commit history is still fairly short, so you should be ready to explain your actual development process clearly.
- If the examiners strongly value external deployment, local execution plus docs may still be weaker than a live hosted instance.
- The PDF report and API PDF were produced earlier, so mention the latest hardening changes during the demo even if they are not reflected word-for-word in those PDFs.

## Demo Talking Points

- Start with the relational model and explain why teams, players, and matches justify SQL.
- Show JWT login, then one protected write endpoint.
- Show one CRUD flow plus one analytics flow.
- Mention the validation and security improvements added after testing, especially password hashing compatibility, strict error handling, and safer query validation.
- Explicitly reference the README, API PDF, technical report PDF, slides, and the GenAI declaration.
