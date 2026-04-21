import json
import os
import time

import jwt
import mysql.connector
import requests
from flask import Flask, jsonify, render_template_string, request
from jwt.algorithms import RSAAlgorithm


ISSUER = os.getenv("OIDC_ISSUER", "http://authentication-identity-server:8080/realms/realm_sv001")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "myapp")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "flask-app")
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI", "http://localhost:8085/secure")
MASTER_ISSUER = os.getenv("OIDC_MASTER_ISSUER", "http://authentication-identity-server:8080/realms/master")
LOCALHOST_ISSUER = os.getenv("OIDC_LOCALHOST_ISSUER", "http://localhost:8081/realms/master")
LOCALHOST_REALM_ISSUER = os.getenv("OIDC_LOCALHOST_REALM_ISSUER", "http://localhost:8081/realms/realm_sv001")
ALLOWED_ISSUERS = {
    ISSUER,
    MASTER_ISSUER,
    LOCALHOST_ISSUER,
    LOCALHOST_REALM_ISSUER,
    "http://authentication-identity-server:8080/auth/realms/master",
    "http://authentication-identity-server:8080/auth/realms/realm_sv001",
    "http://localhost:8081/auth/realms/master",
    "http://localhost:8081/auth/realms/realm_sv001",
}
DB_HOST = os.getenv("DB_HOST", "relational-database-server")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "studentdb")
STUDENTS_FILE = os.path.join(os.path.dirname(__file__), "students.json")


app = Flask(__name__)

_jwks_cache = None
_jwks_cache_time = 0.0


def get_jwks(issuer: str):
    global _jwks_cache, _jwks_cache_time
    now = time.time()
    if _jwks_cache is None or now - _jwks_cache_time > 600:
        jwks_issuer = issuer.replace(
            "http://localhost:8081",
            "http://authentication-identity-server:8080",
        )
        target_issuer = jwks_issuer if issuer.startswith("http://localhost:8081") else issuer
        response = requests.get(f"{target_issuer}/protocol/openid-connect/certs", timeout=5)
        response.raise_for_status()
        _jwks_cache = response.json()
        _jwks_cache_time = now
    return _jwks_cache


def verify_token(token: str):
    claims = jwt.decode(token, options={"verify_signature": False})
    issuer = claims.get("iss")
    if issuer not in ALLOWED_ISSUERS:
        raise ValueError(f"Unsupported issuer: {issuer}")

    header = jwt.get_unverified_header(token)
    jwks = get_jwks(issuer)
    signing_key = next(
        (key for key in jwks.get("keys", []) if key.get("kid") == header.get("kid")),
        None,
    )
    if signing_key is None:
        raise ValueError("Signing key not found")

    public_key = RSAAlgorithm.from_jwk(json.dumps(signing_key))
    return jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        options={"verify_aud": False},
        issuer=issuer,
    )


def exchange_authorization_code(code: str):
    # Reach token endpoint through container DNS so the backend can resolve it.
    internal_issuer = ISSUER.replace(
        "http://localhost:8081",
        "http://authentication-identity-server:8080",
    )
    token_url = f"{internal_issuer}/protocol/openid-connect/token"
    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "client_id": OIDC_CLIENT_ID,
            "code": code,
            "redirect_uri": OIDC_REDIRECT_URI,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def load_students_file():
    with open(STUDENTS_FILE, encoding="utf-8") as file_handle:
        return json.load(file_handle)


