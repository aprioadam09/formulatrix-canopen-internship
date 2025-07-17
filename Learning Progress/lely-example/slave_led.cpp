#include <lely/ev/loop.hpp>
#include <lely/io2/linux/can.hpp>
#include <lely/io2/posix/poll.hpp>
#include <lely/io2/sys/io.hpp>
#include <lely/io2/sys/sigset.hpp>
#include <lely/io2/sys/timer.hpp>
#include <lely/coapp/slave.hpp>
#include <iostream>

using namespace lely;

// ================== PERUBAHAN DIMULAI DI SINI ==================

// 1. Kita buat kelas kustom kita sendiri yang mewarisi sifat dari BasicSlave
class MySlave : public canopen::BasicSlave {
 public:
  // Gunakan constructor dari kelas induk (BasicSlave)
  using BasicSlave::BasicSlave;

 protected:
  // 2. Timpa (override) fungsi virtual OnWrite.
  // Fungsi ini akan dipanggil secara otomatis oleh Lely setiap kali Master
  // menulis data ke objek APAPUN di dalam slave ini.
  void
  OnWrite(uint16_t idx, uint8_t subidx) noexcept override {
    // Panggil dulu implementasi dari kelas induk, ini adalah praktik yang baik.
    BasicSlave::OnWrite(idx, subidx);

    // 3. Kita periksa apakah objek yang ditulis adalah objek kontrol LED kita (0x2000)
    if (idx == 0x2000) {
      try {
        // 4. Ambil nilai yang baru saja ditulis oleh Master dari Object Dictionary.
        // Sintaks (*this)[index][subindex] digunakan untuk mengakses OD.
        uint8_t value = (*this)[0x2000][0];

        // --- Di sini letak logika kustom Anda ---
        std::cout << "\n>>> Perintah Kontrol LED diterima: " << std::hex << (int)value << std::dec << " <<<\n";

        if (value & 0x01) {
          std::cout << "    LED 1: ON\n";
        } else {
          std::cout << "    LED 1: OFF\n";
        }
        if (value & 0x02) {
          std::cout << "    LED 2: ON\n";
        } else {
          std::cout << "    LED 2: OFF\n";
        }
        if (value & 0x04) {
          std::cout << "    LED 3: ON\n";
        } else {
          std::cout << "    LED 3: OFF\n";
        }
        std::cout << "---------------------------------\n";

      } catch (const std::exception& e) {
        // Tangani jika ada error saat membaca nilai dari OD
        std::cerr << "Error saat membaca nilai dari OD 0x2000: " << e.what() << std::endl;
      }
    }
  }
};

// ================== PERUBAHAN SELESAI DI SINI ==================


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

  // 5. Buat instance dari kelas kustom KITA (MySlave), bukan BasicSlave.
  // Pastikan nama file EDS ini ('eds/my_slave.eds') sesuai dengan nama file Anda.
  MySlave slave(timer, chan, "eds/my_slave.eds", "", 2);

  // Pendaftaran lambda yang sebelumnya menyebabkan error sudah dihapus.

  io::SignalSet sigset(poll, exec);
  sigset.insert(SIGHUP);
  sigset.insert(SIGINT);
  sigset.insert(SIGTERM);

  sigset.submit_wait([&](int /*signo*/) {
    sigset.clear();
    ctx.shutdown();
  });

  slave.Reset();

  loop.run();
  return 0;
}
