import sys
import csv
import operator
import pandas as pd

#0 days 00:00:05.915854
def convert_time_to_ms (txt):
  txt = txt.replace(":", " ").replace(".", " ")
  l = [int(s) for s in txt.split() if s.isdigit()]
  conversion = [ 1, 24, 60, 60, 1000000]
 
  #print(f"txt = {txt}, l = {l}") 
  
  if len(l) == 4:
    l.append(0)
    
  assert len(l) == 5, f"{len(l)}"
  
  time = l[0]
  for i in range(1, len(l)):
    time = time * conversion[i] + l[i]
  
  #print(f"Time = {time}")
  
  time2 = l[4] + l[3] * pow(10, 6) + l[2] * 60 * pow(10, 6) + l[1] * 60 * 60 * pow(10, 6) + l[0] * 24 * 60 * 60 * pow(10, 6)
  #print(f"Time2 = {time2}")
  
  assert(time == time2)
  return time # time in microseconds
 


# group_execution, energy,  ,  ,  ,  execution_time 
# A CSV entry should have 6 columns
# 1 Name ; 2 RAPL Pkg ; 3 None ; 4 None ; 5 None ; 6 CPU Time
def make_new_csv_entry (entry_data, csv_file):  
  with open(csv_file, "a+") as f:
     f.write(", ".join(entry_data))
     f.write("\n")


def make_new_dict_entry (row, row_dict, merge, i_row):
  exec_time = convert_time_to_ms(row["execution_time"])
  row_name = row["group_execution"].replace(",", "_")
  previous_energy = 0
  previous_time = 0
  if row_name in row_dict:
    #print(f"Duplicated row: {row_name}")
    if merge:
      previous_energy = float(row_dict[row_name][1])
      previous_time = float(row_dict[row_name][5])
    else:
      row_name += f"__dup_{i_row}"

  col_energy = "energy_j"
  entry_data = [ row_name, f"{float(row[col_energy]) + previous_energy}", "", "", "", f"{exec_time + previous_time:.0f}", row['has_error'], row['error_msg'] ]
  #print(', '.join(entry_data))
  row_dict[row_name]  = entry_data

def generate_simple_csv (row_dict, output_file):
  # Erase content of output file if it exists
  with open(output_file, "w") as f:
    pass

  simple_list = []
  for entry, value in row_dict.items():
    element = { "name" : value[0], "energy" : value[1], "seconds" : value[5], "has_error" : value[6], "error_msg" : value[7] }
    simple_list.append(element)
  
  sorted_list = sorted(simple_list, key=lambda e: float(e['energy']), reverse=True)
  pd.DataFrame(sorted_list).to_csv(output_file, index=False)
  

def generate_csv_file (row_dict, output_file):
  # Erase content of output file if it exists
  with open(output_file, "w") as f:
    pass

  for entry, value in row_dict.items():
    make_new_csv_entry(value, output_file)


def generate_sorted_csv_file (row_dict, output_file):
  with open(output_file) as csvfile:
    reader = csv.reader(csvfile)
    csv_sorted = sorted(reader, key=lambda row: float(row[1]), reverse=True)
    #print(csv_sorted)
    with open(output_file + "_sorted", "w") as f:
      for row in csv_sorted:
        f.write(",".join(row))
        f.write("\n")


def convert (input_file, output_file, merge = True):
  with open(input_file, newline='') as csvfile: 
    reader = csv.DictReader(csvfile)
    i = 0
    row_dict = {}
    for row in reader:
      if i == 0:
        #print(f'Column names are {", ".join(row)}')
        i += 1
      make_new_dict_entry(row, row_dict, merge, i)
      i += 1

  generate_csv_file(row_dict, output_file)
  generate_simple_csv(row_dict, output_file + "_simple")
  generate_sorted_csv_file(csvfile, output_file)


if __name__ == "__main__":
  nargs = len(sys.argv)
  if not (nargs == 3 or nargs == 4):
    print("Usage: convert_format InputFile.csv OutputFile.csv [--merge]")
    exit()

  input_file = sys.argv[1]
  output_file = sys.argv[2]
  merge = (nargs == 4 and sys.argv[3] == "--merge")
  
  convert(input_file, output_file, merge)


