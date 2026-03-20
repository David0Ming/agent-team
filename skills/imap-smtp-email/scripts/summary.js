#!/usr/bin/env node
const Imap = require('imap');
const { simpleParser } = require('mailparser');
const path = require('path');
const fs = require('fs');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const KEYWORDS = {
  interview: ['面试', 'interview', '面谈'],
  resume: ['简历', 'resume', '投递', 'cv'],
  test: ['笔试', 'assessment', '测评', '考试'],
  offer: ['offer', '录用', '入职', 'onboard'],
  study: ['学习', '课程', 'training', '培训', '讲座', 'conference', '会议']
};

function categorize(subject, from, body) {
  const text = `${subject} ${from} ${body}`.toLowerCase();
  if (KEYWORDS.interview.some(k => text.includes(k))) return 'interview';
  if (KEYWORDS.resume.some(k => text.includes(k))) return 'resume';
  if (KEYWORDS.test.some(k => text.includes(k))) return 'test';
  if (KEYWORDS.offer.some(k => text.includes(k))) return 'offer';
  if (KEYWORDS.study.some(k => text.includes(k))) return 'study';
  return 'other';
}

function extractTime(subject, body) {
  const text = `${subject} ${body}`;
  const now = new Date();
  const year = now.getFullYear();
  
  // Pattern 1: 2026年3月18日（周三） 10:30 or 2026年3月18日 10:30
  let match = text.match(/(\d{4})年(\d{1,2})月(\d{1,2})日[^0-9]*(\d{1,2}):(\d{2})/);
  if (match) return `${match[1]}-${match[2].padStart(2,'0')}-${match[3].padStart(2,'0')} ${match[4].padStart(2,'0')}:${match[5]}`;
  
  // Pattern 2: 3月18日 10:30
  match = text.match(/(\d{1,2})月(\d{1,2})日[^0-9]*(\d{1,2}):(\d{2})/);
  if (match) return `${year}-${match[1].padStart(2,'0')}-${match[2].padStart(2,'0')} ${match[3].padStart(2,'0')}:${match[4]}`;
  
  // Pattern 3: 2026-03-18 10:30
  match = text.match(/(\d{4})-(\d{2})-(\d{2})\s*(\d{2}):(\d{2})/);
  if (match) return `${match[1]}-${match[2]}-${match[3]} ${match[4]}:${match[5]}`;
  
  return null;
}

async function loadAccounts() {
  const accountsPath = path.resolve(__dirname, '../accounts.json');
  if (!fs.existsSync(accountsPath)) {
    return [{
      name: 'default',
      imap: {
        host: process.env.IMAP_HOST,
        port: parseInt(process.env.IMAP_PORT) || 993,
        user: process.env.IMAP_USER,
        pass: process.env.IMAP_PASS,
        tls: process.env.IMAP_TLS === 'true'
      }
    }];
  }
  return JSON.parse(fs.readFileSync(accountsPath, 'utf8')).accounts;
}

async function fetchEmails(account, since) {
  return new Promise((resolve, reject) => {
    const imap = new Imap({
      user: account.imap.user,
      password: account.imap.pass,
      host: account.imap.host,
      port: account.imap.port,
      tls: account.imap.tls !== false,
      tlsOptions: { rejectUnauthorized: false }
    });

    const results = [];
    
    imap.once('ready', () => {
      imap.openBox('INBOX', true, (err) => {
        if (err) return reject(err);
        
        imap.search([['SINCE', since]], (err, uids) => {
          if (err || !uids.length) {
            imap.end();
            return resolve(results);
          }

          const f = imap.fetch(uids, { bodies: [''] });
          
          f.on('message', msg => {
            msg.on('body', stream => {
              simpleParser(stream, (err, parsed) => {
                if (!err) {
                  results.push({
                    subject: parsed.subject || '(无主题)',
                    from: parsed.from?.text || '(未知)',
                    date: parsed.date,
                    body: parsed.text || ''
                  });
                }
              });
            });
          });
          
          f.once('end', () => {
            imap.end();
            resolve(results);
          });
        });
      });
    });

    imap.once('error', reject);
    imap.connect();
  });
}

