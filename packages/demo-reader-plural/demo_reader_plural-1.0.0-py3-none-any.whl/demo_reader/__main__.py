import sys
from demo_reader.multireader import MultiReader

print('executing multi-reader-program/__main__.py')

filename = sys.argv[1]
r = MultiReader(filename)
print(r.read())
r.close()