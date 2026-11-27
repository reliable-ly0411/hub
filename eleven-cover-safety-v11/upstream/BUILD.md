# CyanogenMod 12.1 Eleven standalone compatibility port

Base: CyanogenMod's original `cm-12.1` Eleven source, commit `9d2f80421cde3459362f94ea5de7a311081c5894` (November 6, 2015). This is a period-correct public upstream baseline, not an extraction of the user-reported `12.1-RC5.6-umts_spyder` ROM. The ROM's exact `Eleven.apk` has not been verified.

The standalone app uses the independent package `com.cyanogenmod.eleven.standalone`. The original playback/libraries' artwork, layouts and spectrum drawing are preserved. A small interface adapter feeds Android's platform FFT for the active Eleven player session to the original `VisualizerView` (32 bars, same geometry, colors and animations). Android's Visualizer requires explicit record-audio permission; normal playback remains available without it. No recording, network transmission or global output capture is used by the spectrum adapter.

Build using pinned Android SDK Platform 35, Build Tools 35.0.0, Java 21, Python 3, OpenSSL and keytool. Supply the pinned CardView, Palette, ICU4J and ECJ artifacts documented by `standalone/build.sh`. No separate pheelicks visualizer library is needed in this branch. Use `ANDROID_HOME`, `ELEVEN_DEPS`, optional `ELEVEN_BUILD_DIR` and private `ELEVEN_KEY_DIR`; never distribute signing material. Rebuild from the exact base and this patch, with a private signer. Runtime claims require device/emulator acceptance; source checks are not a substitute.

Run `python3 standalone/check-original-spectrum.py` and the capture-size/API checks before packaging.
