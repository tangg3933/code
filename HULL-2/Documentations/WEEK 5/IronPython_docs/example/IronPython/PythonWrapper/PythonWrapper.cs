using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;

using IronPython.Hosting;
using IronPython.Runtime;
using IronPython.Runtime.Exceptions;
using IronPython.Runtime.Types;

using Microsoft.Scripting;
using Microsoft.Scripting.Hosting;

namespace PythonWrapper
{
    #region Exception classes

    public class PythonException : Exception
    {
        public PythonException()
        {
        }
        public PythonException(string message)
            : base(message)
        {
        }
        public PythonException(string message, Exception inner)
            : base(message, inner)
        {
        }
    }

    public class MissingMemberException : PythonException
    {
        public MissingMemberException()
        {
        }
        public MissingMemberException(string message)
            : base(message)
        {
        }
        public MissingMemberException(string message, Exception inner)
            : base(message, inner)
        {
        }
    }

    public class IncorrectParametersException : PythonException
    {
        public IncorrectParametersException()
        {
        }
        public IncorrectParametersException(string message)
            : base(message)
        {
        }
        public IncorrectParametersException(string message, Exception inner)
            : base(message, inner)
        {
        }
    }

    public class ScriptNotFoundException : PythonException
    {
        public ScriptNotFoundException()
        {
        }
        public ScriptNotFoundException(string message)
            : base(message)
        {
        }
        public ScriptNotFoundException(string message, Exception inner)
            : base(message, inner)
        {
        }
    }

    public class CompileErrorException : PythonException
    {
        public CompileErrorException()
        {
        }
        public CompileErrorException(string message)
            : base(message)
        {
        }
        public CompileErrorException(string message, Exception inner)
            : base(message, inner)
        {
        }
    }

    #endregion

    /// <summary>
    /// Provides access to a Python class.
    /// </summary>
    public class PythonClass
    {
        private string _className;
        private PythonType _type;
        private ObjectOperations _op;

        /// <summary>
        /// Create PythonClass object.
        /// </summary>
        /// <param name="className">Name of class.</param>
        /// <param name="scope">Script scope.</param>
        public PythonClass(string className, ScriptScope scope)
        {
            if (scope.ContainsVariable(className))
            {
                _className = className;
                _type = scope.GetVariable(className) as PythonType;
                PythonEngine engine = PythonEngine.Instance;
                _op = engine.Operations;
            }
            else
            {
                string message = String.Format("Class does not exist: {0}", className);
                Trace.TraceError(message);
                throw new MissingMemberException(message);
            }
        }

        /// <summary>
        /// Instantiate a Python object.
        /// </summary>
        /// <param name="parameters">Parameters to pass to constructor.</param>
        /// <returns>Python object.</returns>
        public PythonObject Instantiate(params object[] parameters)
        {
            try
            {
                // Invoke constructor in Python
                object instance = _op.Invoke(_type, parameters);
                return new PythonObject(instance);
            }
            catch (TypeErrorException e)
            {
                string message = String.Format("Incorrect parameters specified for {0} constructor", _className);
                Trace.TraceError(message);
                throw new IncorrectParametersException(message, e);
            }
        }

        /// <summary>
        /// Calls a static method defined in the class. This should be used when you expect the method to return a Python object.
        /// </summary>
        /// <param name="methodName">Method name.</param>
        /// <param name="parameters">Parameters to pass to method.</param>
        /// <returns>Object returned by method.</returns>
        public PythonObject CallStaticMethod(string methodName, params object[] parameters)
        {
            object result = InternalCallStaticMethod(methodName, parameters);
            if (result == null)
                return null;
            return new PythonObject(result);
        }

        /// <summary>
        /// Calls a static method defined in the class. This should be used when you expect the method to return a C# object.
        /// </summary>
        /// <typeparam name="T">Type of object returned by method.</typeparam>
        /// <param name="methodName">Method name.</param>
        /// <param name="parameters">Parameters to pass to method.</param>
        /// <returns>Object returned by method.</returns>
        public T CallStaticMethod<T>(string methodName, params object[] parameters)
        {
            object result = InternalCallStaticMethod(methodName, parameters);
            if (result == null)
                return default(T);
            return (T)result;
        }

