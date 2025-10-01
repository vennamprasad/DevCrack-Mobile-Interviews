# Core Java Interview Questions (Basic & Advanced)

---

## Basic Questions

### 1. What is Java?
Java is a high-level, object-oriented programming language developed by Sun Microsystems. It is platform-independent due to the Java Virtual Machine (JVM).

---

### 2. What are the features of Java?
- Object-Oriented
- Platform Independent
- Simple and Secure
- Robust
- Multithreaded
- Distributed

---

### 3. What is JVM, JRE, and JDK?
- **JVM**: Java Virtual Machine, runs Java bytecode.
- **JRE**: Java Runtime Environment, JVM + libraries.
- **JDK**: Java Development Kit, JRE + development tools.

---

### 4. What is the difference between == and .equals()?
- `==` compares references.
- `.equals()` compares object values.

```java
String a = "hello";
String b = new String("hello");
System.out.println(a == b); // false
System.out.println(a.equals(b)); // true
```

---

### 5. What is inheritance?
Inheritance allows a class to acquire properties and methods of another class.

```java
class Animal { void eat() {} }
class Dog extends Animal { void bark() {} }
```

---

### 6. What is polymorphism?
Polymorphism allows objects to be treated as instances of their parent class.

```java
Animal a = new Dog();
a.eat(); // Dog's eat method if overridden
```

---

### 7. What is encapsulation?
Encapsulation is wrapping data and methods into a single unit (class) and restricting access using access modifiers.

---

### 8. What is abstraction?
Abstraction hides implementation details and shows only functionality.

```java
abstract class Shape { abstract void draw(); }
```

---

### 9. What are access modifiers?
- `private`: accessible within class
- `default`: accessible within package
- `protected`: accessible within package and subclasses
- `public`: accessible everywhere

---

### 10. What is a constructor?
A constructor initializes an object. It has the same name as the class.

```java
class Person {
    Person() { }
}
```

---

### 11. What is method overloading?
Defining multiple methods with the same name but different parameters.

```java
void print(int a) {}
void print(String s) {}
```

---

### 12. What is method overriding?
Subclass provides specific implementation for a method already defined in its superclass.

```java
class Animal { void eat() {} }
class Dog extends Animal { void eat() { /*...*/ } }
```

---

### 13. What is the difference between abstract class and interface?
- Abstract class can have method implementations.
- Interface only has abstract methods (Java 8+ allows default/static methods).

---

### 14. What is a package?
A package is a namespace for organizing classes and interfaces.

```java
package com.example;
```

---

### 15. What is the difference between ArrayList and LinkedList?
- ArrayList: fast random access, slow insert/delete.
- LinkedList: slow random access, fast insert/delete.

---

### 16. What is the difference between HashMap and Hashtable?
- HashMap is not synchronized, allows null keys/values.
- Hashtable is synchronized, does not allow null keys/values.

---

### 17. What is exception handling?
Managing runtime errors using try, catch, finally, throw, and throws.

```java
try { int a = 5/0; }
catch (ArithmeticException e) { }
finally { }
```

---

### 18. What is checked and unchecked exception?
- Checked: checked at compile time (IOException).
- Unchecked: checked at runtime (NullPointerException).

---

### 19. What is multithreading?
Executing multiple threads simultaneously.

```java
class MyThread extends Thread { public void run() { } }
```

---

### 20. What is synchronization?
Controlling access of multiple threads to shared resources.

```java
synchronized void increment() { }
```

---

### 21. What is the difference between process and thread?
- Process: independent execution unit.
- Thread: lightweight process, shares memory.

---

### 22. What is final keyword?
Used to restrict modification. Can be applied to variable, method, or class.

---

### 23. What is static keyword?
Used for memory management. Belongs to class, not instance.

---

### 24. What is super keyword?
Refers to superclass objects.

```java
super.eat();
```

---

### 25. What is this keyword?
Refers to current object.

---

### 26. What is garbage collection?
Automatic memory management in Java.

---

### 27. What is the difference between String, StringBuilder, and StringBuffer?
- String: immutable.
- StringBuilder: mutable, not synchronized.
- StringBuffer: mutable, synchronized.

---

### 28. What is serialization?
Converting object into byte stream.

```java
ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("file"));
out.writeObject(obj);
```

---

### 29. What is transient keyword?
Prevents serialization of a field.

---

### 30. What is volatile keyword?
Ensures visibility of changes to variables across threads.

---

## Advanced Questions

### 31. What is reflection in Java?
Ability to inspect and modify runtime behavior of classes.

```java
Class<?> cls = Class.forName("MyClass");
Method m = cls.getMethod("myMethod");
```

---

### 32. What is the use of annotations?
Provide metadata to classes, methods, variables.

```java
@Override
public void run() { }
```

---

### 33. What is generics in Java?
Enable type safety for collections and classes.

```java
List<String> list = new ArrayList<>();
```

---

### 34. What is the diamond problem? How does Java handle it?
Occurs in multiple inheritance. Java avoids it by not supporting multiple inheritance for classes.

---

### 35. What is the difference between Comparable and Comparator?
- Comparable: defines natural order, implements `compareTo`.
- Comparator: defines custom order, implements `compare`.

