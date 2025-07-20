---
order: 1668587759
---
# Donut 源码把玩日记（1）

工作中要用到Donut，修改它的一些bug并进行一些定制化修改，不得不说Donut的源码写的太漂亮了，文档也很全面，测试的代码也都很完整，看它的代码能感受到一种舒爽~

## 简介

Github：https://github.com/TheWover/donut

Donut可以把VBScrip、JScript、EXE、DLL和.net程序集 转换为shellcode。

一些有意思的技术：

  1. 支持x86 x64的shellcode，当不选定架构时shellcode里会包含x86 x64的shellcode，通过一段汇编去判定具体执行哪个

  2. 内置三种bypass amsi以及wldp方式

  3. 混淆加密 LoadLibrary GetProcAddress需要的dll名称以及函数名称

  4. 支持命令行参数加载

  5. 内置压缩算法减少加载二进制的体积，aPLib，LZNT1，Xpress，Xpress Huffman




## 编译流程

本机的环境是 Windows + visual Studio 2019 

找到visual Studio的`x64 Native Tools Command Prompt for VS 2019`，一般开始文件夹里面就有， 这个工具会包含vs使用的环境变量，就可以直接执行
```bash 
nmake -f Makefile.msvc

```

来编译了。

看一下编译流程Makefile.msvc 
```makefile 
@echo ###### Building exe2h ######
# 编译exe2h，这个工具是把exe中的.text段提取出来，转为hex。在donut中即提取shellcode用。
  cl /nologo loader\exe2h\exe2h.c loader\exe2h\mmap-windows.c

@echo ###### Building loader ######
# 编译donut loader，先编译，再链接，最后使用exe2h提取shellcode
# donut loader中调用api不是直接调用，都是间接通过LoadLibrary GetProcAddress调用
# 通过一系列参数（这些参数大概就是生成的文件不要任何依赖）生成exe，再通过exe2h提取text段内的代码。
  cl -Zp8 -c -nologo -Gy -Os -O1 -GR- -EHa -Oi -GS- -I ./include loader\loader.c hash.c encrypt.c loader\clib.c 
  link -nologo -order:@loader\order.txt -entry:DonutLoader -fixed -subsystem:console -nodefaultlib loader.obj hash.obj encrypt.obj clib.obj
  exe2h loader.exe

@echo ###### Building generator ######
# 编译donut主程序，DLL
  rc ./include/donut.rc
  cl -Zp8 -nologo -DDONUT_EXE -I ./include donut.c hash.c encrypt.c format.c loader\clib.c ./include/donut.res
  cl -Zp8 -nologo -DDLL -LD -I ./include donut.c hash.c encrypt.c format.c loader\clib.c
  move donut.lib lib\donut.lib
  move donut.exp lib\donut.exp
  move donut.dll lib\donut.dll

```

先编译loader，在使用exe2h提取loader中text段的数据，即是`shellcode模板`。

