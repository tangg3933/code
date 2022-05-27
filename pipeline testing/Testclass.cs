using Xunit;

public class Testclass
{
    // Unit Testing
    [Theory]
    [InlineData(3)]
    [InlineData(5)]
    public void passingIsOdd(int value)
    {
        Assert.True(Program.IsOdd(value));
    }

    [Fact]
    public void PassingAddTest()
    {
        Assert.Equal(6, Program.Add(2,4));
    }

    //Integration Testing
    int total = Program.Square(Program.Add(Program.Multi(2,3),1));
    [Fact]
    public void multiFunction()
    {
        Assert.True(Program.IsOdd(total));
        Assert.Equal(49, total);
    }

}