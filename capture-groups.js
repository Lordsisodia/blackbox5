#!/usr/bin/env node
/**
 * Capture Telegram Group IDs
 * Run this to get group chat IDs when messages are sent
 */

const TelegramBot = require('node-telegram-bot-api');

const BOT_TOKEN = '8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo';
const bot = new TelegramBot(BOT_TOKEN, { polling: true });

console.log('🤖 Listening for messages to capture group IDs...');
console.log('Send a message in each group to see the chat ID\n');

bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const chatType = msg.chat.type;
  const chatTitle = msg.chat.title || 'Direct Message';
  const fromName = msg.from?.first_name || 'Unknown';

  console.log('═══════════════════════════════════════');
  console.log(`Chat Title: ${chatTitle}`);
  console.log(`Chat ID: ${chatId}`);
  console.log(`Chat Type: ${chatType}`);
  console.log(`From: ${fromName}`);
  console.log(`Message: ${msg.text || '(no text)'}`);
  console.log('═══════════════════════════════════════\n');

  // Reply with the chat ID
  if (chatType === 'group' || chatType === 'supergroup') {
    bot.sendMessage(chatId, `This group chat ID is: \`${chatId}\``, {
      parse_mode: 'Markdown'
    });
  }
});

console.log('Press Ctrl+C to stop\n');
