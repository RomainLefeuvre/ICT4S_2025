def get_plugin (name, goals, dev='maven'):
    
    assert isinstance(goals, list), "Must provide a list of goals"
    l = []
    
    for goal in goals:
      pat = fr'{dev}-{name}-plugin.*:{goal}'
      l.append(pat)

      pat = fr'{name}.*:{goal}'
      l.append(pat)

    return l


plugins = {
  # Build signatures of APIs and check classes against previously generated signatures
  "animal"     :  get_plugin('animal-sniffer', ['build', 'check']),

  # The ANTLR 4 plugin for Maven can generate parsers for any number of grammars in your project.
  'antlr4'     :  get_plugin('antlr4', ['antlr4']),

  # Provides the ability to run Ant tasks from within Maven
  "antrun"     :  get_plugin('antrun', ['run', 'help']),

  # This plugin may be used to run Rat, the Release Audit Tool.
  "apache-rat" :  get_plugin('apache-rat', ['check', 'rat']),
  
  # allows the user to create a Maven project from an existing template called an archetype (package phase).
  "archetype-jar" :  get_plugin('archetype', ['jar']),
  
  # allows the user to create a Maven project from an existing template called an archetype (integration-test phase).
  "archetype-int" :  get_plugin('archetype', ['integration-test']),
  
  # allows the user to create a Maven project from an existing template called an archetype (install phase).
  "archetype-update" :  get_plugin('archetype', ['update-local-catalog']),
  

  # Convert AsciiDoc documents
  "asciidoc"   :  get_plugin('asciidoctor', ['process-asciidoc', 'auto-refresh', 'http']),

  # Combine project output into a single distributable archive
  "assembly"   :  get_plugin('assembly', ['single']),

  # Seems similar to bundle (below)
  "bnd"       : get_plugin('bnd', ['bnd-process']),

  # Create jar files
  "bundle"    : get_plugin('bundle', ['bundle(all)?', 'wrap', 'manifest', 'install(-file)?',
                           'ant', 'deply(-file)?', '(remote-)?clean']),

  # Check the coding style and generates a report
  "checkstyle" :  get_plugin('checkstyle', ['checkstyle', 'check-aggregate', 'check']),

  # Remove files generated at build-time
  "clean"      :  get_plugin('clean', ['clean']),

  # Allows you to compare binaries or sources for compatibility
  "clirr"      : get_plugin('clirr', ['check', 'clirr', 'check-arbitrary', 'check-no-fork']),

  # Compile Java source code
  "compile"    :  get_plugin('compiler', ['compile']),

  # Compile Java test source files
  "testcomp"   :  get_plugin('compiler', ['testCompile']),

   # Executes Groovy scripts
  "groovy"  :  get_plugin('groovy', ['console', 'execute', 'shell']),

   # Executes Groovy scripts
  "gplus"  :  get_plugin('gplus', ['']),
  
  # Groovy integration for Maven
  "gmaven"  : get_plugin('gmaven', ['']), 

  # Groovy integration for Maven
  "gmavenplus"  : get_plugin('gmavenplus', ['']), 

   # Compile Kotlin source code
  "compile_k"  :  get_plugin('kotlin', ['compile', 'kapt']),

   # Compile Kotlin test source files
  "testcomp_k" :  get_plugin('kotlin', ['test-compile', 'test-kapt']),

   # Compile Scala source code
  "compile_s"  :  get_plugin('scala', ['compile']),

  # Compile Scala test source files
  "testcomp_s" :  get_plugin('scala', ['testCompile']),

  # Generate CycloneDX Software Bill of Materials (SBOM) containing the aggregate of all direct and transitive dependencies of a project
  "cyclone"   : get_plugin('cyclonedx', ['make(Aggregate|Package)?Bom']),

  # Copy and/or unpack artifacts from local or remote repositories to a specified location
  "dependency" :  get_plugin('dependency', ['analyze(-dep-mgt|-only|-report|-duplicate)?',
                                            'build-classpath', 'copy(-dependencies)?',
                                            'display-ancestors', 'get', 'go-offline',
                                            'list(-classes|-repositories)?',
                                            'resolve(-plugins|-sources)?',
                                            'sources', 'tree',
                                            'unpack(-dependencies)?']),

  # Detect publicly disclosed vulnerabilities associated with the project's dependencies
  "dependency-check" : get_plugin('dependency-check', ['aggregate', 'check', 'help', 'purge', 'only']),

  # Attempts to solve a scope problem related to Maven
  "dependency-scope" : get_plugin('dependency-scope', ['check']),

  # Add an artifact to a remote repository
  "deploy"   : get_plugin('deploy', ['deploy(file)?']),

  # Find and flag duplicate classes and resources on the java classpath.
  "duplicate-finder" : get_plugin('duplicate-finder', ['check']),

  # Control environmental constraints such as Maven version
  "enforcer"   :  get_plugin('enforcer', ['enforce']),

  # Help execute system and Java programs.
  "exec-maven" :  get_plugin('exec', ['exec', 'java']),

  # Run findbugs static code analyze
  "findbugs"   : get_plugin('findbugs', ['check', 'findbugs']),

  # Tun integration tests
  "failsafe"   : get_plugin('failsafe', ['integration-test', 'verify']),

  # Generates a flattened version of the pom.xml that Maven installs and deploys instead of the original.
  "flatten"   : get_plugin('flatten', ['flatten', 'clean']),

  # https://github.com/spotify/fmt-maven-plugin
  # Formats your code using google-java-format which follows Google's code styleguide.
  "fmt"        : get_plugin('fmt', ['format', 'check', ]),

  # Allows to parse Java byte code to find invocations of method/class/field signatures and fail build
  "forbidden"  : get_plugin('forbiddenapis', ['check', 'testCheck']),

  # Format Java source code using the Eclipse code formatter
  "formatter"  : get_plugin('formatter', ['format', 'validate']),

    # This plugin downloads/installs Node and NPM locally for your project, runs npm install, and then any combination of Bower, Grunt, Gulp, Jspm, Karma, or Webpack.                         
  "frontend"  :  get_plugin('frontend', ['install-node-and-p?npm', 'install-node-and-yarn', 'p?npm', 'npx', 'yarn', 'bower',
                                          'grunt', 'gulp', 'jspm', 'karma', 'webpack', 'bun', 'install-bun']),

  # Makes basic repository information available through maven resources.
  "git-commit-id" : get_plugin('git-commit-id', ['revision', 'validateRevision']),
  
  # Signs all of the project's attached artifacts with GnuPG
  "gpg"   :  get_plugin('gpg', ['sign(-and-deploy-file)?']),

  # Add artifacts to the local repository
  "install"   :  get_plugin('install', ['install']),

  # Sorts Java source file's import statements according to some rules.
  "impsort"   :  get_plugin('impsort', ['check', 'sort']),

  # Run a set of Maven projects
  "invoker"   :  get_plugin('invoker', ['help', 'install', 'integration-test', 'report', 'run', 'verify']),

  # Java code coverage library
  "jacoco"     :  get_plugin('jacoco', ['help', 'prepare-agent(-integration)?', 'merge', 'report(-integration|-aggregate)?',
                                        'check', 'dump', 'instrument', 'restore-instrumented-classes']),

  # Use Javadoc to generate javadocs for the project.
  "javadoc"    :  get_plugin('javadoc', ['(test-)?javadoc(-no-fork)?', '(test-)?aggregate(-no-fork)?',
                                         '(test-)?(aggregate-)?jar', '(test-)?fix', '(test-)?resource-bundle']),

  # Build jars
  "jar"        :  get_plugin('jar', ['(test-)?jar']),
  
   # Launches the JUnit Platform
  "junit"        :  get_plugin('junit-platform', ['launch']),
  
  # Manages the license of a maven project 
  "license"    :  get_plugin('license', ['(aggregate-)?add-third-party', 'comment-style-list', '(aggregate-)?download-licenses',
                             'license-list', '(update|check|remove)?-file-header', 'update-project-license',
                             # the following goals do not appear on the site, but they appear on the logs
                             'check', 'update', 'remove', 'format']),

  # allows a Maven project to take advantage of Project Lombok,
  # a java library that automatically plugs into your editor and build tools, spicing up your java.
  "lombok"  :  get_plugin('lombok', ['delombok']),

  # Run PMD static code analyzer
  "pmd"  :  get_plugin('pmd', ['(aggregate-)?pmd(-no-fork|-check)?', '(aggregate-)?cpd(-check)?']),
                               
  # Framework Java to build applications
  "quarkus"    :  get_plugin('quarkus', ['']),
  
  # An automated refactoring ecosystem for source code
  "rewrite"    :  get_plugin('rewrite', ['run', 'runNoFork', 'dryRun', 'dryRunNoFork', 'discover']),

  # Retrieve JARs of resources from remote repositories, process and incorporate them into JARs you build with Maven
  "remote"     :  get_plugin('remote-resources', ['process', 'aggregate']),

  # Handle the copying of project resources to the output director
  "resources"  :  get_plugin('resources', ['resources', 'testResources', 'copy-resources']),
  
   # Enables API checks during the Maven build
  "revapi"  :  get_plugin('revapi', ['check(-fork)?', 'convert-config-to-xml', 'report(-fork|-aggregate)?', 'update-(versions|release-properties)', 'validate-configuration']),
  
  # Scala related tasks other than compiling and testing
  "scala"      :  get_plugin('scala', ['add-source', 'doc(-jar)?', 'help', 'run', 'script']),

  # Package an artifact in an uber-jar
  "shade"      :  get_plugin('shade', ['shade']),

 # Generate a site for the project
  "site" :  get_plugin('site', ['(effective-)?site', 'deploy', 'run', 'stage(-deploy)?',
                             'attach-descriptor', 'jar']),

  # Create a jar archive of the source files of the current project
  "source"     :  get_plugin('source', ['aggregate', '(test-)?jar(-no-fork)?']),

   # A general-purpose formatting plugin
  "spotless"   :  get_plugin('spotless', ['apply', 'check']),

  # Looks for bugs in Java programs
  "spotbugs"   :  get_plugin('spotbugs', ['check', 'gui', 'help', 'spotbugs', 'verify']),

  # Create Spring-based applications
  "spring-boot":  get_plugin('spring-boot', ['build-image(-no-fork)?', 'build-info', 'process(-test)?-aot',
                                             'repackage', '(test-)?run', 'start', 'stop']),
  
  # Execute unit tests
  "surefire"   :  get_plugin('surefire', ['test']),
  
  # Creates the web interface version of the test results.
  "surefire-report"   :  get_plugin('surefire-report', ['report(-only)?', 'failsafe-report-only']),

  # Provides extensions to build Eclipse projects.
  "tycho-p2"        : get_plugin('tycho-p2', ['']),
  "tycho-compiler"  : get_plugin('tycho-compiler', ['']),
  "tycho-packaging" : get_plugin('tycho-packaging', ['']),

  # https://www.mojohaus.org/versions/versions-maven-plugin/index.html
  # The Versions Plugin is used when you want to manage the versions of artifacts in a project's POM.
  "versions"   :  get_plugin('versions', ['']),

  # XML-related tasks
  "xml"       : get_plugin('xml', ['validate', 'transform']),

  # Collect dependencies and package them into a web application archive
  "war"        :  get_plugin('war', ['war', 'exploded', 'inplace']),
  
  # Remove any trailing whitespace from .java, .xml and .scala files 
  "whitespace"       : get_plugin('whitespace', ['trim']),
  
  "other"      :   [],
}

