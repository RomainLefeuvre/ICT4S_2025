import regex_gradle
import regex_maven
import os

class Workflow:

    def __init__ (self, path, tasks):
        self.name             = os.path.basename(path)
        self.tasks            = tasks
        self.slope            = None
        self.pearson          = None
        self.spearman         = None
        self.seconds          = 0
        self.energy           = 0
        self.null_energy      = 0
        self.null_time        = 0
        self.is_maven         = False
        self.is_gradle        = False
        self.maven_energy     = 0
        self.maven_seconds    = 0
        self.gradle_energy    = 0
        self.gradle_seconds   = 0
        
        new_fields = { "energy", "seconds", "n" }
        self.add_new_fields("maven", regex_maven.plugins, new_fields)
        self.add_new_fields("gradle", regex_gradle.plugins, new_fields)
    

    def update_build_manager (self, name, task):
        assert name == "maven" or name == "gradle", f"Invalid build manager {name}"
        #assert not self.bmanager or self.bmanager == name, f"Trying to change build manager from {self.bmanager} to {name}"
        energy = task["energy"]
        seconds = task["seconds"]
        if name == "maven":
            self.is_maven = True
            self.maven_energy += energy
            self.maven_seconds += seconds
        else:
            self.is_gradle = True
            self.gradle_energy += energy
            self.gradle_seconds += seconds


    def update_energy_time (self, task):
        seconds = task["seconds"]
        self.seconds += seconds

        if seconds == 0:
           self.null_time += 1

        energy = task["energy"]
        self.energy += energy

        if energy == 0:
            self.null_energy += 1


    def add_new_fields (self, prefix, mydict, fields):
        for k in mydict.keys():
            for field in fields:
                new_field = prefix + "_" + k + "_" + field
                setattr(self, new_field, 0)


    def update_subtasks (self, prefix, subtasks):
        for key, v in subtasks.items():
            for field, value in v.items():
                new_key = prefix + "_" + key + "_" + field
                self.update_field_aux(new_key, value)


    def update_field_aux (self, field, v):
        setattr(self, field, getattr(self, field) + v)


    def print_aux (self):
        return vars(self)

    #def __str__ (self):
    #    return "bola"
