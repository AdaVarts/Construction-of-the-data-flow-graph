# 1 "F:/STU/FIIT/BP/Present.c"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "F:/STU/FIIT/BP/Present.c"
# 9 "F:/STU/FIIT/BP/Present.c"
# 1 "f:/STU/FIIT/BP/practical/fake_libc_include/stdio.h" 1
# 1 "f:/STU/FIIT/BP/practical/fake_libc_include/_fake_defines.h" 1
# 2 "f:/STU/FIIT/BP/practical/fake_libc_include/stdio.h" 2
# 1 "f:/STU/FIIT/BP/practical/fake_libc_include/_fake_typedefs.h" 1



typedef int size_t;
typedef int __builtin_va_list;
typedef int __gnuc_va_list;
typedef int va_list;
typedef int __int8_t;
typedef int __uint8_t;
typedef int __int16_t;
typedef int __uint16_t;
typedef int __int_least16_t;
typedef int __uint_least16_t;
typedef int __int32_t;
typedef int __uint32_t;
typedef int __int64_t;
typedef int __uint64_t;
typedef int __int_least32_t;
typedef int __uint_least32_t;
typedef int __s8;
typedef int __u8;
typedef int __s16;
typedef int __u16;
typedef int __s32;
typedef int __u32;
typedef int __s64;
typedef int __u64;
typedef int _LOCK_T;
typedef int _LOCK_RECURSIVE_T;
typedef int _off_t;
typedef int __dev_t;
typedef int __uid_t;
typedef int __gid_t;
typedef int _off64_t;
typedef int _fpos_t;
typedef int _ssize_t;
typedef int wint_t;
typedef int _mbstate_t;
typedef int _flock_t;
typedef int _iconv_t;
typedef int __ULong;
typedef int __FILE;
typedef int ptrdiff_t;
typedef int wchar_t;
typedef int __off_t;
typedef int __pid_t;
typedef int __loff_t;
typedef int u_char;
typedef int u_short;
typedef int u_int;
typedef int u_long;
typedef int ushort;
typedef int uint;
typedef int clock_t;
typedef int time_t;
typedef int daddr_t;
typedef int caddr_t;
typedef int ino_t;
typedef int off_t;
typedef int dev_t;
typedef int uid_t;
typedef int gid_t;
typedef int pid_t;
typedef int key_t;
typedef int ssize_t;
typedef int mode_t;
typedef int nlink_t;
typedef int fd_mask;
typedef int _types_fd_set;
typedef int clockid_t;
typedef int timer_t;
typedef int useconds_t;
typedef int suseconds_t;
typedef int FILE;
typedef int fpos_t;
typedef int cookie_read_function_t;
typedef int cookie_write_function_t;
typedef int cookie_seek_function_t;
typedef int cookie_close_function_t;
typedef int cookie_io_functions_t;
typedef int div_t;
typedef int ldiv_t;
typedef int lldiv_t;
typedef int sigset_t;
typedef int __sigset_t;
typedef int _sig_func_ptr;
typedef int sig_atomic_t;
typedef int __tzrule_type;
typedef int __tzinfo_type;
typedef int mbstate_t;
typedef int sem_t;
typedef int pthread_t;
typedef int pthread_attr_t;
typedef int pthread_mutex_t;
typedef int pthread_mutexattr_t;
typedef int pthread_cond_t;
typedef int pthread_condattr_t;
typedef int pthread_key_t;
typedef int pthread_once_t;
typedef int pthread_rwlock_t;
typedef int pthread_rwlockattr_t;
typedef int pthread_spinlock_t;
typedef int pthread_barrier_t;
typedef int pthread_barrierattr_t;
typedef int jmp_buf;
typedef int rlim_t;
typedef int sa_family_t;
typedef int sigjmp_buf;
typedef int stack_t;
typedef int siginfo_t;
typedef int z_stream;


typedef int int8_t;
typedef int uint8_t;
typedef int int16_t;
typedef int uint16_t;
typedef int int32_t;
typedef int uint32_t;
typedef int int64_t;
typedef int uint64_t;


