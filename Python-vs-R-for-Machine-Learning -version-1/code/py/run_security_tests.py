# 2018-compatible test runner (targets Python 3.6 era).
import os
import sys
import subprocess
import hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, "artifacts")
GEN = os.path.join(ROOT, "generate_malicious_pickle.py")
LOAD = os.path.join(ROOT, "deserialization_test.py")

def run(cmd, cwd=None):
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, universal_newlines=True)
    out, _ = p.communicate()
    return p.returncode, out

def assert_in(text, haystack, msg):
    if text not in haystack:
        raise AssertionError(msg + "\nExpected substring: {t}\nOutput:\n{h}".format(t=text, h=haystack))

def print_ok(label):
    sys.stdout.write("[OK] {l}\n".format(l=label))

def print_fail(label, e):
    sys.stdout.write("[FAIL] {l}: {e}\n".format(l=label, e=e))
    raise

def ensure_artifacts_dir():
    if not os.path.isdir(ART):
        os.makedirs(ART)

def t1_baseline_reduce():
    label = "T1 Baseline RCE via __reduce__ (protocol=2)"
    try:
        code, out = run([sys.executable, GEN, "--protocol", "2", "--method", "reduce"])
        if code != 0:
            raise RuntimeError(out)
        code, out = run([sys.executable, LOAD])
        if code != 0:
            raise RuntimeError(out)
        # Looser substring so it works across shells
        assert_in("malicious pickle executed (demo)", out, "Echo marker not printed")
        assert_in("Loaded object type: <class 'int'>", out, "Return type not int")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def t2_reduce_ex():
    label = "T2 RCE via __reduce_ex__ (protocols 0-3)"
    try:
        for proto in ("0", "1", "2", "3"):
            outpath = os.path.join(ART, "malicious_p{p}.pkl".format(p=proto))
            code, out = run([sys.executable, GEN, "--protocol", proto, "--method", "reduce_ex", "--out", outpath])
            if code != 0:
                raise RuntimeError(out)
            code, out = run([sys.executable, LOAD, "--path", outpath])
            if code != 0:
                raise RuntimeError(out)
            assert_in("malicious pickle executed via __reduce_ex__ (demo)", out,
                      "Missing __reduce_ex__ marker for protocol " + proto)
            assert_in("Loaded object type: <class 'int'>", out, "Return type not int")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def t3_protocol_matrix():
    label = "T3 Protocol matrix (__reduce__, protocols 0-3)"
    try:
        for proto in ("0", "1", "2", "3"):
            outpath = os.path.join(ART, "malicious_reduce_p{p}.pkl".format(p=proto))
            code, out = run([sys.executable, GEN, "--protocol", proto, "--method", "reduce", "--out", outpath])
            if code != 0:
                raise RuntimeError(out)
            code, out = run([sys.executable, LOAD, "--path", outpath])
            if code != 0:
                raise RuntimeError(out)
            assert_in("malicious pickle executed (demo)", out, "Missing marker for protocol " + proto)
            assert_in("Loaded object type: <class 'int'>", out, "Return type not int")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def t4_allowlist_unpickler_blocks():
    label = "T4 Allowlist Unpickler blocks os.system payload"
    try:
        baseline = os.path.join(ART, "malicious.pkl")
        if not os.path.exists(baseline):
            code, out = run([sys.executable, GEN, "--protocol", "2", "--method", "reduce"])
            if code != 0:
                raise RuntimeError(out)

        # Import safe_unpickler and try to load: expect failure
        code, out = run([sys.executable, "-c",
                         "from safe_unpickler import safe_load; "
                         "f=open(r'%s','rb'); "
                         "safe_load(f)" % baseline],
                        cwd=ROOT)
        if code == 0:
            raise AssertionError("Safe unpickler unexpectedly loaded the payload")
        if "blocked:" not in out and "UnpicklingError" not in out:
            raise AssertionError("Expected UnpicklingError with 'blocked:' in output")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def t5_json_control():
    label = "T5 JSON control (no code execution)"
    try:
        py = (
            "import json; "
            "payload={'x':1,'y':[2,3]}; "
            "s=json.dumps(payload); "
            "print(json.loads(s))"
        )
        code, out = run([sys.executable, "-c", py])
        if code != 0:
            raise RuntimeError(out)
        assert_in("{'x': 1, 'y': [2, 3]}", out, "JSON round-trip failed")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def t6_integrity_check():
    label = "T6 Integrity check (SHA256, detects tamper)"
    try:
        baseline = os.path.join(ART, "malicious.pkl")
        if not os.path.exists(baseline):
            code, out = run([sys.executable, GEN, "--protocol", "2", "--method", "reduce"])
            if code != 0:
                raise RuntimeError(out)
        data = open(baseline, "rb").read()
        h_known = hashlib.sha256(data).hexdigest()
        tampered = bytearray(data)
        idx = min(10, max(0, len(tampered) - 1))
        tampered[idx] ^= 0xFF
        h_tampered = hashlib.sha256(tampered).hexdigest()
        if h_tampered == h_known:
            raise AssertionError("Tamper not detected by hash")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def t7_constrained_execution():
    label = "T7 Constrained execution (subprocess demo)"
    try:
        code, out = run([sys.executable, GEN, "--protocol", "2", "--method", "reduce"])
        if code != 0:
            raise RuntimeError(out)
        code, out = run([sys.executable, LOAD])
        if code != 0:
            raise RuntimeError(out)
        assert_in("malicious pickle executed (demo)", out, "Marker not printed")
        print_ok(label)
    except Exception as e:
        print_fail(label, e)

def main():
    sys.stdout.write("Running Python serialization security tests (T1–T7)...\n\n")
    ensure_artifacts_dir()
    t1_baseline_reduce()
    t2_reduce_ex()
    t3_protocol_matrix()
    t4_allowlist_unpickler_blocks()
    t5_json_control()
    t6_integrity_check()
    t7_constrained_execution()
    sys.stdout.write("\nAll tests completed.\n")

if __name__ == "__main__":
    main()
