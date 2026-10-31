# Case 11 (defective): retrying a payment POST on timeout
- **Source:** A payments integration I have worked on. A "make it resilient" change wrapped the
  provider call in a retry loop. The provider had accepted the first request but answered slowly, so the
  retry created a second payment. It was found by the provider's daily statement, not by our logs.
  Same shape as release 2.14.3 "Retry policy for the PayEx client" in `ops/incidents/INC-2047/recent-changes.md`.
  Sanitised and rewritten against this codebase's names.
- **Diff / code under review:** `case-11.diff` (below, verbatim; this is what the reviewer is given)

```diff
diff --git a/backend/src/InvoiceApp.Api/Clients/PayExClient.cs b/backend/src/InvoiceApp.Api/Clients/PayExClient.cs
--- a/backend/src/InvoiceApp.Api/Clients/PayExClient.cs
+++ b/backend/src/InvoiceApp.Api/Clients/PayExClient.cs
@@ -18,12 +18,29 @@ public class PayExClient : IPayExClient
     public async Task<PayExReceipt> SubmitAsync(Invoice invoice, CancellationToken ct = default)
     {
-        var response = await _http.PostAsJsonAsync("/v2/payments", Map(invoice), ct);
-        response.EnsureSuccessStatusCode();
-
-        return await response.Content.ReadFromJsonAsync<PayExReceipt>(cancellationToken: ct)
-               ?? throw new InvalidOperationException("PayEx returned an empty receipt.");
+        const int maxAttempts = 3;
+
+        for (var attempt = 1; ; attempt++)
+        {
+            try
+            {
+                var response = await _http.PostAsJsonAsync("/v2/payments", Map(invoice), ct);
+                response.EnsureSuccessStatusCode();
+
+                return await response.Content.ReadFromJsonAsync<PayExReceipt>(cancellationToken: ct)
+                       ?? throw new InvalidOperationException("PayEx returned an empty receipt.");
+            }
+            catch (Exception ex) when (attempt < maxAttempts &&
+                                       (ex is TaskCanceledException || ex is HttpRequestException))
+            {
+                _logger.LogWarning(ex, "PayEx submit attempt {Attempt} for {InvoiceId} failed; retrying",
+                    attempt, invoice.Id);
+                await Task.Delay(TimeSpan.FromSeconds(2 * attempt), ct);
+            }
+        }
     }
```

- **Expected finding:** The POST is not idempotent: no idempotency key or reference is sent, and a
  timeout (`TaskCanceledException`) does not mean PayEx rejected the payment. Retrying after a timeout can
  submit the same invoice two or three times, which means a duplicate payment.
  Secondary (does not count as caught on its own): a `TaskCanceledException` caused by the caller's `ct`
  is also retried, and the loop has no jitter.
- **Why it is realistic:** Retry-on-timeout around a non-idempotent call is the most common way
  "add resilience" PRs create duplicate money movement. The code looks careful: it has bounded attempts,
  filtered exceptions, backoff and logging.
- **Label:** defective
