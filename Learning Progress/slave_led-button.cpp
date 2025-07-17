#include <lely/ev/loop.hpp>
#include <lely/io2/linux/can.hpp>
#include <lely/io2/posix/poll.hpp>
#include <lely/io2/sys/io.hpp>
#include <lely/io2/sys/sigset.hpp>
#include <lely/io2/sys/timer.hpp>
#include <lely/coapp/slave.hpp>

#include <iostream>
#include <thread> // Diperlukan untuk threading

using namespace lely;

// Kelas kustom kita, sekarang kita sebut 'MySlave' untuk lebih jelas
class Mydriver : public canopen::BasicSlave {
public:
    using BasicSlave::BasicSlave;

    void SimulateButtonPress() {
        // Ambil nilai status tombol saat ini, lalu naikkan
        uint8_t current_value = this->Get<uint8_t>(0x2001, 0);
        uint8_t new_value = current_value + 1;

        // Simpan nilai baru ke Kamus Objek
        this->Set<uint8_t>(0x2001, 0, new_value);

        std::cout << "\n>>> [Tombol Ditekan!] Mengirim laporan (TPDO 2)... <<<\n" << std::endl;

        // Memicu pengiriman TPDO ke-2 untuk melaporkan penekanan tombol
        this->TpdoEvent(2);
    }

protected:
    // Event handler saat Master menulis ke OD
    void OnWrite(uint16_t idx, uint8_t subidx) noexcept override {
        BasicSlave::OnWrite(idx, subidx);

        if (idx == 0x2000) { // Logika untuk LED
            try {
                uint8_t value = (*this)[0x2000][0];
                std::cout << "\n>>> Perintah Kontrol LED diterima: " << (int)value << " <<<\n";
                // ... (logika if/else untuk status LED) ...
                std::cout << "---------------------------------\n";
                this->TpdoEvent(1); // Kirim laporan status LED (TPDO 1)
            } catch (const std::exception& e) {
                std::cerr << "Error: " << e.what() << std::endl;
            }
        }
    }
};

void button_simulation_thread(Mydriver& slave) {
    std::cout << "\n*** Simulasi Tombol Aktif ***" << std::endl;
    std::cout << "Tekan [Enter] di terminal ini untuk mensimulasikan penekanan tombol." << std::endl;

    while (true) {
        std::cin.get(); // Menunggu pengguna menekan Enter

        // Panggil fungsi publik yang sudah kita buat
        slave.SimulateButtonPress();
    }
}

int main() {
    io::IoGuard io_guard;
    io::Context ctx;
    io::Poll poll(ctx);
    ev::Loop loop(poll.get_poll());
    auto exec = loop.get_executor();

    io::Timer timer(poll, exec, CLOCK_MONOTONIC);
    io::CanController ctrl("can0"); // Menggunakan adapter fisik
    io::CanChannel chan(poll, exec);
    chan.open(ctrl);

    Mydriver slave(timer, chan, "eds/my_slave.eds", "", 2);

    io::SignalSet sigset(poll, exec);
    sigset.insert(SIGHUP);
    sigset.insert(SIGINT);
    sigset.insert(SIGTERM);

    sigset.submit_wait([&] (int /*sgino*/) {
        sigset.clear();
        ctx.shutdown();
    });

    slave.Reset();

    // Jalankan thread untuk simulasi tombol
    std::thread button_thread(button_simulation_thread, std::ref(slave));
    button_thread.detach(); // Lepaskan thread agar berjalan di latar belakang

    loop.run();
    return 0;
}