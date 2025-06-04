import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy import ndimage
# https://pypi.org/project/cliffs-delta/
from cliffs_delta import cliffs_delta

sizes1 = [ "small", "medium", "large" ]
sizes2 = [ "all", "small", "medium", "large" ]

# Creates a dictionary with provided fields (plus a field 'n')
def make_dict_sum (df, fields):
  d = { 'n' : len(df) }
  for field in fields:
    d[field] = df[field].sum()
  return d


def print_ratios_summary (title, dict1, dict2, verbose=True, limit=0):
    print(f"*** {title} ***")
    for x in dict1:
      print_ratio(dict1[x], dict2[x], x.title(), end=";  ", verbose=verbose, limit=limit)
    print("")


def print_ratio (x, y, label, end="\n", verbose=True, limit=0):
    ratio = get_ratio(x, y)
    output = f"{label}: "
    if verbose:
      output = f"{output} {x:.0f} ({ratio:.1f}%)"
    else:
      output = f"{output} {ratio:.1f}%"

    print(output, end=end)


def get_ratios (dict1, dict2, n=1):
  res = []
  for x in dict1:
    res.append(get_ratio(dict1[x], dict2[x], n))
  return res


def get_ratio (x, y, n = 1):
    return round(100 * x / y, n)


def calc_workflow_energy_proportion (df, build_tool_tasks):
  all_energy = df['energy'].sum()
  all_seconds = df['seconds'].sum()

  print_ratio(build_tool_tasks["total"]["energy"], all_energy, "Energy")
  print_ratio(build_tool_tasks["total"]["seconds"], all_seconds, "Seconds")


def plot_bars (properties, bars, title="My title", ylabel = "% of Total", lim=110, colors=[], width=0.25, xlabel=''):
  x = np.arange(len(properties))  # the label locations
  #width = 0.25  # the width of the bars
  multiplier = 0

  fig, ax = plt.subplots(layout='constrained')

  for attribute, measurement in bars.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel(ylabel)
  ax.set_title(title)
  ax.set_xticks(x + width, properties)
  ax.legend(loc='upper left', ncols=3)
  ax.set_ylim(0, lim)
  
  plt.xlabel(xlabel)
  plt.savefig("energy.png")
  plt.show()


# Test Normality
def test_normality (a):
  stat, p = stats.normaltest(a)
  print('stat=%.3f, p=%.3f' % (stat, p))
  if p > 0.05:
    print('probably gaussian')
  else:
    print('probably non gaussian')


##### RQ2

from operator import itemgetter
import collections

subtask_fields = [
  "n",
  "energy",
  "seconds",
]


def sort_by_field (res, field):  
  tmp = collections.OrderedDict(sorted(res.items(), key=lambda t:t[1][field], reverse=True))
  res = {}
  for x, y in tmp.items():
    res[x] = y

  return res


def calc_sum_aux (df, prefix):
  res = {}
  for x in subtask_fields:
    res[x] = df[prefix + '_' + x].sum()
  
  return res
  
    
def calc_sum (df, prefix, mydict):
  res = { }
  res["total"] = {}
  for x in subtask_fields:
    res["total"][x] = 0

  for x in mydict:
    key = prefix + x
    res[key] = calc_sum_aux(df, key)
    for field in subtask_fields:
      res["total"][field] += res[key][field]

  # Ordering result by energy field  
  return sort_by_field(res, 'energy')


def make_dict_subtask (df, prefix, plugins):
    new_dict = {}
    new_dict['n_work'] = len(df)
    tmp_dict = calc_sum(df, prefix, plugins)['total']
    for key, value in tmp_dict.items():
        new_dict[key] = value
    return new_dict


def calc_ratio (mydict):
  for x in mydict:
    energy = mydict[x]["energy"]
    seconds = mydict[x]["seconds"]
    n = mydict[x]["n"]
    mydict[x]["rat_p"] = 100 * get_ratio(energy, seconds, 1)
    mydict[x]["rat_n"] = get_ratio(energy, n, 1)


def print_tasks_summary (mydict, limit=0):
  for key, value in mydict.items():
    print_ratios_summary(key.title(), value, mydict['total'], verbose=False, limit=limit)



def survey(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='large')

    
    return fig, ax




