#!/usr/bin/env node
const Imap = require('imap');
const { simpleParser } = require('mailparser');
const path = require('path');
const fs = require('fs');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });

const KEYWORDS = {
  interview: ['面试', 'interview', '面谈'],
  resume: ['简历', 'resume', '投递', 'cv'],
  test: ['笔试', 'test', 'assessment', '测评'],
  offer: ['offer', '录用', '入职', 'onboard']
};

function categorize(subject, from) {
  const text = `${subject} ${from}`.toLowerCase();
  if (KEYWORDS.interview.some(k => text.includes(k))) return 'interview';
  if (KEYWORDS.resume.some(k => text.includes(k))) return 'resume';
  if (KEYWORDS.test.some(k => text.includes(k))) return 'test';
  if (KEYWORDS.offer.some(k => text.includes(k))) return 'offer';
  return 'other';
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

async function fetchEmails(account, days = 7) {
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
      imap.openBox('INBOX', true, (err, box) => {
        if (err) return reject(err);
        
        const since = new Date();
        since.setDate(since.getDate() - days);
        
        imap.search([['SINCE', since]], (err, uids) => {
          if (err || !uids.length) {
            imap.end();
            return resolve(results);
          }

          const f = imap.fetch(uids, { bodies: ['HEADER'], struct: true });
          
          f.on('message', msg => {
            msg.on('body', stream => {
              simpleParser(stream, (err, parsed) => {
                if (!err) {
                  results.push({
                    subject: parsed.subject || '(无主题)',
                    from: parsed.from?.text || '(未知)',
                    date: parsed.date
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
  const args = process.argv.slice(2);
  const accountName = args.find(a => a.startsWith('--account='))?.split('=')[1];
  const days = parseInt(args.find(a => a.startsWith('--days='))?.split('=')[1] || '7');

  const accounts = await loadAccounts();
  const filtered = accountName ? accounts.filter(a => a.name === accountName) : accounts;

  const categories = { interview: [], resume: [], test: [], offer: [], other: [] };

  for (const account of filtered) {
    console.log(`\n检查账户: ${account.name}`);
    const emails = await fetchEmails(account, days);
    
    emails.forEach(email => {
      const cat = categorize(email.subject, email.from);
      categories[cat].push({ ...email, account: account.name });
    });
  }

  console.log('\n## 邮件分类结果\n');
  
  const labels = {
    interview: '### 面试类',
    resume: '### 简历类',
    test: '### 笔试类',
    offer: '### Offer类',
    other: '### 其他'
  };

  for (const [cat, emails] of Object.entries(categories)) {
    if (emails.length > 0) {
      console.log(`${labels[cat]} (${emails.length}封)\n`);
      emails.forEach(e => {
        const date = e.date ? e.date.toLocaleString('zh-CN') : '未知时间';
        console.log(`- **${e.subject}**`);
        console.log(`  - 发件人: ${e.from}`);
        console.log(`  - 时间: ${date}`);
        console.log(`  - 账户: ${e.account}\n`);
      });
    }
  }
}

main().catch(console.error);
