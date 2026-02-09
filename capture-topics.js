#!/usr/bin/env node
/**
 * Capture Telegram Topic IDs
 * Run this to get topic IDs when messages are sent in topics
 */

const TelegramBot = require('node-telegram-bot-api');

const BOT_TOKEN = '8581639813:AAFA13wDTKEX2x6J-lVfpq9QHnsGRnB1EZo';
const bot = new TelegramBot(BOT_TOKEN, { polling: true });

console.log('🤖 Listening for messages to capture topic IDs...');
console.log('Send a message in each topic to see the topic ID\n');

bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const chatType = msg.chat.type;
  const chatTitle = msg.chat.title || 'Direct Message';
  const fromName = msg.from?.first_name || 'Unknown';
  const topicId = msg.message_thread_id || 'General (no topic)';

  console.log('═══════════════════════════════════════');
  console.log(`Chat Title: ${chatTitle}`);
  console.log(`Chat ID: ${chatId}`);
  console.log(`Topic ID: ${topicId}`);
  console.log(`Chat Type: ${chatType}`);
  console.log(`From: ${fromName}`);
  console.log(`Message: ${msg.text || '(no text)'}`);
  console.log('═══════════════════════════════════════\n');

  // Reply with the IDs
  if (chatType === 'supergroup') {
    const response = `Chat ID: \`${chatId}\`\nTopic ID: \`${topicId}\``;
    bot.sendMessage(chatId, response, {
      parse_mode: 'Markdown',
      message_thread_id: msg.message_thread_id
    });
  }
});

console.log('Press Ctrl+C to stop\n');
