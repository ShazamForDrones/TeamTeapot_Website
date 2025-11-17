# Copilot Instructions for TeamTeapot_Website

## Project Overview
- This is a web application for Teapot TDT (Threat Detection Technology).
- The project is structured as a typical Flask app with `app.py` as the main entry point.
- Templates are in `templates/` (Jinja2: `base.html`, `dashboard.html`, `index.html`, `login.html`, `signup.html`).
- Static assets are in `static/` (CSS, JS, images).

## Key Files & Structure
- `app.py`: Main Flask application, routes, and server logic.
- `test.py`: Contains tests or scripts for validation (check for test conventions if expanding).
- `static/css/`: Stylesheets (`style.css`, `StyleDash.css`).
- `static/js/`: JavaScript (e.g., `sidebar.js` for UI logic).
- `templates/`: Jinja2 HTML templates for all pages.

## Developer Workflows
- **Run the app:**
  ```powershell
  python app.py
  ```
- **Testing:**
  ```powershell
  python test.py
  ```
- No build step is required; static files are served directly.

## Project Conventions
- Follows Flask's default structure: `app.py` for logic, `templates/` for views, `static/` for assets.
- Use Jinja2 templating in HTML files for dynamic content.
- Static files are referenced in templates using Flask's `url_for('static', filename='...')`.
- CSS/JS file naming is camelCase or lowercase with dashes/underscores.

## Integration & Dependencies
- Relies on Flask (check `app.py` for additional dependencies).
- No evidence of a requirements.txt or external service integration in the root—add if new dependencies are introduced.

## Patterns & Examples
- Route handlers are defined in `app.py`.
- Templates extend `base.html` for shared layout.
- Example static asset usage in templates:
  ```html
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  <script src="{{ url_for('static', filename='js/sidebar.js') }}"></script>
  ```

## Recommendations for AI Agents
- When adding new pages, create a template in `templates/` and a route in `app.py`.
- Place new CSS/JS in the appropriate static subfolder and reference via `url_for` in templates.
- Follow existing naming and structural conventions for consistency.
- If adding dependencies, document them and consider adding a `requirements.txt`.

---
Edit this file to update project-specific AI agent instructions as the codebase evolves.
