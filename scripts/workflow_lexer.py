def is_maven_task (name):
    prefix = "##[group]Run mvn"
    if name.startswith(prefix):
        return True
    
    prefix = "##[group]Run ./mvnw"
    if name.startswith(prefix):
        return True
    
    return False


def is_gradle_task (name):
    prefix = "##[group]Run gradle"
    if name.startswith(prefix):
        return True
    
    prefix = "##[group]Run ./gradlew"
    if name.startswith(prefix):
        return True
    
    return False


def is_maven_subtask (name):
    prefix = "[INFO] --- "
    return prefix in name


def is_gradle_subtask (name):
    prefix = "> Task :"
    return prefix in name


def is_gradle_autosubtask (name):
    prefix = "[autobuild] > "
    return prefix in name



def is_autobuild_task (name):
    prefix = "##[group]Attempting to automatically build java code"
    return name.startswith(prefix)