loader启动函数有个入参结构体
```c 
// everything required for an instance goes into the following structure
typedef struct _DONUT_INSTANCE
{
  uint32_t len;    // total size of instance
  DONUT_CRYPT key; // decrypts instance if encryption enabled

  uint64_t iv; // the 64-bit initial value for maru hash

  union
  {
    uint64_t hash[64]; // holds up to 64 api hashes
    void *addr[64];    // holds up to 64 api addresses
// include prototypes only if header included from loader.h
#ifdef LOADER_H
    struct
    {
      // imports from kernel32.dll or kernelbase.dll
      LoadLibraryA_t LoadLibraryA;
      GetProcAddress_t GetProcAddress;
      GetModuleHandleA_t GetModuleHandleA;
      VirtualAlloc_t VirtualAlloc;
      VirtualFree_t VirtualFree;
      VirtualQuery_t VirtualQuery;
      VirtualProtect_t VirtualProtect;
      Sleep_t Sleep;
      MultiByteToWideChar_t MultiByteToWideChar;
      GetUserDefaultLCID_t GetUserDefaultLCID;
      WaitForSingleObject_t WaitForSingleObject;
      CreateThread_t CreateThread;
      GetThreadContext_t GetThreadContext;
      GetCurrentThread_t GetCurrentThread;

      // imports from shell32.dll
      CommandLineToArgvW_t CommandLineToArgvW;

      // imports from oleaut32.dll
      SafeArrayCreate_t SafeArrayCreate;
      SafeArrayCreateVector_t SafeArrayCreateVector;
      SafeArrayPutElement_t SafeArrayPutElement;
      SafeArrayDestroy_t SafeArrayDestroy;
      SafeArrayGetLBound_t SafeArrayGetLBound;
      SafeArrayGetUBound_t SafeArrayGetUBound;
      SysAllocString_t SysAllocString;
      SysFreeString_t SysFreeString;
      LoadTypeLib_t LoadTypeLib;

      // imports from mscoree.dll
      CorBindToRuntime_t CorBindToRuntime;
      CLRCreateInstance_t CLRCreateInstance;

      // imports from ole32.dll
      CoInitializeEx_t CoInitializeEx;
      CoCreateInstance_t CoCreateInstance;
      CoUninitialize_t CoUninitialize;

      // imports from ntdll.dll
      RtlEqualUnicodeString_t RtlEqualUnicodeString;
      RtlEqualString_t RtlEqualString;
      RtlUnicodeStringToAnsiString_t RtlUnicodeStringToAnsiString;
      RtlInitUnicodeString_t RtlInitUnicodeString;
      RtlExitUserThread_t RtlExitUserThread;
      RtlExitUserProcess_t RtlExitUserProcess;
      RtlCreateUnicodeString_t RtlCreateUnicodeString;
      RtlGetCompressionWorkSpaceSize_t RtlGetCompressionWorkSpaceSize;
      RtlDecompressBuffer_t RtlDecompressBuffer;
      NtContinue_t NtContinue;
      // RtlFreeUnicodeString_t         RtlFreeUnicodeString;
      // RtlFreeString_t                RtlFreeString;
    };
#endif
  } api;

  int exit_opt; // 1 to call RtlExitUserProcess and terminate the host process
  int entropy;  // indicates entropy level
  uint64_t oep; // original entrypoint

  // everything from here is encrypted
  int api_cnt;                    // the 64-bit hashes of API required for instance to work
  char dll_names[DONUT_MAX_NAME]; // a list of DLL strings to load, separated by semi-colon

  char dataname[8];    // ".data"
  char kernelbase[12]; // "kernelbase"
  char amsi[8];        // "amsi"
  char clr[4];         // "clr"
  char wldp[8];        // "wldp"

  char cmd_syms[DONUT_MAX_NAME]; // symbols related to command line
  char exit_api[DONUT_MAX_NAME]; // exit-related API

  int bypass;              // indicates behaviour of byassing AMSI/WLDP
  char wldpQuery[32];      // WldpQueryDynamicCodeTrust
  char wldpIsApproved[32]; // WldpIsClassInApprovedList
  char amsiInit[16];       // AmsiInitialize
  char amsiScanBuf[16];    // AmsiScanBuffer
  char amsiScanStr[16];    // AmsiScanString

  char wscript[8];      // WScript
  char wscript_exe[12]; // wscript.exe

  GUID xIID_IUnknown;
  GUID xIID_IDispatch;

  // GUID required to load .NET assemblies
  GUID xCLSID_CLRMetaHost;
  GUID xIID_ICLRMetaHost;
  GUID xIID_ICLRRuntimeInfo;
  GUID xCLSID_CorRuntimeHost;
  GUID xIID_ICorRuntimeHost;
  GUID xIID_AppDomain;

  // GUID required to run VBS and JS files
  GUID xCLSID_ScriptLanguage;        // vbs or js
  GUID xIID_IHost;                   // wscript object
  GUID xIID_IActiveScript;           // engine
  GUID xIID_IActiveScriptSite;       // implementation
  GUID xIID_IActiveScriptSiteWindow; // basic GUI stuff
  GUID xIID_IActiveScriptParse32;    // parser
  GUID xIID_IActiveScriptParse64;

  int type;                    // DONUT_INSTANCE_EMBED, DONUT_INSTANCE_HTTP
  char server[DONUT_MAX_NAME]; // staging server hosting donut module
  char http_req[8];            // just a buffer for "GET"

  uint8_t sig[DONUT_MAX_NAME]; // string to hash
  uint64_t mac;                // to verify decryption ok

  DONUT_CRYPT mod_key; // used to decrypt module
  uint64_t mod_len;    // total size of module

  union
  {
    PDONUT_MODULE p; // Memory allocated for module downloaded via DNS or HTTP
    DONUT_MODULE x;  // Module is embedded
  } module;
} DONUT_INSTANCE, *PDONUT_INSTANCE;

```

在组装shellcode时主要就是制作这个配置结构体，传入loader指针。

