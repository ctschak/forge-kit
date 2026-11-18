import { test } from "node:test";
import assert from "node:assert/strict";
import { cartBadge } from "../src/cart-badge.ts";

test("shows the item count", () => {
  assert.deepEqual(cartBadge(3), { visible: true, text: "3" });
});
