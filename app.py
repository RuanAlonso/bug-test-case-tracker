"""
app.py — Bug & Test Case Tracker
Aplicação Flask simples para cadastro e acompanhamento de bugs e casos de teste.
"""
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = "tracker.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def dashboard():
    conn = get_db()
    bug_counts = conn.execute(
        "SELECT status, COUNT(*) as total FROM bugs GROUP BY status"
    ).fetchall()
    severity_counts = conn.execute(
        "SELECT severity, COUNT(*) as total FROM bugs WHERE status != 'closed' GROUP BY severity"
    ).fetchall()
    tc_counts = conn.execute(
        "SELECT status, COUNT(*) as total FROM test_cases GROUP BY status"
    ).fetchall()
    conn.close()
    return render_template(
        "dashboard.html",
        bug_counts=bug_counts,
        severity_counts=severity_counts,
        tc_counts=tc_counts,
    )


# -------------------- BUGS --------------------

@app.route("/bugs")
def bugs_list():
    status_filter = request.args.get("status", "")
    conn = get_db()
    query = "SELECT * FROM bugs"
    params = []
    if status_filter:
        query += " WHERE status = ?"
        params.append(status_filter)
    query += " ORDER BY created_at DESC"
    bugs = conn.execute(query, params).fetchall()
    conn.close()
    return render_template("bugs_list.html", bugs=bugs, status_filter=status_filter)


@app.route("/bugs/new", methods=["GET", "POST"])
def bug_new():
    conn = get_db()
    if request.method == "POST":
        conn.execute(
            """INSERT INTO bugs (title, description, severity, status, steps_to_reproduce, environment, test_case_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                request.form["title"],
                request.form["description"],
                request.form["severity"],
                request.form["status"],
                request.form["steps_to_reproduce"],
                request.form["environment"],
                request.form.get("test_case_id") or None,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("bugs_list"))
    test_cases = conn.execute("SELECT id, title FROM test_cases").fetchall()
    conn.close()
    return render_template("bug_form.html", test_cases=test_cases)


@app.route("/bugs/<int:bug_id>/status", methods=["POST"])
def bug_update_status(bug_id):
    conn = get_db()
    conn.execute(
        "UPDATE bugs SET status = ? WHERE id = ?",
        (request.form["status"], bug_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("bugs_list"))


@app.route("/bugs/<int:bug_id>/delete", methods=["POST"])
def bug_delete(bug_id):
    conn = get_db()
    conn.execute("DELETE FROM bugs WHERE id = ?", (bug_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("bugs_list"))


# -------------------- TEST CASES --------------------

@app.route("/testcases")
def testcases_list():
    conn = get_db()
    test_cases = conn.execute(
        "SELECT * FROM test_cases ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return render_template("testcases_list.html", test_cases=test_cases)


@app.route("/testcases/new", methods=["GET", "POST"])
def testcase_new():
    conn = get_db()
    if request.method == "POST":
        conn.execute(
            """INSERT INTO test_cases (title, preconditions, steps, expected_result, status)
               VALUES (?, ?, ?, ?, ?)""",
            (
                request.form["title"],
                request.form["preconditions"],
                request.form["steps"],
                request.form["expected_result"],
                request.form["status"],
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("testcases_list"))
    conn.close()
    return render_template("testcase_form.html")


@app.route("/testcases/<int:tc_id>/status", methods=["POST"])
def testcase_update_status(tc_id):
    conn = get_db()
    conn.execute(
        "UPDATE test_cases SET status = ? WHERE id = ?",
        (request.form["status"], tc_id),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("testcases_list"))


@app.route("/testcases/<int:tc_id>/delete", methods=["POST"])
def testcase_delete(tc_id):
    conn = get_db()
    conn.execute("DELETE FROM test_cases WHERE id = ?", (tc_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("testcases_list"))


if __name__ == "__main__":
    app.run(debug=True)
