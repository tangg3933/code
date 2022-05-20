using Xunit;

public class Testclass
{
    [Fact]
    public void PassingAddTest()
    {
        Assert.Equal(5, Program.Add(2,4));
    }
}