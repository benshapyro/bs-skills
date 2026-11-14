# Planted faults by stack

Read this when choosing faults for the Step 6 test. Pick one logic bug for push 1, a different one for push 2, and one house-rule violation that matches a rule actually written in the repo's rules file. Keep every fault small, obviously fake, and in a file nobody depends on (a new helper is easiest).

Don't plant real-looking secrets. A local hook or GitHub push protection may block them, which is a guard working. Note it and move on; never bypass a guard.

## Faults that work in any language

| Kind | Example | Why it's a fair test |
| --- | --- | --- |
| Off-by-one | A loop that reads one past the end, or skips the last item | Easy to see if the reviewer reads the code, easy to miss if it skims |
| Wrong condition | `>` where `>=` is meant; a filter that keeps what it should drop | Looks plausible; needs the intent understood |
| Empty input | Average or ratio with no guard for zero items | Caught an unplanted case of this on the first repo |
| Fix that doesn't fix | Commit says "handle empty list", code still crashes on it | Tests the push review's second rule |
| No test | New function with logic and no test, when the project has tests | Missed until a rule was written; then caught |

## By stack

| Stack | Logic faults | Security or platform smells |
| --- | --- | --- |
| TypeScript / JavaScript | `array.find` result used without a null check; `==` vs `===` coercion bug; unawaited promise in a loop | Token in a URL query string; `innerHTML` with user input |
| Python | Mutable default argument; integer division where a float was meant; `except: pass` swallowing a real error | SQL built with f-strings; `yaml.load` without a safe loader |
| Go | Ignored `err`; `defer resp.Body.Close()` before the error check; loop variable captured by a goroutine | Unbounded read of a request body |
| Dart / Flutter | `setState` or `context` used after an `await` without a `mounted` check; controller never disposed; `.first` or `.reduce` on a list that can be empty | API key in the app bundle; logging personal data |
| Swift / iOS | Force unwrap of an optional that can be nil; UI update off the main thread; retain cycle in a closure | Secret in `Info.plist`; disabled App Transport Security |
| Kotlin / Android | `!!` on a nullable that can be null; work on the main thread; leaked `Context` | Exported activity with no permission; unvalidated deep link |
| Java | `equals` vs `==` on strings; unclosed resource | String-built SQL |
| Ruby / Rails | `find_by` result used without nil check | Mass assignment without strong parameters |
| PHP | Loose comparison `==` with strings | Unescaped output; string-built SQL |
| SQL / migrations | Migration that drops a column still read by code | Missing index on a new foreign key |
| Infrastructure (Terraform, YAML) | Wrong resource reference | Public bucket; wildcard IAM permission |

## Reading the results

- A catch counts only if the comment names the fault and its cause, not just the line.
- If the full review catches a fault on push 1 and the push review flags it again on push 3, the push review is not scoping to the push; tighten its instruction.
- If the clean push (3) gets any comment, read it. A real finding is fine. "Looks good" means the instruction's silence line isn't being followed.
- Record misses as findings, and fix the most important one with a rule in the rules file before re-testing.