def render_students_page(title: str, students):
        template = """
        <!doctype html>
        <html lang="vi">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{{ title }}</title>
            <style>
                :root {
                    color-scheme: light;
                    --bg: #f4f7fb;
                    --card: #ffffff;
                    --text: #1f2937;
                    --muted: #6b7280;
                    --accent: #0f766e;
                    --border: #dbe3ee;
                }
                body {
                    margin: 0;
                    font-family: Arial, Helvetica, sans-serif;
                    background: linear-gradient(135deg, #eef4ff 0%, #f8fafc 55%, #ecfeff 100%);
                    color: var(--text);
                }
                .container {
                    max-width: 1100px;
                    margin: 40px auto;
                    padding: 0 20px;
                }
                .hero {
                    background: var(--card);
                    border: 1px solid var(--border);
                    border-radius: 20px;
                    padding: 24px;
                    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
                    margin-bottom: 20px;
                }
                .hero h1 {
                    margin: 0 0 8px;
                    font-size: 2rem;
                }
                .hero p {
                    margin: 0;
                    color: var(--muted);
                }
                .table-wrap {
                    overflow-x: auto;
                    background: var(--card);
                    border: 1px solid var(--border);
                    border-radius: 20px;
                    box-shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    text-align: left;
                    padding: 14px 16px;
                    border-bottom: 1px solid var(--border);
                    vertical-align: top;
                }
                th {
                    background: #f8fafc;
                    color: var(--accent);
                    font-size: 0.95rem;
                }
                tr:hover td {
                    background: #f9fbff;
                }
                .empty {
                    padding: 24px;
                    color: var(--muted);
                }
                .badge {
                    display: inline-block;
                    padding: 4px 10px;
                    border-radius: 999px;
                    background: #ecfeff;
                    color: #0f766e;
                    font-size: 0.85rem;
                    font-weight: 700;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="hero">
                    <span class="badge">Flask Backend</span>
                    <h1>{{ title }}</h1>
                    <p>{{ subtitle }}</p>
                </div>
                <div class="table-wrap">
                    {% if students %}
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Student ID</th>
                                <th>Fullname</th>
                                <th>DOB</th>
                                <th>Major</th>
                                {% if show_gpa %}<th>GPA</th>{% endif %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for student in students %}
                            <tr>
                                <td>{{ student.get('id', '') }}</td>
                                <td>{{ student.get('student_id', '') }}</td>
                                <td>{{ student.get('name', student.get('fullname', '')) }}</td>
                                <td>{{ student.get('dob', '') }}</td>
                                <td>{{ student.get('major', '') }}</td>
                                {% if show_gpa %}<td>{{ student.get('gpa', '') }}</td>{% endif %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% else %}
                    <div class="empty">No student data available.</div>
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(
                template,
                title=title,
                subtitle="Dữ liệu được lấy từ file JSON và hiển thị dưới dạng bảng HTML thay vì JSON thô.",
                students=students,
                show_gpa=any("gpa" in student for student in students),
        )


def fetch_students_from_db():
    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connection_timeout=5,
    )
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, student_id, fullname, dob, major FROM students ORDER BY id"
        )
        rows = cursor.fetchall()
        for row in rows:
            if row.get("dob") is not None:
                row["dob"] = row["dob"].isoformat()
        return rows
    finally:
        connection.close()


@app.get("/hello")
def hello():
    return jsonify(message="Hello from App Server!")


@app.get("/student")
@app.get("/student/")
def student():
    try:
        return render_students_page("Student List", load_students_file())
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@app.get("/students-db")
def students_db():
    try:
        return render_students_page("Student Database", fetch_students_from_db())
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@app.get("/secure")
def secure():
    # Browser flow: Keycloak redirects back with ?code=...; exchange it for a token.
    code = request.args.get("code", "").strip()
    if code:
        try:
            token_response = exchange_authorization_code(code)
            access_token = token_response.get("access_token", "")
            if not access_token:
                return jsonify(error="No access token in token response"), 401
            payload = verify_token(access_token)
            return jsonify(
                message="Secure resource OK",
                preferred_username=payload.get("preferred_username"),
                sub=payload.get("sub"),
                flow="authorization_code",
            )
        except Exception as exc:
            return jsonify(error=str(exc)), 401

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        # If opened directly in browser, start OIDC login instead of returning 401.
        authorize_url = (
            f"{LOCALHOST_REALM_ISSUER}/protocol/openid-connect/auth"
            f"?client_id={OIDC_CLIENT_ID}"
            f"&redirect_uri={OIDC_REDIRECT_URI}"
            "&response_type=code"
            "&scope=openid"
        )
        return jsonify(
            error="Missing Bearer token",
            hint="Open the authorize URL to sign in with Keycloak browser flow",
            authorize_url=authorize_url,
        ), 401

    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = verify_token(token)
    except Exception as exc:
        return jsonify(error=str(exc)), 401

    return jsonify(
        message="Secure resource OK",
        preferred_username=payload.get("preferred_username"),
        sub=payload.get("sub"),
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
