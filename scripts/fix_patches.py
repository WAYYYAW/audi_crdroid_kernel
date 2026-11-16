#!/usr/bin/env python3
"""针对 crDroid sm8650 (audi, 6.1.182) 构建时补丁无法干净应用的定向修复。

用法: python3 scripts/fix_patches.py susfs-namespace   # 修复 SUSFS 补丁缺失的 hunk
      python3 scripts/fix_patches.py zstd-level        # 补齐 crypto/zstd.c 的 compression_level

只在对应补丁部分失败后调用，且自身幂等：重复执行不会重复插入。
"""

import sys


def fix_susfs_namespace(path: str = "fs/namespace.c") -> bool:
    """补齐 SUSFS 补丁 fs/namespace.c 第 1 个 hunk 的全部内容。

    本内核在 #include "internal.h" 之后多了一行 #include <trace/hooks/blk.h>，
    导致该 hunk 的上下文无法匹配，整块（susfs_def.h 引入 + extern 声明 +
    CL_COPY_MNT_NS 宏）被跳过，最终 fs/namespace.c 报大量未定义符号。
    """
    with open(path) as f:
        src = f.read()

    changed = False

    if "linux/susfs_def.h" not in src:
        needle = "#include <linux/mnt_idmapping.h>\n"
        if needle not in src:
            print(f"ERROR: {path} 中找不到 {needle!r}", file=sys.stderr)
            return False
        src = src.replace(
            needle,
            needle
            + "#ifdef CONFIG_KSU_SUSFS\n"
            + "#include <linux/susfs_def.h>\n"
            + "#endif // #ifdef CONFIG_KSU_SUSFS\n",
            1,
        )
        changed = True

    # 注意：源码里本来就有 CL_COPY_MNT_NS_FILE，不能用子串判断，否则会误判为已修复
    if "#define CL_COPY_MNT_NS " not in src:
        marker = '#include "internal.h"\n'
        if marker not in src:
            print(f"ERROR: {path} 中找不到 {marker!r}", file=sys.stderr)
            return False
        block = (
            "\n#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n"
            "extern bool susfs_is_current_ksu_domain(void);\n"
            "extern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;\n"
            "\n"
            "#define CL_COPY_MNT_NS BIT(25) /* used by copy_mnt_ns() */\n"
            "#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n"
        )
        src = src.replace(marker, marker + block, 1)
        changed = True

    if changed:
        with open(path, "w") as f:
            f.write(src)
        print(f"已修复 {path}")
    else:
        print(f"{path} 无需修复")
    return True


def fix_zstd_level(path: str = "crypto/zstd.c") -> bool:
    """确保 crypto/zstd.c 引用的 compression_level 有定义。

    ZSTD 1.5.7 升级补丁给 zstd_params() 加了基于 compression_level 的可调压缩级别，
    但声明它的第 1 个 hunk 因上游 #define ZSTD_DEF_LEVEL 的值不同而失配
    （补丁期望 1，实际为 3），导致未定义标识符。
    """
    with open(path) as f:
        src = f.read()

    if "compression_level" not in src:
        print(f"{path} 未引用 compression_level，无需修复")
        return True

    if "__read_mostly compression_level" in src:
        print(f"{path} 已定义 compression_level，无需修复")
        return True

    needle = "static zstd_parameters zstd_params(void)\n{\n"
    if needle not in src:
        print(f"ERROR: {path} 中找不到 zstd_params() 定义", file=sys.stderr)
        return False

    src = src.replace(
        needle,
        "static uint __read_mostly compression_level = 1;\n"
        "module_param(compression_level, uint, 0644);\n\n" + needle,
        1,
    )
    with open(path, "w") as f:
        f.write(src)
    print(f"已为 {path} 补齐 compression_level 定义")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    action = sys.argv[1]
    if action == "susfs-namespace":
        return 0 if fix_susfs_namespace() else 1
    if action == "zstd-level":
        return 0 if fix_zstd_level() else 1
    print(f"未知操作: {action}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
