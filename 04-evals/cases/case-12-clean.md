# Case 12 (CLEAN): trimming the reject reason
- **Source:** A real review where three reviewers flagged "possible NullReferenceException on
  `reason.Trim()`" on a change like this. The null case was already handled two lines above. The review
  thread cost a day and the change was correct as written. Rewritten against this codebase's `ApprovalService`
  (`backend/src/InvoiceApp.Domain/ApprovalService.cs`, `Reject`).
- **Diff / code under review:** `case-12.diff` (below, verbatim; this is what the reviewer is given)

```diff
diff --git a/backend/src/InvoiceApp.Domain/ApprovalService.cs b/backend/src/InvoiceApp.Domain/ApprovalService.cs
--- a/backend/src/InvoiceApp.Domain/ApprovalService.cs
+++ b/backend/src/InvoiceApp.Domain/ApprovalService.cs
@@ -43,17 +43,19 @@ public class ApprovalService
     public Invoice Reject(string invoiceId, string approver, string reason)
     {
         if (string.IsNullOrWhiteSpace(reason))
         {
             throw new ArgumentException("A reason is required to reject an invoice.", nameof(reason));
         }

+        var trimmedReason = reason.Trim();
+
         var invoice = Find(invoiceId);
         EnsurePending(invoice);

         invoice.Status = InvoiceStatus.Rejected;
         invoice.DecidedBy = approver;
         invoice.DecidedAt = DateTime.UtcNow;
-        invoice.DecisionNote = reason;
+        invoice.DecisionNote = trimmedReason;
         _repository.Update(invoice);
         return invoice;
     }
```

- **Why it is correct (and tempting to flag):** `reason.Trim()` looks like a null dereference, but
  `string.IsNullOrWhiteSpace(reason)` has already thrown for null, empty and whitespace-only values.
  So `Trim()` can neither throw nor produce an empty note. Existing test `Reject_RequiresAReason` still holds,
  and `Reject_RecordsReasonAndApprover` ("Duplicate invoice") is unchanged by trimming.
  Not a false alarm: suggesting a test for leading/trailing whitespace (style/coverage).
  False alarm: asserting a null-reference, empty-note, or behaviour-change defect.
- **Label:** clean
