type A = number /*int*/ | string | Deb | B | undefined;
type Deb  = {
        a: number /*int*/;
        l: L;
};
type L  = {
        p: string;
        j?: string | number /*int*/;
        l?: A;
};
type B = 1 | 2 | "3" | undefined;