        // Helper method used by CallStaticMethod
        private object InternalCallStaticMethod(string methodName, params object[] parameters)
        {
            // Call method in Python
            if (_op.ContainsMember(_type, methodName))
            {
                try
                {
                    PythonFunction function = _op.GetMember(_type, methodName) as PythonFunction;
                    return _op.Invoke(function, parameters);
                }
                catch (TypeErrorException e)
                {
                    string message = String.Format("Incorrect parameters specified for static method {0} in class {1}", methodName, _className);
                    Trace.TraceError(message);
                    throw new IncorrectParametersException(message, e);
                }
            }
            else
            {
                string message = String.Format("Static method {0} does not exist in class {1}", methodName, _className);
                Trace.TraceError(message);
                throw new MissingMemberException(message);
            }
        }
    }

    /// <summary>
    /// Provides access to a Python object.
    /// </summary>
    public class PythonObject
    {
        private object _instance;
        private ObjectOperations _op;

        /// <summary>
        /// Create Python object.
        /// </summary>
        /// <param name="instance">Python object instance.</param>
        public PythonObject(object instance)
        {
            _instance = instance;
            PythonEngine engine = PythonEngine.Instance;
            _op = engine.Operations;
        }

        /// <summary>
        /// Call method on Python object. This should be used when you expect the method to return a Python object.
        /// </summary>
        /// <param name="methodName">Method name.</param>
        /// <param name="parameters">Parameters to pass to method.</param>
        /// <returns>Object returned by method.</returns>
        public PythonObject CallMethod(string methodName, params object[] parameters)
        {
            object result = InternalCallMethod(methodName, parameters);
            if (result == null)
                return null;
            return new PythonObject(result);
        }

        /// <summary>
        /// Call method on Python object. This should be used when you expect the method to return a C# object.
        /// </summary>
        /// <typeparam name="T">Type of object returned by method.</typeparam>
        /// <param name="methodName">Method name.</param>
        /// <param name="parameters">Parameters to pass to method.</param>
        /// <returns>Object returned by method.</returns>
        public T CallMethod<T>(string methodName, params object[] parameters)
        {
            object result = InternalCallMethod(methodName, parameters);
            if (result == null)
                return default(T);
            return (T)result;
        }

        /// <summary>
        /// Gets property from Python object. This should be used when you expect the method to return a Python object.
        /// </summary>
        /// <param name="propertyName">Property name.</param>
        /// <returns>Python property.</returns>
        public PythonObject GetProperty(string propertyName)
        {
            if (_op.ContainsMember(_instance, propertyName))
            {
                object result = _op.GetMember(_instance, propertyName);
                if (result == null)
                    return null;
                return new PythonObject(result);
            }
            else
            {
                throw new MissingMemberException(String.Format("Property {0} does not exist", propertyName));
            }
        }

        /// <summary>
        /// Gets property from Python object.
        /// </summary>
        /// <typeparam name="T">Type of property. This should be used when you expect the method to return a (C#) object.</typeparam>
        /// <param name="propertyName">Property name.</param>
        /// <returns>Python property.</returns>
        public T GetProperty<T>(string propertyName)
        {
            if (_op.ContainsMember(_instance, propertyName))
            {
                object result = _op.GetMember(_instance, propertyName);
                if (result == null)
                    return default(T);
                return (T)result;
            }
            else
            {
                string message = String.Format("Property {0} does not exist", propertyName);
                Trace.TraceError(message);
                throw new MissingMemberException(message);
            }
        }

        // Helper method used by CallMethod
        private object InternalCallMethod(string methodName, params object[] parameters)
        {
            // Call method in Python
            if (_op.ContainsMember(_instance, methodName))
            {
                Method method = _op.GetMember(_instance, methodName) as Method;
                return _op.Invoke(method, parameters);
            }
            else
            {
                string message = String.Format("Method {0} does not exist", methodName);
                Trace.TraceError(message);
                throw new MissingMemberException(message);
            }
        }
    }