typedef int int_least8_t;
typedef int uint_least8_t;
typedef int int_least16_t;
typedef int uint_least16_t;
typedef int int_least32_t;
typedef int uint_least32_t;
typedef int int_least64_t;
typedef int uint_least64_t;


typedef int int_fast8_t;
typedef int uint_fast8_t;
typedef int int_fast16_t;
typedef int uint_fast16_t;
typedef int int_fast32_t;
typedef int uint_fast32_t;
typedef int int_fast64_t;
typedef int uint_fast64_t;


typedef int intptr_t;
typedef int uintptr_t;


typedef int intmax_t;
typedef int uintmax_t;


typedef _Bool bool;


typedef void* MirEGLNativeWindowType;
typedef void* MirEGLNativeDisplayType;
typedef struct MirConnection MirConnection;
typedef struct MirSurface MirSurface;
typedef struct MirSurfaceSpec MirSurfaceSpec;
typedef struct MirScreencast MirScreencast;
typedef struct MirPromptSession MirPromptSession;
typedef struct MirBufferStream MirBufferStream;
typedef struct MirPersistentId MirPersistentId;
typedef struct MirBlob MirBlob;
typedef struct MirDisplayConfig MirDisplayConfig;


typedef struct xcb_connection_t xcb_connection_t;
typedef uint32_t xcb_window_t;
typedef uint32_t xcb_visualid_t;
# 3 "f:/STU/FIIT/BP/practical/fake_libc_include/stdio.h" 2
# 10 "F:/STU/FIIT/BP/Present.c" 2
# 1 "f:/STU/FIIT/BP/practical/fake_libc_include/stdint.h" 1
# 1 "f:/STU/FIIT/BP/practical/fake_libc_include/_fake_defines.h" 1
# 2 "f:/STU/FIIT/BP/practical/fake_libc_include/stdint.h" 2
# 11 "F:/STU/FIIT/BP/Present.c" 2



typedef struct byte{ 
    uint8_t nibble1 : 4;
    uint8_t nibble2 : 4;
} byte;

uint8_t S[] = {0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2};

uint8_t invS[] = {0x5, 0xe, 0xf, 0x8, 0xC, 0x1, 0x2, 0xD, 0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA};

uint8_t P[] = {0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
                    4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
                    8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
                    12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63};

byte* fromHexStringToBytes (char *block){
    byte* bytes = malloc(8 * sizeof(byte));
    int i;

    for (i=0; i<8; i++){
        bytes[i].nibble1 = (block[2*i]>='0' && block[2*i]<='9')? (block[2*i] - '0') : (block[2*i] - 'a' + 10);
        bytes[i].nibble2 = (block[2*i+1]>='0' && block[2*i+1]<='9')? (block[2*i+1] - '0') : (block[2*i+1] - 'a' + 10);
    }
    return bytes;
}

uint64_t fromBytesToLong (byte* bytes){
    uint64_t result = 0;
    int i;


    for (i=0; i<8; i++){
        result = (result << 4) | (bytes[i].nibble1 & 0xFUL);
        result = (result << 4) | (bytes[i].nibble2 & 0xFUL);
    }
    return result;
}

uint64_t fromHexStringToLong (char* block){
    uint64_t result;
    int i;


    for (i=0; i<16; i++)
        result = (result << 4) | ((block[i]>='0' && block[i]<='9')? (block[i] - '0') : (block[i] - 'a' + 10));
    return result;
}

byte* fromLongToBytes (uint64_t block){
    byte* bytes = malloc (8 * sizeof(byte));
    int i;


    for (i=7; i>=0; i--){
        bytes[i].nibble2 = (block >> 2 * (7 - i) * 4) & 0xFLL;
        bytes[i].nibble1 = (block >> (2 * (7 - i) + 1) * 4) & 0xFLL;
    }
    return bytes;
}

char* fromLongToHexString (uint64_t block){
    char* hexString = malloc (17 * sizeof(char));

    sprintf(hexString, "%016llx", block);
    return hexString;
}

uint8_t Sbox(uint8_t input){
    return S[input];
}

