import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  // ✅ GitHub Pages: use your repo name here
  base: mode === "production" ? "/genre_prediction/" : "/",

  server: {
    host: "::",
    port: 8080,
  },

  // ✅ Remove lovable-tagger entirely
  plugins: [react()],

  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
