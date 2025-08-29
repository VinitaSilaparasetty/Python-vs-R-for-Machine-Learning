# file: code/py/deserialization_test.py
# WARNING: Loads a crafted pickle and triggers its side effect (2018-compatible).
import pickle
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="artifacts/malicious.pkl")
    args = ap.parse_args()

    with open(args.path, "rb") as f:
        obj = pickle.load(f)  # Executes payload via __reduce__/__reduce_ex__
    print("Loaded object type:", type(obj))
    print("Loaded object repr:", repr(obj))

if __name__ == "__main__":
    main()