uint8_t inverseSbox(uint8_t input){
    return invS[input];
}
# 97 "F:/STU/FIIT/BP/Present.c"
uint64_t permute(uint64_t source){
    uint64_t permutation = 0;
    int i;
    for (i=0; i<64; i++){
        int distance = 63 - i;
        permutation = permutation | ((source >> distance & 0x1) << 63 - P[i]);
    }
    return permutation;
}
# 116 "F:/STU/FIIT/BP/Present.c"
uint64_t inversepermute(uint64_t source){
    uint64_t permutation = 0;
    int i;
    for (i=0; i<64; i++){
        int distance = 63 - P[i];
        permutation = (permutation << 1) | ((source >> distance) & 0x1);
    }
    return permutation;
}

uint16_t getKeyLow(char* key){
    int i;
    uint16_t keyLow = 0;

    for (i=16; i<20; i++)

        keyLow = (keyLow << 4) | (((key[i]>='0' && key[i]<='9')? (key[i] - '0') : (key[i] - 'a' + 10)) & 0xF);
    return keyLow;
}

uint64_t* generateSubkeys(char* key){

    uint64_t keyHigh = fromHexStringToLong(key);
    uint16_t keyLow = getKeyLow(key);

    uint64_t* subKeys = malloc(32 * (sizeof(uint64_t)));
    int i;

    subKeys[0] = keyHigh;
    for (i=1; i<32; i++){

        uint64_t temp1 = keyHigh, temp2 = keyLow;
        keyHigh = (keyHigh << 61) | (temp2 << 45) | (temp1 >> 19);
        keyLow = ((temp1 >> 3) & 0xFFFF);

        uint8_t temp = Sbox(keyHigh >> 60);

        keyHigh = keyHigh & 0x0FFFFFFFFFFFFFFFLL;

        keyHigh = keyHigh | (((uint64_t)temp) << 60);

        keyLow = keyLow ^ ((i & 0x01) << 15);
        keyHigh = keyHigh ^ (i >> 1);

        subKeys[i] = keyHigh;
    }
    return subKeys;
}

char* encrypt(char* plaintext, char* key){

    uint64_t* subkeys = generateSubkeys(key);

    uint64_t state = fromHexStringToLong(plaintext);
    int i, j;

    for (i=0; i<31; i++){

        state = state ^ subkeys[i];

        byte* stateBytes = fromLongToBytes(state);

        for (j=0; j<8; j++){
            stateBytes[j].nibble1 = Sbox(stateBytes[j].nibble1);
            stateBytes[j].nibble2 = Sbox(stateBytes[j].nibble2);
        }

        state = permute(fromBytesToLong(stateBytes));

        free(stateBytes);
    }

    state = state ^ subkeys[31];

    free(subkeys);
    return fromLongToHexString(state);
}

char* decrypt(char* ciphertext, char* key){

    uint64_t* subkeys = generateSubkeys(key);

    uint64_t state = fromHexStringToLong(ciphertext);
    int i, j;

    for (i=0; i<31; i++){

        state = state ^ subkeys[31 - i];

        state = inversepermute(state);

        byte* stateBytes = fromLongToBytes(state);

        for (j=0; j<8; j++){
            stateBytes[j].nibble1 = inverseSbox(stateBytes[j].nibble1);
            stateBytes[j].nibble2 = inverseSbox(stateBytes[j].nibble2);
        }

        state = fromBytesToLong(stateBytes);

        free(stateBytes);
    }

    state = state ^ subkeys[0];

    free(subkeys);
    return fromLongToHexString(state);
}

int main(){

    char *plaintext = malloc(17 * sizeof(char));
    char *key = malloc(21 * sizeof(char));

    char *ciphertext;

    printf("Enter the plaintext (64 bits) in hexadecimal format\nUse lower case characters and enter new line at the end\n");
    gets(plaintext);
    printf("Enter the key (80 bits) in hexadecimal format\nUse lower case characters and enter new line at the end\n");
    gets(key);

    ciphertext = encrypt(plaintext, key);

    printf("The ciphertext is: ");
    puts(ciphertext);
    printf("The decrypted plaintext is: ");

    puts(decrypt(ciphertext, key));

    free(key);
    free(plaintext);
    free(ciphertext);
    return 0;
}

