using System;
using IronPython.Hosting;

// Author: Nivin Jose Kovukunnel

namespace PythonTest
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Demonstration using Python 3.9");
            var p1 = Python.CreateEngine();

            try
            {
                p1.ExecuteFile("C:\\Users\\nivin\\Desktop\\test.py");

            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            Console.ReadLine();
        }
    }
}
