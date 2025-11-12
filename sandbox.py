import subprocess, tempfile, os, textwrap, signal

def run_user_code(code: str, tests_code: str, timeout=5):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "solution.py")
        with open(path, "w") as f:
            f.write(code + "\n\n" + tests_code)
        try:
            proc = subprocess.run(["python3", path], capture_output=True, text=True, timeout=timeout)
            return {"stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}
        except subprocess.TimeoutExpired:
            return {"error":"timeout"}
v
