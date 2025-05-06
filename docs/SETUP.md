# 開發環境建置說明（DevContainer）

本專案支援 [Visual Studio Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)，可快速在 Docker 容器中建置一致的開發環境。

## 先決條件

- 安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- 安裝 [Visual Studio Code](https://code.visualstudio.com/)
- 安裝 VSCode 擴充套件：`Dev Containers`

## 使用方法

1. 開啟 VSCode，選擇「Open Folder」開啟專案根目錄。
2. 點選左下角綠色的「><」，選擇「Reopen in Container」。
3. VSCode 將會自動讀取 `.devcontainer/` 中的設定，建立容器並安裝依賴套件。
4. 容器啟動後，即可在容器中開始開發。

## 常見目錄結構

