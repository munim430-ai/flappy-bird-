# Building the Android APK

## Prerequisites

| Tool | Notes |
|------|-------|
| Unity 6000.0.37f1 | Must have the **Android Build Support** module installed |
| Android SDK / NDK | Installed automatically by Unity Hub or set manually in **Preferences > External Tools** |
| JDK 17+ | Bundled with Unity; or configure a custom JDK in External Tools |
| Android device / emulator | API level 22+ (Android 5.1 Lollipop) |

## Build via Unity Editor

1. Open the project in Unity (see `UNITY_SETUP.md`).
2. Open **File > Build Settings** (Ctrl+Shift+B).
3. Select **Android** and click **Switch Platform** if not already active.
4. Under **Scenes In Build**, confirm both scenes are listed:
   - `Assets/Scenes/Menu Background.unity`
   - `Assets/Scenes/fp.unity`
   - If missing, click **Add Open Scenes** with each scene open.
5. Set **Run Device** to your connected device, or leave as default for a standalone APK.
6. Click **Build** and choose an output path (e.g., `Builds/SkullBird.apk`).
7. Unity will compile and produce the APK file.

## Build via Unity Headless CLI

Run from the repository root. Replace `/path/to/Unity` with your Unity editor executable.

**Linux / macOS:**
```bash
/path/to/Unity -quit -batchmode -nographics \
  -projectPath "$(pwd)" \
  -buildTarget Android \
  -executeMethod BuildScript.BuildAndroid \
  -logFile build.log
```

**Windows:**
```cmd
"C:\Program Files\Unity\Hub\Editor\6000.0.37f1\Editor\Unity.exe" ^
  -quit -batchmode -nographics ^
  -projectPath "%CD%" ^
  -buildTarget Android ^
  -executeMethod BuildScript.BuildAndroid ^
  -logFile build.log
```

> The `-executeMethod BuildScript.BuildAndroid` flag calls a custom static build method. You can add `Assets/Editor/BuildScript.cs` with the following minimal content:
>
> ```csharp
> using UnityEditor;
> public static class BuildScript {
>     public static void BuildAndroid() {
>         BuildPlayerOptions opt = new BuildPlayerOptions {
>             scenes = new[] {
>                 "Assets/Scenes/Menu Background.unity",
>                 "Assets/Scenes/fp.unity"
>             },
>             locationPathName = "Builds/SkullBird.apk",
>             target = BuildTarget.Android,
>             options = BuildOptions.None
>         };
>         BuildPipeline.BuildPlayer(opt);
>     }
> }
> ```

## Installing the APK on an Android Device

### Via ADB (USB)

1. Enable **Developer Options** and **USB Debugging** on your Android device.
2. Connect via USB.
3. Install:
   ```bash
   adb install Builds/SkullBird.apk
   ```
4. Launch from your device's app drawer — look for **Skull Bird**.

### Direct Transfer

1. Copy the APK to your device via USB storage, Google Drive, or any file transfer method.
2. On the device, open the APK file.
3. If prompted, enable **Install from Unknown Sources** in Settings > Security.
4. Follow the installation prompts.

## App Details

| Setting | Value |
|---------|-------|
| Package name | `com.learning.skullbird` |
| Min SDK | API 22 (Android 5.1) |
| Orientation | Portrait |
| Product name | Skull Bird |
