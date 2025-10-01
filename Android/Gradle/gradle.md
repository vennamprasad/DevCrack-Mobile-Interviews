# Gradle Interview Questions (Basic & Advanced)

## Basic Questions

### 1. What is Gradle?
**Answer:**  
Gradle is an open-source build automation tool that supports multi-language development, primarily used for Java, Android, and Kotlin projects.

---

### 2. What are the advantages of using Gradle over other build tools?
**Answer:**  
Gradle offers incremental builds, build caching, flexible DSL (Groovy/Kotlin), and better performance compared to tools like Maven and Ant.

---

### 3. What is a build.gradle file?
**Answer:**  
It's the main configuration file for Gradle projects, written in Groovy or Kotlin DSL, specifying dependencies, plugins, and build logic.

---

### 4. How do you define dependencies in Gradle?
**Answer:**  
```groovy
dependencies {
    implementation 'com.google.guava:guava:31.0.1-jre'
}
```

---

### 5. What is a Gradle task?
**Answer:**  
A task is a single unit of work, such as compiling code or running tests, defined in the build script.

---

### 6. How do you create a custom Gradle task?
**Answer:**  
```groovy
task hello {
    doLast {
        println 'Hello, Gradle!'
    }
}
```

---

### 7. What is the difference between implementation and api configurations?
**Answer:**  
`implementation` hides dependencies from consumers, while `api` exposes them to modules that depend on your module.

---

### 8. How do you run a Gradle build?
**Answer:**  
Use the command:  
```bash
gradle build
```

---

### 9. What is the settings.gradle file used for?
**Answer:**  
It configures project structure, especially for multi-module projects.

---

### 10. How do you add a plugin in Gradle?
**Answer:**  
```groovy
plugins {
    id 'java'
}
```

---

## Intermediate Questions

### 11. What is the difference between build.gradle (project) and build.gradle (module)?
**Answer:**  
Project-level build.gradle configures global settings; module-level build.gradle configures specific module dependencies and tasks.

---

### 12. How do you exclude a transitive dependency?
**Answer:**  
```groovy
implementation('group:artifact:version') {
    exclude group: 'excluded-group', module: 'excluded-module'
}
```

---

### 13. What is Gradle Wrapper and why is it useful?
**Answer:**  
Gradle Wrapper (`gradlew`) ensures consistent Gradle version across environments, simplifying setup.

---

### 14. How do you define build variants in Android using Gradle?
**Answer:**  
```groovy
android {
    buildTypes {
        release { ... }
        debug { ... }
    }
}
```

---

### 15. How do you pass parameters to Gradle tasks?
**Answer:**  
```bash
gradle myTask -PmyParam=value
```
Access in script:  
```groovy
println project.property('myParam')
```

---

### 16. What is a multi-project build in Gradle?
**Answer:**  
A build containing multiple subprojects/modules, managed via `settings.gradle`.

---

### 17. How do you share code between modules in Gradle?
**Answer:**  
Create a common module and add it as a dependency in other modules.

---

### 18. How do you configure repositories in Gradle?
**Answer:**  
```groovy
repositories {
    mavenCentral()
    google()
}
```

---

### 19. How do you use Gradle properties?
**Answer:**  
Define in `gradle.properties` and access via `project.property('name')`.

---

### 20. How do you run a specific Gradle task?
**Answer:**  
```bash
gradle <taskName>
```

---

## Advanced Questions

### 21. How do you write a custom plugin in Gradle?
**Answer:**  
Create a class implementing `Plugin<Project>` and apply it in build.gradle.

```groovy
class MyPlugin implements Plugin<Project> {
    void apply(Project project) {
        project.task('customTask') {
            doLast {
                println 'Custom plugin task'
            }
        }
    }
}
```

---

### 22. What is build caching in Gradle?
**Answer:**  
Build caching stores outputs of tasks to avoid redundant work, improving build speed.

---

### 23. How do you enable parallel execution in Gradle?
**Answer:**  
Add to `gradle.properties`:  
```
org.gradle.parallel=true
```

---

### 24. How do you profile a Gradle build?
**Answer:**  
Run:  
```bash
gradle build --profile
```

---

### 25. How do you use annotation processors in Gradle?
**Answer:**  
```groovy
dependencies {
    annotationProcessor 'com.google.dagger:dagger-compiler:2.x'
}
```

---

### 26. How do you publish artifacts to a Maven repository using Gradle?
**Answer:**  
Use the `maven-publish` plugin and configure `publishing` block.

---

### 27. How do you configure test tasks in Gradle?
**Answer:**  
```groovy
test {
    useJUnitPlatform()
    testLogging {
        events "passed", "failed"
    }
}
```

---

### 28. How do you use conditional logic in build.gradle?
**Answer:**  
```groovy
if (project.hasProperty('release')) {
    // release-specific config
}
```

---

### 29. How do you integrate Gradle with CI/CD pipelines?
**Answer:**  
Use Gradle commands in CI scripts (Jenkins, GitHub Actions, etc.) for build, test, and deploy steps.

---

### 30. How do you debug Gradle build scripts?
**Answer:**  
Use `--debug` or `--stacktrace` flags:  
```bash
gradle build --debug
```

---

### 31. How do you use composite builds in Gradle?
**Answer:**  
Include builds using `includeBuild` in `settings.gradle` for dependency substitution.

---

### 32. How do you configure source sets in Gradle?
**Answer:**  
```groovy
sourceSets {
    main {
        java {
            srcDirs = ['src/main/java', 'src/shared/java']
        }
    }
}
```

---

### 33. How do you manage versioning in Gradle?
**Answer:**  
Set version in build.gradle:  
```groovy
version = '1.0.0'
```

---

### 34. How do you use environment variables in Gradle?
**Answer:**  
Access via `System.getenv('VAR_NAME')` in build scripts.

---

### 35. How do you use dependency constraints in Gradle?
**Answer:**  
```groovy
dependencies {
    constraints {
        implementation('org.example:lib:1.2.3')
    }
}
```

---

### 36. How do you configure custom outputs for tasks?
**Answer:**  
```groovy
task customOutput {
    outputs.file("$buildDir/custom.txt")
    doLast {
        file("$buildDir/custom.txt").text = "Hello"
    }
}
```

---

### 37. How do you use Gradle for non-Java projects?
**Answer:**  
Apply appropriate plugins (e.g., `cpp`, `python`) and configure tasks for the language.

---

### 38. How do you resolve dependency conflicts in Gradle?
**Answer:**  
Use `resolutionStrategy` in `configurations` block.

```groovy
configurations.all {
    resolutionStrategy {
        force 'group:artifact:version'
    }
}
```

---

### 39. How do you generate JAR/AAR files using Gradle?
**Answer:**  
Run `gradle jar` for Java or `gradle assembleRelease` for Android.

---

### 40. How do you use buildSrc for organizing build logic?
**Answer:**  
Create a `buildSrc` directory with custom plugins/tasks for reuse across the project.

---

*Feel free to ask for more details or code samples on any question!*