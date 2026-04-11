import json
import os
import time

import jwt
import mysql.connector
import requests
from flask import Flask, jsonify, request
from jwt.algorithms import RSAAlgorithm


ISSUER = os.getenv("OIDC_ISSUER", "http://authentication-identity-server:8080/auth/realms/realm_sv001")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "myapp")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"
MASTER_ISSUER = os.getenv("OIDC_MASTER_ISSUER", "http://authentication-identity-server:8080/auth/realms/master")
LOCALHOST_ISSUER = os.getenv("OIDC_LOCALHOST_ISSUER", "http://localhost:8081/auth/realms/master")
LOCALHOST_REALM_ISSUER = os.getenv("OIDC_LOCALHOST_REALM_ISSUER", "http://localhost:8081/auth/realms/realm_sv001")
ALLOWED_ISSUERS = {ISSUER, MASTER_ISSUER, LOCALHOST_ISSUER, LOCALHOST_REALM_ISSUER}
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


def load_students_file():
    with open(STUDENTS_FILE, encoding="utf-8") as file_handle:
        return json.load(file_handle)


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
        return jsonify(load_students_file())
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@app.get("/students-db")
def students_db():
    try:
        return jsonify(fetch_students_from_db())
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@app.get("/secure")
def secure():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401

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