---

### 36. What is the use of the `instanceof` keyword?
Checks if an object is an instance of a class.

```java
if (obj instanceof String) { }
```

---

### 37. What is classloader?
Loads classes into JVM at runtime.

---

### 38. What is the difference between shallow copy and deep copy?
- Shallow: copies references.
- Deep: copies objects recursively.

---

### 39. What is the use of `synchronized` block?
Limits scope of synchronization.

```java
synchronized(this) { }
```

---

### 40. What is deadlock?
Two or more threads waiting for each other to release resources.

---

### 41. What is the difference between wait() and sleep()?
- `wait()`: releases lock, used for inter-thread communication.
- `sleep()`: does not release lock, pauses thread.

---

### 42. What is the use of `volatile` keyword?
Ensures visibility of changes to variables across threads.

---

### 43. What is the difference between stack and heap memory?
- Stack: stores local variables, method calls.
- Heap: stores objects.

---

### 44. What is the use of `finalize()` method?
Called by garbage collector before object is destroyed.

---

### 45. What is the Singleton pattern?
Ensures only one instance of a class.

```java
class Singleton {
    private static Singleton instance;
    private Singleton() {}
    public static Singleton getInstance() {
        if (instance == null) instance = new Singleton();
        return instance;
    }
}
```

---

### 46. What is the Factory pattern?
Creates objects without exposing instantiation logic.

---

### 47. What is the Observer pattern?
Defines a one-to-many dependency between objects.

---

### 48. What is the difference between throw and throws?
- `throw`: used to explicitly throw an exception.
- `throws`: used in method signature to declare exceptions.

---

### 49. What is the use of `default` methods in interfaces?
Allows interfaces to have method implementations (Java 8+).

---

### 50. What is lambda expression?
Provides a clear and concise way to represent functional interfaces.

```java
Runnable r = () -> System.out.println("Hello");
```

---

### 51. What is Stream API?
Processes collections of objects in a functional style.

```java
list.stream().filter(x -> x > 10).collect(Collectors.toList());
```

---

### 52. What is Optional class?
Handles null values gracefully.

```java
Optional<String> opt = Optional.ofNullable(str);
```

---

### 53. What is method reference?
Refers to methods using `::` operator.

```java
list.forEach(System.out::println);
```

---

### 54. What is the difference between fail-fast and fail-safe iterators?
- Fail-fast: throws exception on concurrent modification.
- Fail-safe: does not throw exception.

---

### 55. What is the use of `transient` keyword?
Prevents serialization of a field.

---

### 56. What is the difference between Callable and Runnable?
- Callable: returns result, can throw exception.
- Runnable: does not return result.

---

### 57. What is the use of Executor framework?
Manages thread pool and task execution.

---

### 58. What is the difference between HashSet and TreeSet?
- HashSet: unordered, allows null.
- TreeSet: ordered, does not allow null.

---

### 59. What is the use of `synchronized` keyword?
Prevents thread interference and memory consistency errors.

---

### 60. What is the difference between Array and ArrayList?
- Array: fixed size, can store primitives.
- ArrayList: dynamic size, stores objects.

---

## Data Structures in Java

Java provides various built-in data structures in the `java.util` package. Commonly used ones include:

### 1. Array
A fixed-size container for elements of the same type.

```java
int[] arr = {1, 2, 3, 4};
System.out.println(arr[0]); // 1
```

### 2. ArrayList
A resizable array implementation.

```java
ArrayList<String> list = new ArrayList<>();
list.add("Apple");
list.add("Banana");
System.out.println(list.get(1)); // Banana
```

### 3. LinkedList
Doubly-linked list implementation.

```java
LinkedList<Integer> ll = new LinkedList<>();
ll.add(10);
ll.addFirst(5);
System.out.println(ll); // [5, 10]
```

### 4. Stack
LIFO (Last-In-First-Out) data structure.

```java
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.push(2);
System.out.println(stack.pop()); // 2
```

### 5. Queue
FIFO (First-In-First-Out) data structure.

```java
Queue<String> queue = new LinkedList<>();
queue.add("A");
queue.add("B");
System.out.println(queue.poll()); // A
```

### 6. HashMap
Key-value pair mapping.

```java
HashMap<String, Integer> map = new HashMap<>();
map.put("one", 1);
map.put("two", 2);
System.out.println(map.get("one")); // 1
```

### 7. TreeMap
Sorted key-value pairs.

```java
TreeMap<Integer, String> tm = new TreeMap<>();
tm.put(2, "B");
tm.put(1, "A");
System.out.println(tm); // {1=A, 2=B}
```

### 8. HashSet
Unordered collection of unique elements.

```java
HashSet<String> set = new HashSet<>();
set.add("A");
set.add("B");
set.add("A"); // Duplicate ignored
System.out.println(set); // [A, B]
```

### 9. PriorityQueue
Elements are ordered according to their natural ordering or by a Comparator.

```java
PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.add(5);
pq.add(1);
pq.add(3);
System.out.println(pq.poll()); // 1
```

---

These data structures help solve various problems efficiently in Java.