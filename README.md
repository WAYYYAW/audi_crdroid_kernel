# 一加 Ace 3V (audi) crDroid 6.1.182 内核自动化构建仓库

本项目是专为 **OnePlus Ace 3V（一加 Ace 3V，设备代号 `audi`）** 上的 **crDroid** 自定义 ROM 设计的通用内核云端自动化构建框架。

内核源码直接基于 crDroid 官方分支 [crdroidandroid/android_kernel_oneplus_sm8650](https://github.com/crdroidandroid/android_kernel_oneplus_sm8650) 的 **17.0** 分支构建，基线版本已更新至最新的 **Linux 6.1.182**。

---

## 📱 机型与系统信息

- **目标机型**: 一加 Ace 3V / OnePlus Ace 3V (`audi` / `PJF110` / `OP5CFBL1`)
- **平台芯片**: 骁龙 7+ Gen 3 (SM7675 / pineapple 家族)
- **适配系统**: crDroid Android 17.0 (基于 Android 15 / LineageOS 22 体系)
- **内核版本**: Linux 6.1.182 (GKI v4 / Pineapple / Oplus 专属驱动已完整融合)

---

## ✨ 核心特性与可选参数

本仓库支持通过 GitHub Actions 的 `workflow_dispatch` 界面在网页端一键勾选/配置编译特性：

### 1. 多 Root 方案一键切换 (`ksu_type`)
- **BakaSU**（默认）：基于 SukiSU 改进的活跃维护分支，完美兼容 SukiSU Manager，支持完整伪装与高级功能。
- **KernelSU Next**：由 pershoot / KernelSU Next 团队维护的高性能分支，内置 dev-susfs 深度适配，带 apk_sign 签名支持。
- **SukiSU Ultra**：经典 SukiSU Ultra 方案。
- **原版 KernelSU**：tiann/KernelSU 官方主线。
- **无内置 Root (none)**：纯净原生内核，方便使用 Magisk 或保持未 Root 状态。

### 2. 隐匿与补丁框架
- **SUSFS (v1.5.x)**：集成专为 6.1 内核适配的 SUSFS 隐藏环境挂载与路径伪装补丁，有效抵御各类 Root 扫描。
- **KPM (KPatch-Next)**：支持独立 KPatch-Next 内核级模块修补框架。

### 3. 高级性能与拓展补丁
- **LZ4 1.10.0 + ZSTD 1.5.7**：全新算法与汇编优化补丁，大幅加快 zram 压缩与解压速度。
- **TCP BBR & Brutal**：包含 BBR、Brutal、Westwood、Vegas 等先进 TCP 拥塞控制算法，可将 BBR 设为默认拥塞控制算法。
- **内核防格基带保护 (Baseband Guard)**：拦截任何尝试对底层非用户分区（如 modem, fsg, dsp 等）恶意覆写的指令，有效防御各类格机脚本。
- **Droidspaces 容器与 NTSYNC**：为手机提供接近原生性能的轻量 Linux 容器环境，支持 POSIX 消息队列与 NTSYNC 互斥锁。
- **三星 SSG I/O 调度器**：针对闪存读写特化优化，提升整体流畅度与 I/O 响应。
- **Re:Kernel 支持**：配合 Freezer、NoActive 等墓碑冻结工具，降低待机功耗。
- **网络高级拓展 (IPset)**：完整启用 netfilter xt_set 与 ipset 散列表匹配，满足高级代理与路由分流需求。
- **-O2 编译优化**：替换默认大小优先策略，针对运行效率进行深度优化。

---

## 🚀 编译工具链与极速构建

- **编译器**: 最新 AOSP LLVM Clang 20 (`r547379`) + LLD 链接器
- **构建加速**: 内置 ccache-ECS 缓存优化与时间劫持库（libfakestat / libfaketimeMT），后续增量编译通常只需 **5~8 分钟**。

---

## 📦 双重构建产物交付

每次工作流执行成功后，会自动生成并发布：

1. **AnyKernel3 卡刷包 (`AnyKernel3_crDroid_audi_*.zip`)**
   - 适配 Ace 3V 的 `boot` 分区自动替换机制。
   - 可直接使用手机端 **Kernel Flasher** 应用或 **TWRP / OrangeFox** 刷入。
2. **纯提取版内核镜像 (`Image`)**
   - 提取出未打包的内核原生 `Image` 文件。
   - 适合开发者用于 fastboot 临时引导测试 (`fastboot boot Image`) 或手动打入自定义 `boot.img`。
3. **GitHub Release 自动发布**
   - 带有规范的版本号 Tag、编译参数详细说明日志和直接下载链接。

---

## 🛠️ 使用教程

### 1. 推送到你的 GitHub 账户
1. 在 GitHub 上新建一个仓库（例如名为 `audi_crdroid_kernel`）。
2. 在本地进入该工程目录并执行：
   ```bash
   git remote add origin https://github.com/<你的用户名>/<仓库名>.git
   git branch -M main
   git push -u origin main
   ```

### 2. 触发编译
1. 打开你的 GitHub 仓库页面，点击顶部的 **Actions** 标签。
2. 在左侧选择 **`crDroid 6.1.182 OnePlus Ace 3V (audi) 内核编译`** 工作流。
3. 点击右侧的 **Run workflow** 按钮。
4. 按需选择 KernelSU 分支、开启/关闭特性开关，然后点击 **Run workflow** 启动编译。
5. 编译完成后，前往仓库的 **Releases** 页面即可下载打包好的卡刷包与镜像。

---

## 📥 刷入方法

> [!IMPORTANT]
> 刷入任何第三方定制内核前，请务必备份原厂或当前正在使用的 `boot` 分区镜像。

### 方法一：使用 Kernel Flasher 刷入（强烈推荐）
1. 在手机上安装 [Kernel Flasher](https://github.com/capntrips/KernelSU/releases) 或相关内核刷写工具。
2. 选择下载好的 `AnyKernel3_crDroid_audi_*.zip`。
3. 点击“刷入并重启”即可。

### 方法二：通过第三方 Recovery 刷入
1. 重启手机进入 TWRP / OrangeFox Recovery。
2. 点击“安装 (Install)”，选中 `AnyKernel3_crDroid_audi_*.zip`。
3. 滑动刷入，完成后重启系统。

---

## 🌟 致谢与鸣谢

- **crDroid Android**: [crDroidAndroid](https://github.com/crdroidandroid) & [android_kernel_oneplus_sm8650](https://github.com/crdroidandroid/android_kernel_oneplus_sm8650)
- **cctv18**: [cctv18/oppo_oplus_realme_sm8650](https://github.com/cctv18/oppo_oplus_realme_sm8650) 提供的编译框架与特性补丁支持
- **osm0sis**: [AnyKernel3](https://github.com/osm0sis/AnyKernel3)
- **KernelSU 团队**: [KernelSU](https://github.com/tiann/KernelSU) / [KernelSU-Next](https://github.com/KernelSU-Next/KernelSU-Next) / [BakaSU](https://github.com/Baka-SU/BakaSU)
- **SUSFS**: [ShirkNeko/susfs4ksu](https://github.com/ShirkNeko/susfs4ksu)
- **Baseband Guard**: [vc-teahouse/Baseband-guard](https://github.com/vc-teahouse/Baseband-guard)
