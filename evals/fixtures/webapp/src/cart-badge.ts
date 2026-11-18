// Cart badge shown on the header cart icon.
export interface Badge {
  visible: boolean;
  text: string;
}

export function cartBadge(count: number): Badge {
  return { visible: true, text: String(count) };
}
