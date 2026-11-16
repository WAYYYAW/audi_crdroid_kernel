### AnyKernel3 Ramdisk Mod Script
## osm0sis @ xda-developers & crDroid OnePlus Ace 3V (audi) Build

### AnyKernel setup
# global properties
properties() { '
kernel.string=crDroid Kernel 6.1.182 for OnePlus Ace 3V (audi)
do.devicecheck=0
do.modules=0
do.systemless=0
do.cleanup=1
do.cleanuponabort=0
device.name1=audi
device.name2=OP5CFBL1
device.name3=OnePlusAce3V
device.name4=PJF110
device.name5=pineapple
supported.versions=
supported.patchlevels=
supported.vendorpatchlevels=
'; } # end properties

### AnyKernel install
## boot shell variables
BLOCK=boot
IS_SLOT_DEVICE=auto
RAMDISK_COMPRESSION=auto
PATCH_VBMETA_FLAG=auto
NO_MAGISK_CHECK=1

# import functions/variables and setup patching - see for reference (DO NOT REMOVE)
. tools/ak3-core.sh

ui_print " "
ui_print "=========================================="
ui_print " crDroid 6.1.182 Kernel for OnePlus Ace 3V"
ui_print " Codename: audi (SM7675 / pineapple)"
ui_print "=========================================="
ui_print " "

# Resolving occasional file system I/O latency issues which may cause binary execution exceptions
sync
sleep 0.5
chmod -R 755 $AKHOME/tools

# boot install
split_boot
if [ -f "split_img/ramdisk.cpio" ]; then
    unpack_ramdisk
    write_boot
else
    flash_boot
fi
## end boot install

# 优先选择模块路径
if [ -f "$AKHOME/zram.zip" ]; then
    MODULE_PATH="$AKHOME/zram.zip"
    KSUD_PATH="/data/adb/ksud"
    if [ -f "$KSUD_PATH" ]; then
        ui_print "Installing zram Module..."
        /data/adb/ksud module install "$MODULE_PATH"
        ui_print "Installation Complete!"
    else
        ui_print "KSUD Not Found, skipping installation..."
    fi
else
    ui_print "ZRAM module Not Found, skipping ZRAM module installation..."
fi

if [ -f "$AKHOME/kpn.zip" ]; then
    MODULE_PATH="$AKHOME/kpn.zip"
    KSUD_PATH="/data/adb/ksud"
    if [ -f "$KSUD_PATH" ]; then
        ui_print "Installing KP-N Module..."
        /data/adb/ksud module install "$MODULE_PATH"
        ui_print "Installation Complete!"
    else
        ui_print "KSUD Not Found, skipping installation..."
    fi
else
    ui_print "KP-N module Not Found, skipping KP-N module installation..."
fi