    /// <summary>
    /// Provides access to a Python script.
    /// </summary>
    public class PythonScript
    {
        private ScriptSource _source;
        private CompiledCode _code;
        private ScriptScope _scope;
        private ObjectOperations _op;

        /// <summary>
        /// Create Python script.
        /// </summary>
        /// <param name="scriptPath">Path to script.</param>
        public PythonScript(string scriptPath)
        {
            if (File.Exists(scriptPath))
            {
                PythonEngine engine = PythonEngine.Instance;
                _source = engine.Engine.CreateScriptSourceFromFile(scriptPath);

                try
                {
                    Trace.TraceInformation(String.Format("Compiling source code for {0}", scriptPath));
                    _code = _source.Compile();
                }
                catch (SyntaxErrorException e)
                {
                    string message = String.Format("Could not compile {0}: {1}", scriptPath, e.Message);
                    Trace.TraceInformation(message);
                    throw new CompileErrorException(message, e);
                }

                _scope = engine.Engine.CreateScope();
                _code.Execute(_scope);
                _op = engine.Operations;
                Trace.TraceInformation(String.Format("Source code for {0} has been compiled", scriptPath));
            }
            else
            {
                string message = String.Format("Script could not be found: {0}", scriptPath);
                Trace.TraceError(message);
                throw new ScriptNotFoundException(message);
            }
        }

        /// <summary>
        /// Get access to a class defined in script.
        /// </summary>
        /// <param name="className">Class name.</param>
        /// <returns>PythonClass object.</returns>
        public PythonClass GetClass(string className)
        {
            if (_scope.ContainsVariable(className))
                return new PythonClass(className, _scope);
            return null;
        }

        /// <summary>
        /// Calls a global function defined in the script. This should be used when you expect the method to return a Python object.
        /// </summary>
        /// <param name="functionName">Function name.</param>
        /// <param name="parameters">Parameters to pass to function.</param>
        /// <returns>Object returned by function.</returns>
        public PythonObject CallFunction(string functionName, params object[] parameters)
        {
            object result = InternalCallFunction(functionName, parameters);
            if (result == null)
                return null;
            return new PythonObject(result);
        }

        /// <summary>
        /// Calls a global function defined in the script. This should be used when you expect the method to return a C# object.
        /// </summary>
        /// <param name="functionName">Function name.</param>
        /// <param name="parameters">Parameters to pass to function.</param>
        /// <returns>Object returned by function.</returns>
        public T CallFunction<T>(string functionName, params object[] parameters)
        {
            object result = InternalCallFunction(functionName, parameters);
            if (result == null)
                return default(T);
            return (T)result;
        }

        // Helper method used by CallFunction
        private object InternalCallFunction(string functionName, params object[] parameters)
        {
            // Call function in Python
            if (_scope.ContainsVariable(functionName))
            {
                PythonFunction function = _scope.GetVariable(functionName) as PythonFunction;
                return _op.Invoke(function, parameters);
            }

            return null;
        }
    }

    /// <summary>
    /// Singleton wrapper class for Python engine.
    /// </summary>
    public class PythonEngine
    {
        private static PythonEngine _instance;

        private ScriptEngine _scriptEngine;
        private ObjectOperations _operations;

        /// <summary>
        /// Create Python Engine.
        /// </summary>
        private PythonEngine()
        {
            Trace.TraceInformation("Creating Python engine");

            var options = new Dictionary<string, object>()
            {
                { "Debug", true }   // Enable breakpoints to be set in Python script
            };
            _scriptEngine = Python.CreateEngine(options);
            _operations = _scriptEngine.Operations;
        }

        /// <summary>
        /// Get Python engine instance.
        /// </summary>
        public static PythonEngine Instance
        {
            get
            {
                if (_instance == null)
                    _instance = new PythonEngine();
                return _instance;
            }
        }

        /// <summary>
        /// Get Script engine instance.
        /// </summary>
        public ScriptEngine Engine
        {
            get
            {
                return _scriptEngine;
            }
        }

        /// <summary>
        /// Get Object operations instance.
        /// </summary>
        public ObjectOperations Operations
        {
            get
            {
                return _operations;
            }
        }
    }
}
