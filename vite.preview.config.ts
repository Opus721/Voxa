import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "path";

const mock = (file: string) => resolve(__dirname, "src/preview/mocks", file);

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    {
      name: "preview-entry",
      configureServer(server) {
        server.middlewares.use((req, _res, next) => {
          if (req.url === "/" || req.url === "/index.html") {
            req.url = "/preview.html";
          }
          next();
        });
      },
    },
  ],
  clearScreen: false,
  server: { port: 1421, strictPort: true, host: "127.0.0.1" },
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
      "@tauri-apps/api/core": mock("core.ts"),
      "@tauri-apps/api/event": mock("event.ts"),
      "@tauri-apps/api/app": mock("app.ts"),
      "@tauri-apps/api/webview": mock("webview.ts"),
      "@tauri-apps/api/window": mock("window.ts"),
      "@tauri-apps/plugin-os": mock("os.ts"),
      "@tauri-apps/plugin-opener": mock("opener.ts"),
      "@tauri-apps/plugin-updater": mock("updater.ts"),
      "@tauri-apps/plugin-process": mock("process.ts"),
      "@tauri-apps/plugin-dialog": mock("dialog.ts"),
      "@tauri-apps/plugin-fs": mock("fs.ts"),
      "tauri-plugin-macos-permissions-api": mock("permissions.ts"),
    },
  },
});
