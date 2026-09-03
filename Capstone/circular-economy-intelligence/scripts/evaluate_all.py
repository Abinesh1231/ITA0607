import subprocess, sys
subprocess.run([sys.executable, "-m", "ml.src.classification.evaluate"], check=True)
