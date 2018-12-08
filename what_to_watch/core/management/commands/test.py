from pathlib import Path
import os
p = Path(os.path.abspath(__file__)).parents[3]
print(p)
