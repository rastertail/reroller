@0xb17f0a85bb0ffdb3;

struct Op {
    union {
        load @0: UInt32;
        store @1: UInt32;
        call @2 :UInt32;
        coyield @3 :Void;
    }
}

struct Stream {
    ops @0 :List(Op);
}

struct Rule {
    ops @0 :List(Op);
}

struct Weights {
    loadWeight @0 :UInt32;
    storeWeight @1 :UInt32;
    callWeight @2 :UInt32;
    yieldWeight @3 :UInt32;
    ruleWeight @4 :UInt32;
}

struct File {
    streams @0 :List(Stream);
    rules @1 :List(Rule);
    weights @2 :Weights;
}