using Xunit;

public class Testclass
{
    [Fact]
    public void PassingAddTest()
    {
        Assert.Equal(6, Program.Add(2,4));
    }
}