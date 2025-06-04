import sys
import os
import pandas as pd
import workflow_parser as wkparser
import shutil
import csv
from pathlib import Path

LOC_SMALL   =   10_000
LOC_MEDIUM  =  100_000

# we need at least three points to calculate a line with MMQ
def is_len_valid (input_file):
  with open(input_file) as f:
    n_lines = len(f.readlines())
    return n_lines > 1, n_lines


def check_null_energy_time(input_file):
  with open(input_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      energy = float(row["energy"])
      seconds = float(row["seconds"])
      if energy == 0 and not seconds == 0:
        print(f"Null energy measurement and non-null time measurement: {row['name']} {row['energy']} {row['seconds']}")
        return False
      elif not energy == 0 and seconds == 0:
        print(f"Non-null energy measurement and null time measurement: {row['name']} {row['energy']} {row['seconds']}")
        return False

  return True


def calc_corr (df, row1, row2, method):
  new_df = df[[row1, row2]].copy()
  x = new_df.corr(method)
  #print(new_df.corr(), x[row1][row2])
  return x[row1][row2]


def search_project_loc (workflow_path, loc_dir):
  files = sorted(os.listdir(loc_dir))
  workflow_name = os.path.basename(workflow_path)
  print(f"Setting size for {workflow_name}")
  for f in files:
    filename = Path(f).stem
    if workflow_name.startswith(filename):
      print(f"Arquivo {workflow_name} Começa com {filename}")  
      return f

  print(f"Could not find LOC for {workflow_name}")
  return None


def add_row_cloc (row):
  nocode = [ "XML", "JSON", "Text", "CSV", "HTML", "Markdown", "Properties", "SVG", "CSS", "XSD", "AsciiDoc", "SUM" ]
  lang = row["language"]
  code = row["code"]
  if lang in nocode:
    return 0
  else:
    return code
    

def process_cloc_file (file):
  try:
    df = pd.read_csv(file)
    total = 0
    for index, row in df.iterrows():
      total += add_row_cloc(row)

    return total
  except Exception as e:
      raise Exception(f"Exception for {file}") from e



def set_project_size (workflow_path, loc_dir):
  file = search_project_loc(workflow_path, loc_dir)
  if not file:
    return False
  
  input_file = os.path.join(loc_dir, file)
  sloc = process_cloc_file(input_file)

  if sloc <= LOC_SMALL:
    #workflow.size = "small"
    return "small"
  elif sloc <= LOC_MEDIUM:
    #workflow.size = "medium"
    return "medium"
  else:
    #workflow.size = "large"
    return "large"

  #print(sloc, workflow.size)

  #assert False
  return True


def calc_overview (file, size, noerror): 
  df = pd.read_csv(file)
  
  parser = wkparser.Parser(file, size)
  
  workflow = parser.match(noerror)
  #print(f"Name = {workflow.name}")
  workflow.pearson = calc_corr(df, 'energy', 'seconds', 'pearson')
  workflow.spearman = calc_corr(df, 'energy', 'seconds', 'spearman')
  #print(f"Energy = {workflow.energy}, Seconds = {workflow.seconds}")
  workflow.slope = workflow.energy / workflow.seconds
  return workflow


def convert_dir_overview (input_dir, loc_dir, noerror):
  files = os.listdir(input_dir)
  suffix = ".csv_simple"
  csvfiles = sorted([ f for f in files if f.endswith(suffix) ])
  results = []
  for f in csvfiles:
    try:
      print(f"Processing file {f}")
      input_file = os.path.join(input_dir, f)

      valid, n_lines = is_len_valid(input_file)
      if not valid:
        print(f"Discarding file {f}: only {n_lines} lines")
        continue

      valid = check_null_energy_time(input_file)
      if not valid:
        print(f"Discarding file {f}: null values for energy or time measurements")
        continue
      
      print(f"Analysing file {input_file}")

      size = set_project_size(input_file, loc_dir)
      if size:
      #print(f"Result: {result}\n")
      #result["file"] = result["file"].replace(suffix, ".csv_simple")
        result = calc_overview(input_file, size, noerror)
        result.size = size
        results.append(result)
      
      #check_null(result, "null_energy")
      #check_null(result, "null_time")
    except Exception as e:
      raise Exception(f"Exception for {input_file}") from e

  return results
   

def save_csv (content, output_dir, myfile):
    output_file = os.path.join(output_dir, myfile)
    pd.DataFrame(content).to_csv(output_file, index=False)


def save_csv_tasks (content, output_dir, myfile):
    output_file = os.path.join(output_dir, myfile)
    print(f"Save csv tasks: saving {len(content)} taks")
    pd.DataFrame(content).to_csv(output_file, index=False)


def copy_files (workflows, input_dir, output_dir):
    both_dir = os.path.join(output_dir, "both")
    maven_dir = os.path.join(output_dir, "maven")
    gradle_dir = os.path.join(output_dir, "gradle")
    none_dir = os.path.join(output_dir, "none")
    for w in workflows:
      file = os.path.join(input_dir, w.name)
      if w.is_maven and w.is_gradle:
        shutil.copy(file, both_dir)
      elif w.is_maven:
        shutil.copy(file, maven_dir)
      elif w.is_gradle:
        shutil.copy(file, gradle_dir)
      else:
        shutil.copy(file, none_dir)

  
if __name__ == "__main__":
  nargs = len(sys.argv)
  if not nargs >= 5:
    print("Usage: overview InputDir LoCDir OutputDir OutputFile [noerror]")
    exit()
    
  input_dir = sys.argv[1]
  loc_dir = sys.argv[2]
  output_dir = sys.argv[3]
  output_csv = sys.argv[4]
  noerror = False
  if nargs == 6:
    noerror = sys.argv[5]
  suffix = "_noerror.csv" if noerror=="True" else "_witherror.csv"
  print(f"Suffix {suffix}")
  print(f"NoErrorValue {noerror}")
  output_name = f"all_tasks{suffix}"
  output_csv = output_csv.replace(".csv",suffix)
  
  os.makedirs(output_dir, exist_ok=True)
  results = convert_dir_overview(input_dir, loc_dir, noerror)
  n = len(results)
  print("----")
  print(f"Converted {len(results)} files")
  maven = [x for x in results if x.is_maven == True]
  print(f"Maven files = {len(maven)} ({100*len(maven)/n:.1f}%)")
  gradle = [x for x in results if x.is_gradle == True]
  print(f"Gradle files = {len(gradle)} ({100*len(gradle)/n:.1f}%)")
  nomanager = [x for x in results if not (x.is_maven or x.is_gradle)]
  print(f"No build manager files = {len(nomanager)} ({100*len(nomanager)/n:.1f}%)")
  print("----")
  wkparser.Parser.print_summary(wkparser.Parser, 'maven')
  print("----")
  wkparser.Parser.print_summary(wkparser.Parser, 'gradle')

  mydict = [vars(x) for x in results]
  #save_csv(results, output_dir, output_csv)
  save_csv(mydict, output_dir, output_csv)
  save_csv_tasks(wkparser.Parser.all_subtasks, output_dir, output_name)
  #copy_files(results, input_dir, output_dir)
  #print(par)
  #process(output_dir)

