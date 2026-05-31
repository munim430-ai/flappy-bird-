# Running Skull Bird in Unity

## Requirements

- Unity **6000.0.37f1** (Unity 6)  
  Download from [Unity Download Archive](https://unity.com/releases/editor/archive)
- Unity Hub (recommended for version management)
- 2D mobile support module installed with the editor

## Opening the Project

1. Launch **Unity Hub**.
2. Click **Open** > **Add project from disk**.
3. Navigate to and select the `flappy-bird-` repository root folder.
4. Unity Hub will detect `ProjectSettings/ProjectVersion.txt` and open with the correct editor version. If prompted to upgrade, choose **Continue** only if you intentionally want to upgrade.
5. Wait for Unity to import all assets (first open may take a few minutes).

## Running in the Editor

1. In the **Project** window, navigate to `Assets/Scenes/`.
2. Double-click **Menu Background** to open the menu scene.
3. Press the **Play** button (▶) at the top of the editor.
4. The menu screen will appear with **Skull Bird** title and Start / Exit buttons.
5. Click **Start** to load the gameplay scene.

## Switching Build Target to Android

The project is configured for Android (portrait, 1080×1920).

1. Go to **File > Build Settings** (Ctrl+Shift+B / Cmd+Shift+B).
2. Select **Android** from the platform list.
3. Click **Switch Platform** and wait for Unity to reimport assets for Android.
4. Optionally click **Player Settings** to verify:
   - Product Name: `Skull Bird`
   - Bundle Identifier: `com.learning.skullbird`
   - Default Orientation: Portrait

## Scene List

| Scene | Path | Description |
|-------|------|-------------|
| Menu Background | `Assets/Scenes/Menu Background.unity` | Main menu / start screen |
| fp | `Assets/Scenes/fp.unity` | Gameplay scene |

## Notes

- Audio, sprites, and scripts are all self-contained in `Assets/`.
- No external packages beyond Unity's built-in 2D and UGUI packages are required.
- The `Library/` folder is gitignored — Unity regenerates it automatically on first open.
