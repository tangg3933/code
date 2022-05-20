using Xunit;

public class Testclass
{
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
}