categories = {
    'Integration Test' : ['archetype-int', 'failsafe'],
    'Unit Test'        : ['junit', 'surefire', 'surefire-report'],
    #'Ant'              : ['antrun'],
    'Compile'          : ['compile', 'testcomp', 'groovy', 'gplus', 'gmaven', 'gmavenplus',
                          'compile_k', 'testcomp_k', 'compile_s', 'testcomp_s', 'scala', 'tycho-compiler'],
    #'Dependency Check' : ['dependency-check'],
    'Documentation'    : ['asciidoc', 'javadoc', 'site'],
    'Install'          : ['archetype-update', 'install'],
    'Linter'           : ['checkstyle', 'findbugs', 'fmt', 'formatter', 'jacoco', 'pmd', 'rewrite', 'spotless', 'spotbugs', 'whitespace'],
    'Packaging'        : ['archetype-jar', 'assembly', 'bnd', 'bundle', 'jar', 'remote', 'source', 'tycho-packaging', 'war'],
    #'Privacy'          : ['gpg'],
    'Others'           : ['animal', 'antlr4', 'apache-rat', 'clean', 'clirr', 'cyclone', 'dependency', 'dependency-scope',
                          'deploy', 'duplicate-finder', 'enforcer', 'exec-maven', 'flatten', 'forbidden', 'frontend', 'git-commit-id',
                          'impsort', 'invoker', 'license', 'lombok', 'quarkus', 'resources', 'revapi', 'shade', 'spring-boot', 'tycho-p2',
                          'versions', 'xml', 'antrun', 'dependency-check', 'gpg'], 
    'Unclassified'     : ['other'],                      
}

categories_short = {
    'Integration Test' : 'Int Test',
    'Unit Test'        : 'Unit Test',
    'Ant'              : 'Ant',
    'Compile'          : 'Compile',
    'Dependency Check' : 'Dep Check',
    'Documentation'    : 'Doc',
    'Install'          : 'Install',
    'Linter'           : 'Linter',
    'Packaging'        : 'Pack',
    'Privacy'          : 'Privacy',
    'Others'           : 'Others',
    'Unclassified'     : 'Unclass', 
}
