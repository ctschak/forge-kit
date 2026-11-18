# Profile: Java

Loaded when detection returns `java`. Existing Maven/Gradle setup wins (`rules/quality.md` QG4, QG5).

| Kind | Prefer existing | Default if absent (propose, QG5) |
|---|---|---|
| build + test | `./mvnw verify` / `./gradlew check` | wrapper + JUnit 5 |
| lint / style | Checkstyle / Spotless config | Checkstyle (project style) or Spotless |
| static analysis | SpotBugs / PMD / Error Prone | SpotBugs on changed modules |
| integration | Testcontainers / existing ITs | Testcontainers for DB/queue boundaries |
| coverage | JaCoCo | JaCoCo report for changed-line check (QG6) |

| ID | Check |
|---|---|
| JV1 | Resources: `try-with-resources` for streams, connections, clients; no leaked executors. |
| JV2 | Concurrency: shared mutable state guarded or immutable; no blocking calls on reactive/event threads; executor sizing stated. |
| JV3 | Nullability: `Optional` for absent returns, annotations where the project uses them; no `null` collections. |
| JV4 | Transactions: boundaries at service layer; no remote calls inside DB transactions; isolation/locking stated for contended writes. |
| JV5 | Spring (if used): constructor injection; config via properties; no field injection; controller → service → repository boundaries kept. |
| JV6 | Exceptions: checked exceptions wrapped with context; no swallowed `catch` (CS4); API errors mapped per `rules/api-standards.md`. |
| JV7 | Generics / types: no raw types; no unchecked casts without reason. |
