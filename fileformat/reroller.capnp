@0xb17f0a85bb0ffdb3;

struct Op {
    union {
        loadStore :group {
            dst @0 :UInt16;
            val @1 :UInt8;
        }
        call @2 :UInt32;
        yieldValue @3 :UInt8;
        yieldNone @4 :Void;
    }
}

struct Stream {
    ops @0 :List(Op);
}

struct Rule {
    ops @0 :List(Op);
}

struct File {
    streams @0 :List(Stream);
    rules @1 :List(Rule);
}