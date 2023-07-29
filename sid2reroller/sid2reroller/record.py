"""
Trace SID writes into Reroller streams
"""

import capnp

reroller_capnp = capnp.load("../fileformat/reroller.capnp")


class SidRecorder:
    """
    Trace and record SID writes
    """

    def __init__(self):
        # TODO Multiple SIDs

        self.memory = [0x00] * 0x10000
        self.pending_delays = [-1] * 4

        self.data = reroller_capnp.File.new_message()
        stream_container = self.data.init("streams", 4)
        self.streams = list(
            map(lambda c: c.init_resizable_list("ops"), stream_container)
        )

        self.data.init("rules", 0)
        self.data.weights.loadWeight = 2
        self.data.weights.storeWeight = 2
        self.data.weights.callWeight = 3
        self.data.weights.yieldWeight = 3
        self.data.weights.ruleWeight = 1

    def __getitem__(self, k):
        return self.memory[k]

    def __setitem__(self, k, v):
        if isinstance(k, int):
            if k in range(0xD400, 0xD41D):
                reg = k - 0xD400
                stream = reg // 7
                ofs = reg % 7

                if self.pending_delays[stream] > -1:
                    self.streams[stream].add().load = self.pending_delays[stream]
                    self.streams[stream].add().coyield = None

                    self.pending_delays[stream] = -1

                self.streams[stream].add().load = v
                self.streams[stream].add().store = ofs

            self.memory[k] = v
        else:
            for x, y in zip(range(65536)[k], v):
                self[x] = y

    def new_frame(self):
        """
        Split register writes into a new frame
        """

        for i, _ in enumerate(self.pending_delays):
            self.pending_delays[i] += 1

    def finish(self) -> bytes:
        """
        Finish writing to streams and return the Reroller input data
        """

        for s in self.streams:
            s.finish()

        return self.data.to_bytes_packed()
