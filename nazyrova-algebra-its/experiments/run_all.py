"""One command to reproduce every reported number.

Runs, in order: agreement (Table 5), ablation (Table 7), sensitivity (Fig 6),
topic mastery (Table 6 / Fig 7). Emits everything to results/.
"""
import subprocess, sys, os
HERE = os.path.dirname(__file__)
for script in ["eval_agreement.py", "eval_ablation.py", "sensitivity.py", "topic_mastery.py"]:
    print("==>", script)
    subprocess.run([sys.executable, os.path.join(HERE, script)], check=True)
print("Done. See results/.")
