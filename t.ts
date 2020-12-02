type D = [C, [string, string]];
type A = number /*int*/ | string | Deb | B | C | undefined;
type Deb = {
    a: number /*int*/;
    l: L;
};
type L = {
    p: string;
    j?: string | number /*int*/;
    l?: A;
    op: C;
};
type C = [number /*int*/, string];
type B = 1 | 2 | "3" | undefined;

let a: D = [[1, ""], ["", ""]];