
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Varsayılan Vite portu
    open: true, // Sunucu başlatıldığında tarayıcıyı otomatik aç
    host: 'localhost', // Yerel sunucu için host
  },
  build: {
    outDir: 'dist', // Derleme çıktısı için klasör
    sourcemap: true, // Hata ayıklama için kaynak haritaları
  },
});