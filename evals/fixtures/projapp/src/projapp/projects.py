from datetime import datetime, timezone


def create_project(conn, org_id, name):
    if not name.strip():
        raise ValueError("name required")
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute("INSERT INTO projects (org_id, name, created_at) VALUES (?, ?, ?)", (org_id, name, now))
    return cur.lastrowid


def list_projects(conn, org_id, page=1, per_page=20):
    offset = page * per_page
    rows = conn.execute(
        "SELECT id, name, created_at FROM projects WHERE org_id = ? ORDER BY id LIMIT ? OFFSET ?",
        (org_id, per_page, offset),
    ).fetchall()
    return [dict(r) for r in rows]
