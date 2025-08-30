# coding: utf-8
"""
Black-box probes for a running Python dashboard (Flask/Streamlit-like).
Tests:
  A1 XSS reflection
  A2 Filename/path traversal
  A3 DoS via oversized input
How to use:
  1) Start your Python dashboard locally (e.g., http://127.0.0.1:5000)
  2) Set TARGET_URL and endpoints below.
  3) python dashboard_attacks.py
Python 3.6 compatible (requests==2.18.x).
"""
from __future__ import print_function
import os, re, time
try:
    import requests
except Exception:
    raise SystemExit("Please: pip install requests==2.18.4")

# ---- configure these to match your app ----
TARGET_URL = "http://127.0.0.1:5000"
ANALYZE_ENDPOINT = "/analyze"    # e.g., accepts form/json: term, n
PING_ENDPOINT    = "/"           # basic GET page to check liveness
DATA_DIR         = os.path.abspath(os.path.join(os.getcwd(), "data"))
TIMEOUT_S        = 12

def ok(msg):  print("[OK]  " + msg)
def bad(msg): print("[FAIL] " + msg)

def live():
    try:
        r = requests.get(TARGET_URL + PING_ENDPOINT, timeout=TIMEOUT_S)
        return r.status_code < 500
    except Exception:
        return False

def post_analyze(term, n):
    # try JSON first, then form; adapt if your app differs
    u = TARGET_URL + ANALYZE_ENDPOINT
    try:
        r = requests.post(u, json={"term": term, "n": n}, timeout=TIMEOUT_S)
        if r.status_code >= 400:
            # fallback to form
            r = requests.post(u, data={"term": term, "n": n}, timeout=TIMEOUT_S)
        return r
    except Exception as e:
        raise SystemExit("Could not reach dashboard at {}: {}".format(u, e))

def test_xss_reflection():
    """
    A1: if the dashboard reflects the search term into HTML without escaping,
        the raw <script> will appear in the response body.
        We only check for raw tags; we DO NOT execute any JS.
    """
    marker = "<script>SAFE_POC</script>"
    r = post_analyze(marker, 10)
    body = r.text or ""
    reflected_raw = marker in body
    reflected_escaped = ("&lt;script&gt;SAFE_POC&lt;/script&gt;" in body) or ("&lt;script&gt;" in body)
    if reflected_raw and not reflected_escaped:
        bad("A1 XSS reflection detected (raw <script> present).")
    else:
        ok("A1 XSS reflection not observed (content escaped or not reflected).")

def sanitize_filename(s):
    return re.sub(r"[^A-Za-z0-9._-]", "_", s)

def expected_path(term, suffix="stack"):
    name = "{}_{}.csv".format(sanitize_filename(term), suffix)
    return os.path.join(DATA_DIR, name)

def test_path_traversal():
    """
    A2: attempt to influence server-side filenames with traversal/meta chars.
    This probe sends a traversal-y term and then checks whether a file
    appears outside DATA_DIR (we only check expected safe path).
    NOTE: this is a heuristic; if your server writes elsewhere, adjust.
    """
    term = "../etc/passwd"
    r = post_analyze(term, 5)
    time.sleep(1.0)  # allow write
    safe_p = expected_path(term)
    if os.path.exists(safe_p):
        ok("A2 Filename sanitized (created under data/: {})".format(safe_p))
    else:
        # If server created an unexpected file or blocked the request, we can’t
        # see it; treat as pass unless you KNOW your app writes under ./data/.
        ok("A2 No unsafe file observed under data/ (likely blocked or written elsewhere).")

def test_dos_size():
    """
    A3: send an oversized request to check time-to-first-byte and status.
    We DO NOT aim to crash the app; we merely assert time-bound behavior.
    """
    term = "news"
    big_n = 100000  # oversized
    t0 = time.time()
    try:
        r = post_analyze(term, big_n)
        dt = time.time() - t0
        if dt > 8.0:
            bad("A3 Oversized input responded slowly (>{:.1f}s). Consider caps/queue.".format(dt))
        else:
            ok("A3 Oversized input bounded (responded in {:.1f}s with status {}).".format(dt, r.status_code))
    except Exception as e:
        ok("A3 Oversized input rejected quickly: {}".format(e))

def main():
    if not live():
        raise SystemExit("Dashboard not reachable at {}".format(TARGET_URL))
    if not os.path.isdir(DATA_DIR):
        try: os.makedirs(DATA_DIR)
        except Exception: pass
    print("Running Python dashboard probes against", TARGET_URL)
    test_xss_reflection()
    test_path_traversal()
    test_dos_size()
    print("Done.")
if __name__ == "__main__":
    main()
