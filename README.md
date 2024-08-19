# FFmpeg 粗剪

這個腳本能根據提供的 CSV 文件生成一批 `ffmpeg` 命令，用於對視頻進行快速剪輯。腳本設計支持 Windows 和 Linux/macOS 系統，讓你可以輕鬆生成一系列的命令來進行視頻的剪切、複製和處理。

## 特性

- **跨平台支持**：根據用戶的輸入，自動格式化路徑和文件名，適用於 Windows 或 Linux/macOS 系統。
- **自動文件擴展名處理**：自動為輸出文件名添加 `.mp4` 擴展名，如果 CSV 中未提供。

## 需求

- Python 3.x
- 已安裝 `ffmpeg` 並可在系統的 PATH 中訪問。

## 安裝

複製此倉庫或直接下載腳本到本地機器：

```bash
git clone https://github.com/scorpio-su/ffmpeg-rough-cut.git
cd ffmpeg-rough-cut
```

確保你已安裝必要的依賴項：

```bash
pip install -r requirements.txt
```

## 使用

1. **準備你的 CSV 文件**

   創建一個 CSV 文件，包含以下列：

   - `start time`: 剪輯的開始時間（例如，`0:26:08`）。
   - `end time`: 剪輯的結束時間（例如，`0:45:48`）。
   - `input file path`: 輸入視頻文件的路徑。
   - `output file path`: 輸出文件的保存目錄。
   - `output file name`: 輸出文件的名稱（不需要包含 `.mp4`）。

   示例 `input_data.csv`：

   ```csv
   start time,end time,input file path,output file path,output file name
   0:26:08,0:45:48,TR514/514-1.mkv,TR514_OK_OK/,Day 1
   ```

2. **運行腳本**

   從命令行運行腳本：

   ```bash
   python script.py
   ```

   腳本會提示你指定操作系統（Windows 或 Linux/macOS）。根據你的選擇，它將生成一個批處理文件（Windows 上為 `.bat` 文件，Linux/macOS 上為 `.sh` 文件）。

3. **執行生成的腳本**

   運行腳本後，會在相同目錄下生成一個命令文件（`ffmpeg_commands.bat` 或 `ffmpeg_commands.sh`）。你可以執行此文件來依次運行所有的 `ffmpeg` 命令。

   - 在 Windows 上：
     ```cmd
     ffmpeg_commands.bat
     ```
   - 在 Linux/macOS 上：
     ```bash
     bash ffmpeg_commands.sh
     ```

## 示例

這是一個示例 CSV 文件及其對應的輸出命令：

**CSV 文件 (`input_data.csv`)：**

```csv
 start time,end time,input file path,output file path,output file name
 0:26:08,0:45:48,TR514/514-1.mkv,TR514_OK_OK/,Day 1
```

**生成的命令：**

```bash
ffmpeg -ss 0:26:08 -i "TR514/514-1.mkv" -to 0:45:48 -c copy -avoid_negative_ts 1 "TR514_OK_OK/Day 1.mp4"
```
