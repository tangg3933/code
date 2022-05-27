using System;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello World");
        Console.WriteLine(Add(2,3));
        Console.WriteLine(IsOdd(5));
    }

    public static int Add(int x, int y)
    {
        return x+y;
    }

    public static int Square(int x)
    {
        return x*x;
    }

    public static int Multi(int x, int y)
    {
        return x*y;
    }

    public static bool IsOdd(int value)
    {
        return value % 2 == 1;
    }
}
