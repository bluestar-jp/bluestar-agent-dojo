const fs = require('fs');
const path = require('path');

// ルートディレクトリの shihan/prompts へのパス
const SOURCE_DIR = path.resolve(__dirname, '../../../shihan/prompts');
// Extension内の配布用ディレクトリ
const DEST_DIR = path.resolve(__dirname, '../dist/prompts');

// 憲法や秘伝もコピー対象にする
const OKITE_DIR = path.resolve(__dirname, '../../../shihan/okite');
const HIDEN_DIR = path.resolve(__dirname, '../../../shihan/hiden');
const DEST_ASSETS_DIR = path.resolve(__dirname, '../dist/assets');

function copyDir(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  
  if (!fs.existsSync(src)) {
    console.warn(`Source directory not found: ${src}`);
    return;
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (let entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else if (entry.name.endsWith('.md')) {
      fs.copyFileSync(srcPath, destPath);
      console.log(`Copied: ${entry.name}`);
    }
  }
}

console.log('--- Syncing Dojo Prompts ---');
copyDir(SOURCE_DIR, DEST_DIR);
copyDir(OKITE_DIR, path.join(DEST_ASSETS_DIR, 'okite'));
copyDir(HIDEN_DIR, path.join(DEST_ASSETS_DIR, 'hiden'));
console.log('--- Sync Complete ---');
