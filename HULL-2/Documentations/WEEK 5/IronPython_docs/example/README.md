IronPythonDotNet35
==================

This is a wrapper for calling into Python code from C# in .Net 3.5. In .Net 4.0 and above, using the dynamic keyword makes it easy to call into Python without having to worry about types. However, if you have to use .Net 3.5 for any reason (like better XP support) this wrapper makes it easier to call Python code from C#.

Example usage:

```C#
// Compile script
PythonScript script = new PythonScript("example.py");

// Call top-level function
string returnValue = script.CallFunction<string>("get_string", "World");
Console.WriteLine(returnValue);

// Create Python object
PythonClass pyClass = script.GetClass("ExampleClass");
PythonObject pyObj = pyClass.Instantiate(5);

// Get property
int number = pyObj.GetProperty<int>("number");
Console.WriteLine("Number property is {0}", number);

// Get return value as Python object
PythonObject pyObj2 = pyObj.CallMethod("get_object");
int number2 = pyObj2.GetProperty<int>("number");
Console.WriteLine("Number property for 2nd object is {0}", number2);
```
