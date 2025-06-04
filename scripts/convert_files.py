import convert_format as cformat
import sys
import os


def isValid (f):
  with open(f, "r") as myfile:
    n_lines = len(myfile.readlines())
    return n_lines > 1


def convert (input_dir, output_dir):
  # Ensure output directory exists
  os.makedirs(output_dir, exist_ok=True)
  for f in sorted(os.listdir(input_dir)):
    input_file = os.path.join(input_dir, f)
    output_file = os.path.join(output_dir, f)
    print(f"File {input_file}")
    if isValid(input_file):
      print(f"Converting {f}")
      cformat.convert(input_file, output_file, False)
    else:
      print(f"Discarding {f}: too few lines")
  
  
if __name__ == "__main__":
  nargs = len(sys.argv)
  if not (nargs == 2 or nargs == 3):
    print("Usage: convert_files InputDir [OutputDir]")
    exit()
    
  input_dir = sys.argv[1]
  output_dir = "."
  if nargs > 2:
    output_dir = sys.argv[2]
    
  convert(input_dir, output_dir)

