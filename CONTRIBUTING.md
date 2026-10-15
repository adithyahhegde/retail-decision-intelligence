# Contributing

Use Python type hints for public functions, clear domain names and small functions.
Explain business assumptions near calculations. Avoid framework additions without a recorded
need. Add a failing regression test before a bug fix where practical, implement the fix,
then run relevant tests and the complete suite before a release. Preserve raw test output.

A review must check requirements, data grain, monetary units, joins/denominators, error
handling, data privacy, reproducibility and documentation. Passing tests are necessary but
not proof of analytical validity. Use hand-worked and adversarial cases.

Commit no real business data or secrets. New third-party dependencies require verified
package identity, license, supported version, justified purpose and a lock strategy.
Current application dependencies are Python's standard library only.
