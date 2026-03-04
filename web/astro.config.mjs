import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://myrient.erista.me',
  output: 'static',
  build: {
    format: 'directory',
  },
});
