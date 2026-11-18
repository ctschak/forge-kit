// Project lint (no deps): fails on debug logging and `any` in src/.
import { readdirSync, readFileSync } from "node:fs";
let problems = 0;
for (const f of readdirSync("src")) {
  readFileSync(`src/${f}`, "utf8").split("\n").forEach((line, i) => {
    if (/console\.log\(/.test(line)) { console.log(`src/${f}:${i + 1} no-console: remove debug logging`); problems++; }
    if (/:\s*any\b/.test(line)) { console.log(`src/${f}:${i + 1} no-explicit-any: use unknown + narrowing`); problems++; }
  });
}
console.log(`${problems} problem(s)`);
process.exit(problems ? 1 : 0);
