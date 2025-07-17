#include <lely/ev/loop.hpp>
#include <lely/io2/linux/can.hpp>
#include <lely/io2/posix/poll.hpp>
#include <lely/io2/sys/io.hpp>
#include <lely/io2/sys/sigset.hpp>
#include <lely/io2/sys/timer.hpp>
#include <lely/coapp/slave.hpp>
#include <iostream>

using namespace lely;

class Mydriver : public canopen::BasicSlave {
 public:
    using BasicSlave::BasicSlave;

 protected:
    void
    OnWrite(uint16_t idx, uint8_t subidx) noexcept override {
        BasicSlave::OnWrite(idx, subidx);

        if (idx == 0x2000) {
            try {
                uint8_t value = (*this)[0x2000][0];

                std::cout << "\n>>> Perintah Kontrol LED diterima: " << std::hex << (int)value << std::dec << " <<<\n";

                if (value & 0x01) {
                    std::cout << "      LED 1: ON\n";
                } else {
                    std::cout << "      LED 1: OFF\n";
                }
                if (value & 0x02) {
                    std::cout << "      LED 2: ON\n";
                } else {
                    std::cout << "      LED 2: OFF\n";
                }
                if (value & 0x04) {
                    std::cout << "      LED 3: ON\n";
                } else {
                    std::cout << "      LED 3: OFF\n";
                }
                std::cout << "------------------\n";
                
                this->TpdoEvent(1);

            } catch (const std::exception & e) {
                std::cerr << "Error saat membaca nilai dari OD 0x2000: " << e.what() << std::endl;
            }
        }
    }
};

int main() {
    io::IoGuard io_guard;
    io::Context ctx;
    io::Poll poll(ctx);
    ev::Loop loop(poll.get_poll());
    auto exec = loop.get_executor();

    io::Timer timer(poll, exec, CLOCK_MONOTONIC);
    io::CanController ctrl("can0");
    io::CanChannel chan(poll, exec);
    chan.open(ctrl);

    Mydriver slave(timer, chan, "my_slave.eds", "", 2);

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