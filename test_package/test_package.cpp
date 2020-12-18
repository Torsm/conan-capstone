#include "capstone/capstone.h"

int main() {
    csh handle;
    cs_open(CS_ARCH_X86, CS_MODE_64, &handle);
    cs_close(&handle);
}
