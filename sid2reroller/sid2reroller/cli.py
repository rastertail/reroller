import capnp

def main():
    reroller_capnp = capnp.load("../fileformat/reroller.capnp")

    file_data = reroller_capnp.File.new_message()
    streams = file_data.init_resizable_list("streams")
    stream = streams.add()
    stream_ops = stream.init_resizable_list("ops")

    op = stream_ops.add()
    op.loadStore.dst = 0xd400
    op.loadStore.val = 0x00

    op = stream_ops.add()
    op.loadStore.dst = 0xd401
    op.loadStore.val = 0x01

    op = stream_ops.add()
    op.loadStore.dst = 0xd402
    op.loadStore.val = 0x02

    op = stream_ops.add()
    op.yieldValue = 0xff

    stream_ops.finish()
    streams.finish()

    file = open("out.rr", "w+b")
    file_data.write(file)
