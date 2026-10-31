using System;
using System.Reflection;
using InvoiceApp.Domain;
using NetArchTest.Rules;
using Xunit;

namespace ArchitectureTests;

/// Rule: InvoiceApp.Domain (approval rules) must not depend on the web host or on any I/O client.
/// PayEx (HTTP), Azure SQL (EF Core / SqlClient) and Service Bus are planned (ops/); when they land they
/// belong in an adapter behind an interface (as IInvoiceRepository already is), never inside ApprovalService.
/// INC-2041 is the failure this guards: a synchronous PayEx call wired straight into the approve path.
public class StructuralRuleTests
{
    private static readonly Assembly Domain = typeof(ApprovalService).Assembly;
    private static readonly Assembly Api = typeof(InvoiceApp.Api.InMemoryInvoiceRepository).Assembly;

    private static readonly string[] Forbidden =
    {
        "InvoiceApp.Api",
        "Microsoft.AspNetCore",
        "System.Net.Http",
        "Microsoft.EntityFrameworkCore",
        "Microsoft.Data.SqlClient",
        "Azure.Messaging.ServiceBus",
    };

    private static TestResult DomainRule(Assembly assembly) =>
        Types.InAssembly(assembly)
            .ShouldNot().HaveDependencyOnAny(Forbidden)
            .GetResult();

    [Fact]
    public void Domain_must_not_depend_on_web_host_or_io_clients()
    {
        var result = DomainRule(Domain);

        Assert.True(result.IsSuccessful,
            "Violations: " + string.Join(", ", result.FailingTypeNames ?? Array.Empty<string>()));
    }

    [Fact]
    public void Rule_detects_violations_when_they_exist()
    {
        var result = DomainRule(Api);

        Assert.False(result.IsSuccessful);
        Assert.Contains(result.FailingTypeNames!, n => n.EndsWith(".ApprovalsController"));
    }
}
