import * as path from 'path';
import * as fs from 'fs';

/**
 * BlueStar Dojo Extension
 * 師範エージェントをスキルとして動的に登録する
 */
export function activate(context: any) {
  console.log('BlueStar Dojo Extension Activated 🥋');

  const promptsDir = path.join(__dirname, 'prompts');
  
  // promptsディレクトリ内のMarkdownファイルをスキャンしてスキルとして登録
  if (fs.existsSync(promptsDir)) {
    const files = fs.readdirSync(promptsDir);
    
    files.forEach(file => {
      if (file.endsWith('.md')) {
        const skillId = file.replace('.md', '');
        const content = fs.readFileSync(path.join(promptsDir, file), 'utf-8');

        // スキルとして登録 (APIは仮想)
        context.registerSkill({
          id: `bluestar.${skillId}`,
          name: toTitleCase(skillId),
          description: `BlueStar Dojo Shihan: ${skillId}`,
          instructions: content
        });
        
        console.log(`Registered Skill: bluestar.${skillId}`);
      }
    });
  }
}

function toTitleCase(str: string) {
  return str.split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}
