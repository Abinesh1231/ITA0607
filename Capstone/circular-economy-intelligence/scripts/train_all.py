import subprocess, sys

commands = [
    [sys.executable, "-m", "ml.src.data.split"],
    [sys.executable, "-m", "ml.src.classification.train"],
]
for cmd in commands:
    subprocess.run(cmd, check=True)
