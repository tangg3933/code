using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using PythonWrapper;

namespace ExampleProject
{
    class Program
    {
        static void Main(string[] args)
        {
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

            Console.ReadLine();
        }
    }
}
