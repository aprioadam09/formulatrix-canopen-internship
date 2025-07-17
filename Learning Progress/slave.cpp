#include <lely/ev/loop.hpp>
#include <lely/io2/linux/can.hpp>
#include <lely/io2/posix/poll.hpp>
#include <lely/io2/sys/io.hpp>
#include <lely/io2/sys/sigset.hpp>
#include <lely/io2/sys/timer.hpp>
#include <lely/coapp/slave.hpp>

using namespace lely;

int main() {
    io::IoGuard io_guard;
    io::Context ctx;
    io::Poll poll(ctx);
    ev::Loop loop(poll.get_poll());
    auto exec = loop.get_executor();

    io::Timer timer(poll, exec, CLOCK_MONOTONIC);
    io::CanController ctrl("vcan0");
    io::CanChannel chan(poll, exec);
    chan.open(ctrl);

    canopen::BasicSlave slave(timer, chan, "eds/cpp-slave.eds", "", 2);

    io::SignalSet sigset(poll, exec);
    sigset.insert(SIGHUP);
    sigset.insert(SIGINT);
    sigset.insert(SIGTERM);

    sigset.submit_wait([&] (int /*sgino*/) {
        sigset.clear();
        ctx.shutdown();
    });

    slave.Reset();

    loop.run();
    return 0;
}