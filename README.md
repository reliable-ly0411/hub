# Eleven · CyanogenMod 独立移植版

## 推荐下载：CM12.1

**[下载 Eleven（Android 9 / 11 模拟器实测）](Eleven-CM12.1-Standalone-Android9-11-tested.zip)**

版本 `2.0-cm12.1-standalone.2`。解压后安装 `Eleven.apk`，允许读取本地音乐。要看频谱，在十一的 **设置 → Show music visualization** 打开开关，再允许系统的音频权限。普通播放不需要麦克风权限。

使用 [同期 CM12.1 Eleven 源码](https://github.com/CyanogenMod/android_packages_apps_Eleven/tree/9d2f80421cde3459362f94ea5de7a311081c5894)，不是从 XT910 的 RC5.6 ROM 提取的原 APK。原版界面、32 柱频谱绘制、动画与配色逻辑保留；青色来自原版封面或占位图配色，并非固定为青色。

同一签名包在 GPD 的 Android 9（API 28）和 Android 11（API 30）模拟器验证了本地播放和动态频谱。Android 9 还验证了首次权限拒绝/授权、曲库立即刷新及界面/媒体键暂停恢复。未做实体手机或扬声器试听。ZIP 内含源码补丁、构建说明、许可和校验值。

- APK SHA-256：`903f0fd6201b5d313b3a9413e886064ea26272a8f7fad09d463e4d710a8a5831`
- ZIP SHA-256：`a854c0a3d8220f6bdf76b4f2e6146ccfcb89aceb64fb61da2440a59f4b4dfd40`

## 历史包：CM12.0

[旧 v6 下载（仅 Android 11 模拟器验收）](Eleven-CM12-Standalone-v6-Android11-tested.zip)。v6 不是上面的 CM12.1 版本，不适合作为 Android 9 包。此前的 `UNTESTED.zip` 是 v6 验收前留档，两者的 APK 字节相同。
