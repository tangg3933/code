using IronPython.Hosting;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;

// Author: Nivin Jose Kovukunnel

namespace RunPythonScriptFromCS
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Execute python process...");
            Option1_ExecProcess();

            Console.WriteLine();

            //Console.WriteLine("Execute python IronPython...");
            //Option2_IronPython();

            Console.ReadKey();
        }

        static void Option1_ExecProcess()
        {
            // 1) Create Process Info
            var psi = new ProcessStartInfo();
            psi.FileName = @"D:\Shared components, tools and SDKs\Python37_64\python.exe";

            // 2) Provide script and arguments
            var script = @"C:\Users\nivin\Downloads\RunPythonScriptFromCS\DaysBetweenDates.py";
            var start = "2019-1-1";
            var end = "2019-1-22";

            psi.Arguments = $"\"{script}\" \"{start}\" \"{end}\"";

            // 3) Process configuration
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            // 4) Execute process and get output
            var errors = "";
            var results = "";

            using (var process = Process.Start(psi))
            {
                errors = process.StandardError.ReadToEnd();
                results = process.StandardOutput.ReadToEnd();
            }

            // 5) Display output
            Console.WriteLine("ERRORS:");
            Console.WriteLine(errors);
            Console.WriteLine();
            Console.WriteLine("Results:");
            Console.WriteLine(results);

        }


        static void Option2_IronPython()
        {
            // 1) Create engine
            var engine = Python.CreateEngine();

            // 2) Provide script and arguments
            var script = @"C:\Users\nivin\Downloads\RunPythonScriptFromCS\DaysBetweenDates.py";
            var source = engine.CreateScriptSourceFromFile(script);

            var argv = new List<string>();
            argv.Add("");
            argv.Add("2019-1-1");
            argv.Add("2019-1-22");

            engine.GetSysModule().SetVariable("argv", argv);
            

            // 3) Output redirect
            var eIO = engine.Runtime.IO;

            var errors = new MemoryStream();
            eIO.SetErrorOutput(errors, Encoding.Default);

            var results = new MemoryStream();
            eIO.SetOutput(results, Encoding.Default);

            // 4) Execute script
            var scope = engine.CreateScope();
            source.Execute(scope);

            // 5) Display output
            string str(byte[] x) => Encoding.Default.GetString(x);

            Console.WriteLine("ERRORS:");
            Console.WriteLine(str(errors.ToArray()));
            Console.WriteLine();
            Console.WriteLine("Results:");
            Console.WriteLine(str(results.ToArray()));

        }


    }

}


