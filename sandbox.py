import os

print(__file__)
print(os.path.dirname(__file__))
print(os.path.dirname(os.path.dirname(__file__)))

print("base_dir:", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
