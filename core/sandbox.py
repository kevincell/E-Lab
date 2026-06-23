import os
import shutil
import subprocess
import uuid


SANDBOX_DIR = "/var/elab-sandbox"


def run_c_code(source_code: str, stdin: str = "", expected_output: str = "",
               time_limit: float = 2.0, memory_limit_kb: int = 128000) -> dict:
    """
    Runs C code in an isolated Docker container.
    Works on cgroup v1 and v2.
    """
    memory_limit_mb = memory_limit_kb // 1024
    run_id = str(uuid.uuid4())
    tmpdir = os.path.join(SANDBOX_DIR, run_id)
    os.makedirs(tmpdir, exist_ok=True)

    try:
        code_file = os.path.join(tmpdir, "main.c")
        with open(code_file, "w") as f:
            f.write(source_code)

        input_file = os.path.join(tmpdir, "input.txt")
        with open(input_file, "w") as f:
            f.write(stdin)

        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", f"{memory_limit_mb}m",
            "--memory-swap", f"{memory_limit_mb}m",
            "--cpus", "0.5",
            "--pids-limit", "64",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges:true",
            "--tmpfs", "/tmp:rw,nosuid,exec,size=50m",
            "-v", f"{tmpdir}:/box:rw",
            "elab-sandbox",
            "sh", "-c",
            f"cd /box && gcc main.c -o /tmp/program 2>&1 && timeout {time_limit}s /tmp/program < input.txt"
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=time_limit + 5
            )

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if "error:" in stdout.lower() or "error:" in stderr.lower():
                return {
                    "status_id": 6,
                    "status": "Compilation Error",
                    "stdout": "",
                    "stderr": "",
                    "compile_output": stdout or stderr,
                    "time": "0.0",
                    "memory": 0,
                }

            if result.returncode == 124 or "timeout" in stderr.lower():
                status_id = 5
                status_desc = "Time Limit Exceeded"
            elif result.returncode != 0:
                status_id = 11
                status_desc = "Runtime Error"
            elif expected_output and stdout == expected_output.strip():
                status_id = 3
                status_desc = "Accepted"
            elif expected_output:
                status_id = 4
                status_desc = "Wrong Answer"
            else:
                status_id = 3
                status_desc = "Accepted"

            return {
                "status_id": status_id,
                "status": status_desc,
                "stdout": stdout,
                "stderr": stderr,
                "compile_output": "",
                "time": str(time_limit if status_id == 5 else 0.1),
                "memory": 1024,
            }

        except subprocess.TimeoutExpired:
            return {
                "status_id": 5,
                "status": "Time Limit Exceeded",
                "stdout": "",
                "stderr": "Execution timed out",
                "compile_output": "",
                "time": str(time_limit),
                "memory": memory_limit_kb,
            }

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
