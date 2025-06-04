import pandas as pd
import re
from pathlib import Path

import workflow
import workflow_lexer as lex
import regex_maven
import regex_gradle

def new_total ():
    return { "energy" : 0, "seconds" : 0, "n" : 0 }


class Parser:

    total_other = { "maven" : new_total(), "gradle" : new_total() }
    total_all   = { "maven" : new_total(), "gradle" : new_total() }
    all_subtasks = []
                  
    def __init__ (self, file, size):
        self.file = file
        self.file_without_path = Path(self.file).stem
        self.df = pd.read_csv(file)
        self.size = size
        self.idx = 0
        self.len = len(self.df.index)
        self.workflow = workflow.Workflow(file, len(file))
        self.maven = []
        self.gradle = []
        self.other = []


    def is_eof (self):
        return self.idx >= self.len


    # assumes self.idx + 1 is a valid index
    def get_next_name (self):
        return self.df.iloc[self.idx + 1]["name"]


    def get_row (self):
        return self.df.iloc[self.idx]
    

    def get_name (self):    
        return self.get_row()["name"]
    

    def has_error (self, task):    
        return task['has_error'] == True


    def print_task_error (self, task, kind):
      print(f"*** Subtask Error: {kind} (Energy: {task['energy']}): {task['error_msg']}")


    def next_state (self):
        self.idx += 1

    def has_next_state (self):
        return self.idx + 1 < self.len


    def match (self, noerror=False):
        print("Started to Match Workflow")
        while (not self.is_eof()):
            self.match_task(noerror)

        return self.workflow


    def match_task (self, noerror):
        name = self.get_name()
        
        if lex.is_maven_task(name):
            self.match_maven_task(noerror)
        elif lex.is_autobuild_task(name) and lex.is_maven_subtask(self.get_next_name()):
            self.match_maven_task(noerror)
        elif lex.is_gradle_task(name):
            self.match_gradle_task(noerror)
        elif lex.is_autobuild_task(name) and lex.is_gradle_autosubtask(self.get_next_name()):
            self.match_gradle_task(noerror)
        elif self.has_next_state() and lex.is_maven_subtask(self.get_next_name()):
            print(f"Maven subtask without a prior mvn or mvnw: {name}")
            self.match_maven_task(noerror)
        elif self.has_next_state() and lex.is_gradle_subtask(self.get_next_name()):
            print(f"Gradle subtask without a prior mvn or mvnw: {name}")
            self.match_gradle_task(noerror)
        else:
            self.workflow.update_energy_time(self.get_row())
            self.next_state()
        #match_other_task(state)

    
    def match_maven_task (self, noerror):
        name = self.get_name()
        task = self.get_row()
        #if not noerror or not self.has_error():
        print(f"Maven task: {name}") 
        self.maven.append(name)
        self.workflow.update_build_manager("maven", task)
        
        # Using now the energy/time associated with the subtasks
        #self.workflow.update_energy_time(task)

        #self.workflow.update_field("maven", task)
        self.next_state()
        #subtasks = self.new_subtasks(regex_maven.quentin_maven)
        subtasks = self.new_subtasks(regex_maven.plugins)
        #print(f"Maven subb = {get_name(state)} {is_maven_subtask(get_name(state))}")
        has_subtask = False
        while (not self.is_eof() and lex.is_maven_subtask(self.get_name())):
            self.match_maven_subtask(subtasks, noerror)
            self.next_state()
            has_subtask = True
    
        if has_subtask:
            #print(f"Summary Maven for task {name}")
            #self.print_subtasks(subtasks)
            self.workflow.update_subtasks("maven", subtasks)
        #print(workflow)
        else:
            self.workflow.update_energy_time(task)


    def match_gradle_task (self, noerror):
        name = self.get_name()
        task = self.get_row()

        #if not noerror or not self.has_error(task):
        print(f"Gradle task: {name}")
        self.gradle.append(name)
        self.workflow.update_build_manager("gradle", task)
          
        # Using now the energy/time associated with the subtasks
        #self.workflow.update_energy_time(task)

        self.next_state()
        #subtasks = self.new_subtasks(regex_gradle.quentin_gradle)
        subtasks = self.new_subtasks(regex_gradle.plugins)
        has_subtask = False
        while (not self.is_eof() and lex.is_gradle_subtask(self.get_name())):
            self.match_gradle_subtask(subtasks, noerror)
            self.next_state()
            has_subtask = True
    
        if has_subtask:
            #print(f"Summary Gradle for task {name}")
            #self.print_subtasks(subtasks)
            self.workflow.update_subtasks("gradle", subtasks)
        #print(workflow)
        else:
            self.workflow.update_energy_time(task)


    def match_maven_subtask (self, subtasks, noerror):
        name = self.get_name()
        subtask = self.get_row()
        kind = self.get_kind_subtask(name, regex_maven.plugins, subtask["energy"])
        
        
        if self.has_error(subtask):
            self.print_task_error(subtask, kind)

        if not noerror or not self.has_error(subtask):
          self.update_subtask("maven", kind, subtask, subtasks)
          self.workflow.update_energy_time(subtask)

    
    def match_gradle_subtask (self, subtasks, noerror):
        name = self.get_name()
        subtask = self.get_row()
        kind = self.get_kind_subtask(name, regex_gradle.plugins, subtask["energy"])
       
        if self.has_error(subtask):
            self.print_task_error(subtask, kind)

        if not noerror or not self.has_error(subtask):
          self.update_subtask("gradle", kind, subtask, subtasks)
          self.workflow.update_energy_time(subtask)


    def new_subtasks (self, mydict):
        subtasks = {}
        for k in mydict.keys():
            subtasks[k] = new_total()

        subtasks["other"] = new_total()
        return subtasks
    

    def update_subtask (self, bmanager, kind, task, subtasks):
        self.update_subtask_aux(task, subtasks[kind])
        self.update_subtask_aux(task, Parser.total_all[bmanager])
        self.add_all_subtasks(bmanager, kind, task)

        if kind == "other":
            self.update_subtask_aux(task, Parser.total_other[bmanager])
            #print(f'Name: {self.get_name()}, Energy: {task["energy"]}')


    def add_all_subtasks (self, build_tool, kind, subtask):
        entry = self.new_subtask_entry(build_tool, kind, subtask)
        Parser.all_subtasks.append(entry)


    def new_subtask_entry (self, build_tool, kind, subtask):
        return {
            "file"       : self.file_without_path,
            "size"       : self.size,
            "build_tool" : build_tool,
            "kind"       : kind,
            "energy"     : subtask["energy"],
            "seconds"    : subtask["seconds"],
            "has_error"  : subtask["has_error"],
            "error_msg"  : subtask["error_msg"],
        }


    def update_subtask_aux (self, task, subtask):
        subtask["energy"] += task["energy"]
        subtask["seconds"] += task["seconds"]
        subtask["n"] += 1


    def get_kind_subtask (self, name, mydict, energy):
        for subtask, l in mydict.items():
            for x in l:
                #print(f"Procurando {x} em {name} = {re.search(x, name)}")
                if re.search(x, name):
                    return subtask
  
        print(f"Could not match {name}, Energy = {energy}")
        return "other"
    
    
    def print_subtasks(self, subtasks):
        print("Subtask summary for task ")
        for k, v in subtasks.items():
            print(f"  {k}, {v['energy']}, {v['seconds']}, {v['n']}")
            #del v['n']
    
    
    def print_summary(self, bmanager):
        energy = Parser.total_all[bmanager]["energy"]
        seconds = Parser.total_all[bmanager]["seconds"]
        n = Parser.total_all[bmanager]["n"]

        other_energy = Parser.total_other[bmanager]['energy']
        other_seconds = Parser.total_other[bmanager]['seconds']
        other_n = Parser.total_other[bmanager]['n']

        print(f"Total Subtasks: Energy = {energy}, Seconds {seconds}, N = {n}")
        print(f"Non-matched {bmanager} subtasks:")
        self.print_summary_aux(self, "Energy", other_energy, energy)
        self.print_summary_aux(self, "Seconds", other_seconds, seconds)
        self.print_summary_aux(self, "Subtasks", other_n, n)


    def print_summary_aux (self, name, v1, v2):
        ratio = 0
        if v2 != 0:
            ratio = 100 * v1 / v2
        print(f"{name} = {v1:.2f} ({ratio:.2f}%)")


if __name__ == "__main__":
  #import sys
  #nargs = len(sys.argv)
  #if not nargs == 2:
  #  print("Usage: workflow_parser InputFile")
  #  exit()
    
  #input = sys.argv[1]
  input = "/home/sergio/pesquisa/energy-CI-CD/converted_data/correctexam_corrigeExamBack___maven.yml.csv_simple"
  input = "/home/sergio/pesquisa/energy-CI-CD/converted_data/SonarOpenCommunity_sonar-cxx___codeql-analysis.yml.csv_simple"
  parser = Parser(input)
  parser.match()
  print(parser.workflow.__dict__)
  
  
