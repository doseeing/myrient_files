import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://myrient.erista.me',
  // For GitHub Pages project site (e.g. username.github.io/myrient_files), use base:
  base: 'doseeing.github.io/myrient_files/',
  output: 'static',
  build: {
    format: 'directory',
  },
});
