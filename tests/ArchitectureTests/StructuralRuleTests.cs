using NetArchTest.Rules;
using Xunit;

namespace ArchitectureTests;

/// ONE structural rule, encoded as a test that runs.
/// Default rule: controllers must not touch the store directly; they go through the service.
/// Replace the TODO names after reading the real code (cite them in 01-architecture/citations.md).
/// Pick the rule that PayEx/persistence will most easily violate (e.g. nothing outside the
/// submission worker may reference the PayEx client).
public class StructuralRuleTests
{
    // TODO: any type from the assembly under test
    private static readonly System.Reflection.Assembly Api =
        typeof(Program).Assembly;

    [Fact]
    public void Controllers_must_not_depend_on_the_store_directly()
    {
        var result = Types.InAssembly(Api)
            .That().HaveNameEndingWith("Controller")
            .ShouldNot().HaveDependencyOn("TODO.Namespace.Of.Store") // TODO
            .GetResult();

        Assert.True(result.IsSuccessful,
            "Violations: " + string.Join(", ", result.FailingTypeNames ?? Array.Empty<string>()));
    }
}