def survey_two_aux (results, category_names, ax):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    #fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)

        
def survey_two (results1, results2, category_names):
    plt.rc('font', size=22)
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(32,8))
    ax1.set_title("(a)", y=-0.01)
    ax2.set_title("(b)", y=-0.01)
    
    #first_legend = ax1.legend(handles = "Testando",   
                         #loc ='lower center')  
    
    #ax1.add_artist(first_legend)  
    
    #fig.legend(handles =[line2], loc ='lower center') 


    survey_two_aux(results1, category_names, ax1)
    
    survey_two_aux(results2, category_names, ax2)

    ax1.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
               loc='lower left', fontsize='medium')


def calc_energy_category (categories, task_energy, field, bmanager, prefix):
  energy_category = {}

  for x in categories.keys():
    energy_category[x] = 0

  for x in task_energy:
    for key, value in categories.items():
      if x in value:
        energy_category[key] += bmanager[f'{prefix}{x}'][field]
        break
        
  return energy_category


def calc_energy_category_dict (df, categories, tasks, prefix):
  dict_cat = {}

  for x in categories.keys():
    dict_cat[x] = []

  for x in tasks:
    lst_task_energy = calc_energy_task(df, x, prefix)
    
    for key_cat, value in categories.items():
      if x in value:
        dict_cat[key_cat] += lst_task_energy
        break
        
  return dict_cat


def calc_power_category (df, categories, tasks, prefix, time=True):
  dict_cat = {}

  for x in categories.keys():
    dict_cat[x] = []

  for x in tasks:
    lst_task_power = calc_power_task(df, x, prefix, time)
    
    for key_cat, value in categories.items():
      if x in value:
        dict_cat[key_cat] += lst_task_power
        break
        
  return dict_cat


def calc_energy_task (df, field, prefix):
    key = prefix + field
    key_energy = key + "_energy"
    
    df_tmp = df[df[key_energy] > 0]
    values = []
    for index, row in df_tmp.iterrows():
      energy = row[key_energy]
      values.append(energy)
    
    return sorted(values)


def calc_power_task (df, field, prefix, time=True):
    key = prefix + field
    key_energy = key + "_energy"
    if time:
      key_seconds = key + "_seconds"
    else:
      key_seconds = key + "_n"
    df_tmp = df[df[key_energy] > 0]
    
    values = []
    for index, row in df_tmp.iterrows():
      energy = row[key_energy]
      # time is in millisecons, energy is in Watt-second
      seconds = row[key_seconds] / 1000
      values.append(energy / seconds)
    
    return sorted(values)


def read_all_tasks (file, build_tool, noerror=True):
  df = pd.read_csv(file)
  
  if noerror:
    df = remove_tasks_with_errors(df)

  df = df[df["build_tool"] == build_tool]
  print(f"Build tool {build_tool} = {len(df)}")
  return df


def get_energy_all_tasks (df, group=True, all=True):
  dict_energy = {}
  list_all = []
  for s in sizes1:
    new_df = df[df["size"] == s]
    print(f"len {s} = {len(new_df)}")
    if group:
      new_df = new_df.groupby("file").sum().reset_index()
      print(f"Group len {s} = {len(new_df)}")
    #print(res)  
    dict_energy[s] = list(new_df["energy"])
    list_all += dict_energy[s]

  if all:
    dict_energy["all"] = list_all  
  
  return dict_energy




def filter_tasks_by (mydict, field, lim):
  tmp = {}
  for key, value in mydict.items():
    ratio = 0
    if field == '':
      ratio = value / mydict["total"]
    else:
      ratio = value[field] / mydict["total"][field]
    if ratio >= lim:
        tmp[key] = value

  return tmp


def check_categories (bmanager):
  plugins = bmanager.plugins
  categories = bmanager.categories

  for p in plugins.keys():
    flag = False
    for key, value in categories.items():
      if p in value:
        flag = True
        break
  
    assert flag, f"Could not find a category for plugin '{p}'"

  for key, value in categories.items():
    for v in value:
      assert v in plugins, f"Could not find plugin '{v}' from category '{key}'"


def remove_workflows_no_subtask(df, prefix, plugins):
  drop_list = check_no_subtasks(df, prefix, plugins)
  new_df = df.drop(drop_list)
  old_n = len(df)
  new_n = len(new_df)
  print(f"Workflows No Subtask: Removed {old_n - new_n} workflows: {old_n} -> {new_n}")
  return new_df


