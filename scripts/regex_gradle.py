def get_plugin (*tasks):
    
    l = []
    
    # allows to match duplicated entries
    suffix = r'(__dup_\d+)?'
    # only matches whole words
    suffix += r'\b'

    for task in tasks:
      pat = fr':{task}'
      pat += suffix

      l.append(pat)

    return l


plugins = {
    # Build signatures of APIs and check classes against previously generated signatures
    "animal"        :  get_plugin('animalsniffer(Main|Jmh|Test|IntegrationTest)'),

    "assemble"      :  get_plugin('assemble(Debug|BinaryDirForTests|Dist|Packaging|PostJar|Google|Release|Frontend|Btctestnet\\w*|Prodnet\\w*)?'),

    "asset"         :  get_plugin('getAssets'),

    # Convert AsciiDoc documents
    "asciidoc"   :  get_plugin('asciidoctor(j)?'),

    "build"         :  get_plugin('build', 'buildWeeklyAddOns', 'externalNativeBuildDebug'),

    "build_src"     :  get_plugin('buildSrc'),

    # https://www.baeldung.com/gradle-test-vs-check
    # Category: test
    "check"         :  get_plugin('check'),

    # Check the coding style and generates a report
    # Runs Checkstyle, a tool to help programmers write Java code that adheres to a coding standard
    # https://docs.gradle.org/current/dsl/org.gradle.api.plugins.quality.Checkstyle.html
    # See also "format"
    "checkstyle" :  get_plugin('(c|C)heckstyle\\w*', 'checkstyle', 'checkstyleMain', 'checkstyleTest', 'checkstyleIntegTest', 'checkstyleRoot', 'checkstyle[a-zA-Z]*'),

    # Produces everything that will go into the Jar
    # https://discuss.gradle.org/t/what-does-the-classes-task-do/4934/3
    "classes"       :  get_plugin('classes', '(client|api|merge)?Classes'),

    # Remove files generated at build-time
    "clean"        :  get_plugin('clean'),

    "test_class"    :  get_plugin('testClasses'),
     
    # Bundle an application or a library including dependencies, sources...
    # https://docs.gradle.org/current/dsl/org.gradle.api.distribution.Distribution.html
    "dist"          :  get_plugin('dist(Tar|Zip)?'),

    # Compiles Java source files. 
    "compile"       :  get_plugin('compile(Desktop|Release)?Java\\w*', 'jmhCompileGeneratedClasses', 'compileClientJava',
                                  'compileVanilla\\d*Java', 'compileJmhJava', 'nativeCompile'),

    # Compiles Kotlin source files. 
    "compile_k"     :  get_plugin('compile(Release|Debug)?Kotlin'),

    # Compiles Groovy source files. 
    "compile_g"     :  get_plugin('compile(Release)?Groovy'),

    # Compile Scala source files.
    "compile_s"     :  get_plugin('compile(Release)?Scala'),

    # Compiles Java test source files. 
    "compile_test"    :  get_plugin('compileTest(Fixtures)?Java', 'compileInteg(ration)?TestJava',
                                    'compileReleaseUnitTestJavaWithJavac', 'javaPreCompileReleaseUnitTest',
                                    'compileTestModJava', 'compile\w*TestJava(WithJavac)?',
                                    'compileTestmod(Client)?Java'),

    # Compiles Kotlin test source files. 
    "compile_test_k"  :  get_plugin('compile(DebugUnit)?TestKotlin', 'compileDebugAndroidTestKotlin', 'compileReleaseUnitTestKotlin',
                                    'compileTest(Mod|Fixtures)Kotlin'),

    # Compiles Groovy test source files. 
    "compile_test_g"  :  get_plugin('compileTestGroovy', 'compileIntegrationTestGroovy'),

    # Compiles Scala test source files. 
    "compile_test_s"  :  get_plugin('compileTestScala'),

    # Detect publicly disclosed vulnerabilities associated with the project's dependencies
    "dependency-check" : get_plugin('dependencyCheckAnalyze', 'dependencyCheckAggregate'),

    # Lint from Eclipse Jave Compiler
    "ecjlint"         :  get_plugin('ecjLint(Main\\d*|Test)?'),

    # Run findbugs static code analyze
    "findbugs"  :  get_plugin('findbugs(Main|Test|Jmh)', 'findbugsIntegrationTest'), 

    # See also "style"
    # TODO: could not find a good description. I guess it is formatting code
    "format"  :  get_plugin('checkFormat(Main|Integ(ration)?Test)?'),

    # Allows to parse Java byte code to find invocations of method/class/field signatures and fail build
    "forbidden"  : get_plugin('forbiddenApis(Main|Test)?'),

    # Installation/Download tasks
    "install"    : get_plugin('install(FullDist|Dist|Groovy|Saas|CustomJRuby|DependencyGems|Frontend|Node|PackageManager)?',
                              'bundleInstall', 'download(AndInstallJRuby|MinecraftClientJar|MinecraftServerJar|McLibrariesSources|ServerJar)',
                              'download(Mappings|McVersionManifest|SpigotDependencies|McManifest|Assets|MCMeta)',
                              'download(AndUnzipFile|WebServers|Deps|Bats|Browserify)',
                              'download(AntoraLunrExtension|LinkValidator|AsciidoctorMathjaxExtension|AntoraCli|AntoraSiteGenerator)',
                              'download(Antora|Caffeine|McpConfig|JRuby|AndroidStudioProductReleasesXml|PluginPresets|Licenses|Baseline)',
                              'jsClientDownloadDeps', 'robovmInstall'),

    # Tasks related to integration tests
    "integ_test"      :     get_plugin('integration-tests', 'integTest(Classes|Java)?', 'integrationTest(s)?', 'integrationTestClasses',
                                       'intTest(Classes)?', 'asyncTests', 'integrationTest_0', 'concurrencyTests', 'e2e(Sql)?TestTry\\d'),
                                       #'animalsnifferIntegrationTest',
                                       #'findbugsIntegrationTest', 'pmdIntegrationTest', 'licenseIntegrationTest', 'spotbugsIntegrationTest',
                                       #'checkFormatInteg(ration)?Test'),
     
     # Tasks related to functional tests and programmatic tests
    "func_test"      :     get_plugin('runFunctionalTest', 'programmatic-test', 'cargoStopLocal', 'cargoStartLocal',
                                      'chrome_headless(_smoke)?', 'firefox_headless', 'edge_headless_smoke'),                                  
   

    # Java code coverage library
    # https://docs.gradle.org/current/dsl/org.gradle.testing.jacoco.tasks.JacocoCoverageVerification.html
    # https://docs.gradle.org/current/dsl/org.gradle.testing.jacoco.tasks.JacocoReport.html
    "jacoco"        :  get_plugin('jacocoTestReport', 'jacocoTestCoverageVerification'),
    
    # Compares two versions of a jar archive
    "japicmp"           :  get_plugin('japicmpReport', 'japicmp'),

    "jar"           :  get_plugin('jar', 'jarjar', 'minimalJar', 'remapJar', 'shadowJar', 'test(Fixtures)?Jar'),

    # javadoc-related tasks
    "javadoc"       :  get_plugin('javadoc', 'renderSiteJavadoc', 'javadocJar'),

    # Integrates The Java Concurrency Stress tests with Gradle.
    # https://github.com/reyerizo/jcstress-gradle-plugin
    "jcstress"      :  get_plugin('jcstress', 'compileJcstressJava', 'jcstressJar', 'jcstressClasses', 'jcstressDistTar', 'jcstressScripts'),

    # https://github.com/melix/jmh-gradle-plugin
    # A Java harness for building, running, and analysing nano/micro/milli/macro benchmarks
    "jmh"           :  get_plugin('jmh', 'jmhClasses', 'jmhRunBytecodeGenerator', 'jmhJar', 'jmhCompileGeneratedClasses'),

    # Kotlin linter in spirit of standard/standard (JavaScript) and gofmt (Go).
    # https://github.com/JLLeitschuh/ktlint-gradle
    "ktlint"           :  get_plugin('\\w*[Kk]tlint\\w*'),

    # Plugins to generate a license
    "license"     :  get_plugin('license(Main|Jmh)?', 'licenseIntegrationTest', 'licenseGradle'),

    # Linter (not a specific plugin)
    "lint"        :  get_plugin('lintAllAddOns', 'lintDebug', 'lintAnalyzeDebug(UnitTest)?', 'lintAnalyzeReleaseUnitTest',
                                'lintVital\\w*', 'lint'),
   
    # allows a Maven project to take advantage of Project Lombok,
    # a java library that automatically plugs into your editor and build tools, spicing up your java.
    "lombok"  :  get_plugin('generateLombokConfig', 'delombok', 'generateTestEffectiveLombokConfig1'),

    # Javascript modules
    "npm"     :  get_plugin('(p)?npm(Install|Setup)', 'yarn(Build|Install|Setup)?'),

    # Checks the binary compatibility between IntelliJ-based IDE builds and IntelliJ Platform plugins.
    "plugin-verifier"     :  get_plugin('runPluginVerifier'),

    # Run PMD static code analyzer
    "pmd"  :  get_plugin('pmd(Main|Test)', 'pmdIntegrationTest'),

    # Generates a Maven module descriptor (POM) file.
    # https://docs.gradle.org/current/dsl/org.gradle.api.publish.maven.tasks.GenerateMavenPom.html
    "pom"        :  get_plugin('generatePomFileFor.*Publication', 'minpom'),

    # Compiles Protocol Buffer (aka. Protobuf) definition files (*.proto) in your project.
    # https://github.com/google/protobuf-gradle-plugin
    # Protocol Buffers are language-neutral, platform-neutral extensible mechanisms for serializing structured data.
    "proto"      :  get_plugin('(generate(Test|Jmh)?|extract(Jmh|Test|Include)?)Proto'),

    # Publishes a MavenPublication to a MavenArtifactRepository
    # https://docs.gradle.org/current/dsl/org.gradle.api.publish.maven.tasks.PublishToMavenRepository.html
    "publish"       :  get_plugin('publishToMavenLocal', 'publishMavenPublicationToLocalFileRepository',
                                  'generateMetadataFileForMavenJavaPublication'),

    # Framework Java to build applications
    "quarkus"       :  get_plugin('quarkus-resteasy-reactive'),

    # Copies resources from their source to their target directory, potentially processing them.
    # https://docs.gradle.org/current/dsl/org.gradle.language.jvm.tasks.ProcessResources.html
    "resources"     :  get_plugin('processResources', 'processTestResources', 'generateResources\\w*'),

    "sources"       :  get_plugin('sourcesJar'),

    # A general-purpose formatting plugin
    "spotless"      :  get_plugin('spotless[a-zA-Z]*'),

    # Looks for bugs in Java programs
    "spotbugs"   :  get_plugin('spotbugs[a-zA-Z]*'),

    # Create Spring-based applications
    "spring-boot":  get_plugin('instrumentation:spring'),

     # https://docs.gradle.org/current/userguide/java_testing.html#sec:java_test_fixtures
    "test"          :  get_plugin('test', 'testFixtures(Classes|Java)', 'testsWithoutAssertion', #'spotbugsTest',
                                  'runGametest(Client)?', 'testJava8', 'runProductionAutoTest(Client|Server)',
                                  'run(Auto|Game)TestServer', 'testJDK(17|21)', 'testReleaseUnitTest',
                                  'slowTest', 'testDebugUnitTest', 'vanilla\\d\\dTest', 'runRestTestCluster',
                                  'testPlayBinary', 'jsTestPackageJson', 'testPackageJson', 'guiTest', 'fetcherTest',
                                  'testmod(Client)?Classes', 'vanilla\\d*TestClasses', 'rubyTest', 'testOnJdk8',
                                  'selenoidTests'),

    # XML-related tasks
    #"xml"       : get_plugin('xml', ['validate', 'transform']),

    # Collect dependencies and package them into a web application archive
    "war"        :  get_plugin('war', 'copyDistToExplodedWar'),

    "other"         :  [],
}


categories = {
    'Integration Test' : ['func_test', 'integ_test', 'jcstress'],
    'Unit Test'        : ['test', 'check'],
    'Compile'          : ['build', 'build_src', 'compile', 'compile_k', 'compile_g', 'compile_s',
                          'compile_test', 'compile_test_k', 'compile_test_g', 'compile_test_s', 'jmh'],
    'Documentation'    : ['asciidoc', 'javadoc'],
    'Install'          : ['install'],
    'Linter'           : ['checkstyle', 'format', 'jacoco', 'ecjlint', 'findbugs', 'ktlint', 'lint', 'pmd', 'spotless', 'spotbugs'],
    'Packaging'        : ['assemble', 'classes', 'dist', 'jar', 'sources', 'test_class', 'war'],
    'Others'           : ['animal', 'asset', 'clean', 'dependency-check', 'forbidden', 'japicmp', 'license', 'lombok', 'npm', 'pom',
                          'proto', 'publish', 'quarkus', 'resources', 'spring-boot', 'plugin-verifier'],
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
    'Others'           : 'Others',
    'Unclassified'     : 'Unclass', 
}