具体构建完整shellcode在`donut.c` `build_loader`方法, 也包含x86 x64的识别以及对应跳转的汇编代码。
```c 
/**
 * Function: build_loader
 * ----------------------------
 *   Builds the shellcode that's injected into remote process.
 *
 *   INPUT  : Donut configuration.
 *
 *   OUTPUT : Donut error code.
 */
static int build_loader(PDONUT_CONFIG c) {
    uint8_t *pl;
    uint32_t t;

    // target is x86?
    if(c->arch == DONUT_ARCH_X86) {
      c->pic_len = sizeof(LOADER_EXE_X86) + c->inst_len + 32;
    } else 
    // target is amd64?
    if(c->arch == DONUT_ARCH_X64) {
      c->pic_len = sizeof(LOADER_EXE_X64) + c->inst_len + 32;
    } else 
    // target can be both x86 and amd64?
    if(c->arch == DONUT_ARCH_X84) {
      c->pic_len = sizeof(LOADER_EXE_X86) + 
                   sizeof(LOADER_EXE_X64) + c->inst_len + 32;
    }
    // allocate memory for shellcode
    c->pic = malloc(c->pic_len);

    if(c->pic == NULL) {
      DPRINT("Unable to allocate %" PRId32 " bytes of memory for loader.", c->pic_len);
      return DONUT_ERROR_NO_MEMORY;
    }

    DPRINT("Inserting opcodes");

    // insert shellcode
    pl = (uint8_t*)c->pic;

    // call $ + c->inst_len
    PUT_BYTE(pl,  0xE8);
    PUT_WORD(pl,  c->inst_len);
    PUT_BYTES(pl, c->inst, c->inst_len);
    // pop ecx
    PUT_BYTE(pl,  0x59);

    // x86?
    if(c->arch == DONUT_ARCH_X86) {
      // pop edx
      PUT_BYTE(pl, 0x5A);
      // push ecx
      PUT_BYTE(pl, 0x51);
      // push edx
      PUT_BYTE(pl, 0x52);

      DPRINT("Copying %" PRIi32 " bytes of x86 shellcode", 
        (uint32_t)sizeof(LOADER_EXE_X86));

      PUT_BYTES(pl, LOADER_EXE_X86, sizeof(LOADER_EXE_X86));
    } else 
    // AMD64?
    if(c->arch == DONUT_ARCH_X64) {

      DPRINT("Copying %" PRIi32 " bytes of amd64 shellcode", 
        (uint32_t)sizeof(LOADER_EXE_X64));

      PUT_BYTES(pl, LOADER_EXE_X64, sizeof(LOADER_EXE_X64));
    } else 
    // x86 + AMD64?
    if(c->arch == DONUT_ARCH_X84) {

      DPRINT("Copying %" PRIi32 " bytes of x86 + amd64 shellcode",
        (uint32_t)(sizeof(LOADER_EXE_X86) + sizeof(LOADER_EXE_X64)));

      // xor eax, eax
      PUT_BYTE(pl, 0x31);
      PUT_BYTE(pl, 0xC0);
      // dec eax
      PUT_BYTE(pl, 0x48);
      // js dword x86_code
      PUT_BYTE(pl, 0x0F);
      PUT_BYTE(pl, 0x88);
      PUT_WORD(pl,  sizeof(LOADER_EXE_X64));
      PUT_BYTES(pl, LOADER_EXE_X64, sizeof(LOADER_EXE_X64));
      // pop edx
      PUT_BYTE(pl, 0x5A);
      // push ecx
      PUT_BYTE(pl, 0x51);
      // push edx
      PUT_BYTE(pl, 0x52);
      PUT_BYTES(pl, LOADER_EXE_X86, sizeof(LOADER_EXE_X86));
    }
    return DONUT_ERROR_SUCCESS;
}

```

## DEBUG调试

shellcode不太好调试，所以donut的每一行都有一个 `DPRINT` 在debug模式下，会打印
```bash 
nmake debug -f Makefile.msvc  # 编译

donut -t -z3 "ConsoleApp.exe" # 将App转换为shellcode

loader instance # 加载shellcode

```

## 修复Win7运行失败

在dev分支(https://github.com/TheWover/donut/tree/dev) 生成最新的donut，发现在win7上无法使用，调试后发现它为了支持`XPRESS HUFFMAN编码解压，使用了`RtlDecompressBufferEx`,这个函数，这个函数只能在win8上使用，换成了`RtlDecompressBuffer`就好了。

donut很多功能都集中在loader里，http client，aPLib压缩库，各种内存执行模块，各种bypass函数，使用时可以按需删减。