def remove_tasks_with_errors (df):
  new_df = df[df["has_error"] == False]
  old_n = len(df)
  new_n = len(new_df)
  print(f"Tasks With Error: Removed {old_n - new_n} workflows: {old_n} -> {new_n}")
  return new_df


def check_no_subtasks (df, prefix, plugins):
  no_sub_list = []
  for index, row in df.iterrows():
    flag = False
    for x in plugins:
      key = prefix + x + '_energy'
      if row[key] > 0:
        flag = True
    
    if not flag:
      #print(f"{row['name']} does not have subtasks")
      no_sub_list.append(index)
    
  return no_sub_list


def calc_category_kruskall_mwu (dict_cat):
  list_value_cat = []
  list_name_cat = []
  discarded_cat = []
  for key, value in dict_cat.items():
   n_workflows = len(value)
   print(f"Category: {key}, N: {n_workflows}, median: {ndimage.median(value):.3f}")
   if n_workflows >= 5:
     list_value_cat.append(value)
     list_name_cat.append(key)
   else:
     discarded_cat.append(key)

  print("")
  print(f"Cats for Kruskall:  f{list_name_cat}")
  print(f"Discarded category: f{discarded_cat}")

  print("")  
  print(stats.kruskal(*list_value_cat))

  for i in range(0, len(list_value_cat)):
    v1 = list_value_cat[i]
    for j in range(0, len(list_value_cat)):
      v2 = list_value_cat[j]
      stat, pvalue = stats.mannwhitneyu(v1, v2)
      if pvalue < 0.05:
        d, res = cliffs_delta(v1, v2)
        #print(f"{list_name_cat[i]} x {list_name_cat[j]} = {stat}, {pvalue}. Cliff {res}")
        print(f"{list_name_cat[i]} x {list_name_cat[j]}: Cliff {res} ({d:.3f})" )
      else:
        print(f"{list_name_cat[i]} x {list_name_cat[j]}: EQUAL")
    print("")


def create_dfs_size (df, build_tool, sizes=[ "small", "medium", "large" ]):
    df_build = {}
    df_build['all'] = df.loc[df[build_tool]]
    df_all = df_build['all']
    for x in sizes:
        df_build[x] = df_all.loc[df_all['size'] == x]
        
    return df_build


def map_task_category (kind, categories):
    for key, value in categories.items():
        if kind in value:
            return key
        

def field_by_cat (df, field, plugins, categories):
    dict_cat = {}
    for x in categories.keys():
      dict_cat[x] = []
    
    for kind in plugins.keys():
      cat = map_task_category(kind, categories)
      df_kind = df[df['kind'] == kind]
      lst = list(df_kind[field])
      dict_cat[cat] += lst
    
    return dict_cat  


def power_by_cat (df, plugins, categories):
    dict_cat = {}
    for x in categories.keys():
      dict_cat[x] = []
    
    for kind in plugins.keys():
      cat = map_task_category(kind, categories)
      df_kind = df[df['kind'] == kind]
      for index, row in df_kind.iterrows():
        energy = row['energy']
        time   = row['seconds'] / 1000 # miliseconds to seconds
        dict_cat[cat].append(energy / time)
          
    return dict_cat


def get_tasks_by_kind (df, plugins):
    tasks = {}
    for key in plugins.keys():
      tasks[key] = []
     
    for index, row in df.iterrows():
        kind = row["kind"]
        #tasks[kind].append( { "energy" : row["energy"], "seconds": row["seconds"], "n" : 1 } )
        tasks[kind].append(row["energy"])
        
    return tasks


def calc_energy_by_task (tasks):
  dict_sum = {}
  dict_sum["total"] = 0
  for key, value in tasks.items():
    dict_sum[key] = sum(value)
    dict_sum["total"] += dict_sum[key]
        
  return dict_sum


def print_all_tasks (sum_tasks):
  ordered_sum = dict(sorted(sum_tasks.items(), key=lambda item: item[1], reverse=True))
  for key, value in ordered_sum.items():   
    print(f"{key}: Energy: {value} ({get_ratio(value, ordered_sum['total'])}%)")



def get_ratio_categories (categories):
  ratios_category = []
  all_energy = sum(categories.values())
  for key, value in categories.items():
    ratios_category.append(get_ratio(value, all_energy, 0))
    #print(f'{key} : {get_ratio(value, all_energy, 0)}')
    
  return ratios_category