async function main() {
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];
  
  const accounts = await loadAccounts();
  const categories = { interview: [], resume: [], test: [], offer: [], study: [], other: [] };
  const todos = [];

  for (const account of accounts) {
    console.log(`检查账户: ${account.name}`);
    const emails = await fetchEmails(account, today);
    
    emails.forEach(email => {
      const cat = categorize(email.subject, email.from, email.body);
      categories[cat].push({ ...email, account: account.name });
      
      // Add to todos: interview, test, study, or calendar invites
      if (cat === 'interview' || cat === 'test') {
        const time = extractTime(email.subject, email.body);
        todos.push({
          type: 'work',
          title: `${cat === 'interview' ? '面试' : '笔试'}: ${email.subject}`,
          time: time || '待确认',
          from: email.from
        });
      } else if (cat === 'study') {
        const time = extractTime(email.subject, email.body);
        todos.push({
          type: 'study',
          title: email.subject,
          time: time || '待确认',
          from: email.from
        });
      } else if (email.subject.includes('日程')) {
        // Calendar invites
        const time = extractTime(email.subject, email.body);
        if (time) {
          todos.push({
            type: 'work',
            title: email.subject.replace(/^日程(邀请|更新)：/, ''),
            time: time,
            from: email.from
          });
        }
      }
    });
  }

  const memoryDir = path.resolve(process.env.HOME || process.env.USERPROFILE, '.openclaw/workspace/memory/daily');
  if (!fs.existsSync(memoryDir)) fs.mkdirSync(memoryDir, { recursive: true });

  const summaryPath = path.join(memoryDir, `email-summary-${dateStr}.md`);
  let content = `# 邮件摘要 ${dateStr}\n\n`;
  
  const labels = {
    interview: '## 面试类',
    resume: '## 简历类',
    test: '## 笔试类',
    offer: '## Offer类',
    study: '## 学习类',
    other: '## 其他'
  };

  for (const [cat, emails] of Object.entries(categories)) {
    if (emails.length > 0) {
      content += `${labels[cat]} (${emails.length}封)\n\n`;
      emails.forEach(e => {
        const date = e.date ? e.date.toLocaleString('zh-CN') : '未知';
        content += `- **${e.subject}**\n  - 发件人: ${e.from}\n  - 时间: ${date}\n  - 账户: ${e.account}\n\n`;
      });
    }
  }

  fs.writeFileSync(summaryPath, content);
  console.log(`\n摘要已保存: ${summaryPath}`);

  if (todos.length > 0) {
    const todosPath = path.resolve(process.env.HOME || process.env.USERPROFILE, '.openclaw/workspace/memory/email-todos.md');
    let content = fs.existsSync(todosPath) ? fs.readFileSync(todosPath, 'utf8') : `# 邮件待办\n\n## 工作代办\n\n## 学习代办\n`;
    
    todos.forEach(todo => {
      const section = todo.type === 'work' ? '## 工作代办' : '## 学习代办';
      const todoLine = `- [ ] ${todo.title} (${todo.time}) - 来自: ${todo.from}\n`;
      
      if (!content.includes(todoLine)) {
        content = content.replace(section, `${section}\n${todoLine}`);
        
        // Create cron reminder if time is valid
        if (todo.time !== '待确认') {
          try {
            const eventTime = new Date(todo.time);
            const reminderTime = new Date(eventTime.getTime() - 60 * 60 * 1000);
            
            if (reminderTime > new Date()) {
              const eventName = todo.title.substring(0, 50);
              const cronCmd = `openclaw cron add --name "提醒-${eventName}" --at "${reminderTime.toISOString()}" --message "提醒: ${todo.title} 将在 ${todo.time} 开始"`;
              require('child_process').execSync(cronCmd, { stdio: 'inherit' });
              console.log(`已创建提醒: ${todo.title} at ${reminderTime.toLocaleString('zh-CN')}`);
            }
          } catch (e) {
            console.warn(`无法创建提醒: ${e.message}`);
          }
        }
      }
    });
    
    fs.writeFileSync(todosPath, content);
    console.log(`待办已更新: ${todosPath}`);
  }
}

main().catch(console.error);
