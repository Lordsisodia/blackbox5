#!/usr/bin/env node
/**
 * Enhanced Task Agent Bridge v2
 * Full CRUD operations with conversational metadata collection
 */

const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');

const BOT_TOKEN = '8339689516:AAFs2t-7Bk_Igq-0uIIVwPF6Ge1iLMVpKug';
const CHAT_ID = '7643203581';
const USER_ID = 'a95135f0-1970-474a-850c-d280fc6ca217';
const SUPABASE_URL = 'https://avdgyrepwrvsvwgxrccr.supabase.co';

// Load Supabase key
const env = fs.readFileSync('/opt/moltbot/agents/task-agent/.env', 'utf8');
const keyMatch = env.match(/SUPABASE_ANON_KEY=(.+)/);
const SUPABASE_KEY = keyMatch ? keyMatch[1].trim() : '';

const bot = new TelegramBot(BOT_TOKEN, { polling: true });
console.log('🤖 Enhanced Task Agent Bridge started...');

// Conversation state management
const userConversations = new Map();

// Task creation flow states
const CREATION_STATES = {
  IDLE: 'idle',
  AWAITING_TITLE: 'awaiting_title',
  AWAITING_TYPE: 'awaiting_type',
  AWAITING_PRIORITY: 'awaiting_priority',
  AWAITING_DURATION: 'awaiting_duration',
  AWAITING_DATE: 'awaiting_date',
  AWAITING_SUBTASKS: 'awaiting_subtasks'
};

// Supabase API helpers
async function supabaseGet(endpoint) {
  const response = await fetch(`${SUPABASE_URL}/rest/v1/${endpoint}`, {
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`
    }
  });
  return response.json();
}

async function supabasePost(endpoint, data) {
  const response = await fetch(`${SUPABASE_URL}/rest/v1/${endpoint}`, {
    method: 'POST',
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=representation'
    },
    body: JSON.stringify(data)
  });
  return response.json();
}

async function supabasePatch(endpoint, data) {
  const response = await fetch(`${SUPABASE_URL}/rest/v1/${endpoint}`, {
    method: 'PATCH',
    headers: {
      'apikey': SUPABASE_KEY,
      'Authorization': `Bearer ${SUPABASE_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  });
  return response.ok;
}

// Get tasks with subtasks
async function getDeepWorkTasks(limit = 10) {
  return supabaseGet(`deep_work_tasks?select=*&completed=eq.false&user_id=eq.${USER_ID}&order=priority.asc&limit=${limit}`);
}

async function getLightWorkTasks(limit = 10) {
  return supabaseGet(`light_work_tasks?select=*&completed=eq.false&user_id=eq.${USER_ID}&order=priority.asc&limit=${limit}`);
}

async function getDeepSubtasks(taskId) {
  return supabaseGet(`deep_work_subtasks?select=*&task_id=eq.${taskId}&completed=eq.false`);
}

async function getLightSubtasks(taskId) {
  return supabaseGet(`light_work_subtasks?select=*&task_id=eq.${taskId}&completed=eq.false`);
}

// Create tasks
async function createDeepTask(taskData) {
  const payload = {
    ...taskData,
    user_id: USER_ID,
    completed: false
  };
  return supabasePost('deep_work_tasks', payload);
}

async function createLightTask(taskData) {
  const payload = {
    ...taskData,
    user_id: USER_ID,
    completed: false
  };
  return supabasePost('light_work_tasks', payload);
}

async function createDeepSubtask(taskId, title) {
  return supabasePost('deep_work_subtasks', {
    task_id: taskId,
    title,
    completed: false
  });
}

// Complete tasks
async function completeDeepTask(taskId) {
  return supabasePatch(`deep_work_tasks?id=eq.${taskId}`, { completed: true });
}

async function completeLightTask(taskId) {
  return supabasePatch(`light_work_tasks?id=eq.${taskId}`, { completed: true });
}

async function completeDeepSubtask(subtaskId) {
  return supabasePatch(`deep_work_subtasks?id=eq.${subtaskId}`, { completed: true });
}

// Format tasks with subtasks for display
async function formatTasksWithSubtasks() {
  const tasks = await getDeepWorkTasks(5);
  let message = '*🔴 DEEP WORK TASKS*\n\n';

  if (tasks.length === 0) {
    message += 'No active deep work tasks\n';
  } else {
    for (const task of tasks) {
      const subtasks = await getDeepSubtasks(task.id);
      const icon = task.priority === 'URGENT' ? '🔴' : task.priority === 'HIGH' ? '🟠' : '🟡';

      message += `${icon} *${task.title}*\n`;
      message += `ID: \`${task.id.substring(0, 8)}...\` | Priority: ${task.priority}`;

      if (task.estimated_duration) {
        message += ` | Est: ${task.estimated_duration}m`;
      }
      if (task.focus_blocks) {
        message += ` | ${task.focus_blocks} blocks`;
      }
      if (task.task_date) {
        message += ` | Due: ${task.task_date}`;
      }
      message += '\n';

      if (subtasks.length > 0) {
        message += `📎 ${subtasks.length} subtasks:\n`;
        subtasks.slice(0, 3).forEach((sub, idx) => {
          const isLast = idx === Math.min(subtasks.length - 1, 2);
          message += `  ${isLast ? '└' : '├'} ○ ${sub.title}\n`;
        });
        if (subtasks.length > 3) {
          message += `  └ ...and ${subtasks.length - 3} more\n`;
        }
      }
      message += '\n';
    }
  }

  return message;
}

// Format light tasks
async function formatLightTasks() {
  const tasks = await getLightWorkTasks(5);
  let message = '*🟢 LIGHT WORK TASKS*\n\n';

  if (tasks.length === 0) {
    message += 'No active light work tasks\n';
  } else {
    for (const task of tasks) {
      const icon = task.priority === 'URGENT' ? '🔴' : task.priority === 'HIGH' ? '🟠' : '🟢';
      message += `${icon} *${task.title}*\n`;
      message += `ID: \`${task.id.substring(0, 8)}...\` | Priority: ${task.priority}`;

      if (task.estimated_duration) {
        message += ` | Est: ${task.estimated_duration}m`;
      }
      message += '\n\n';
    }
  }

  return message;
}

// Generate morning briefing
async function generateMorningBriefing() {
  const deepTasks = await getDeepWorkTasks(20);
  const lightTasks = await getLightWorkTasks(20);

  const urgentCount = deepTasks.filter(t => t.priority === 'URGENT').length;
  const today = new Date().toISOString().split('T')[0];
  const dueToday = deepTasks.filter(t => t.task_date === today);

  let message = `*📋 SISO Tasks - ${today}*\n\n`;

  if (urgentCount > 0) {
    message += `🔴 *URGENT: ${urgentCount} tasks*\n`;
    deepTasks.filter(t => t.priority === 'URGENT').slice(0, 3).forEach(t => {
      message += `• ${t.title}\n`;
    });
    message += '\n';
  }

  if (dueToday.length > 0) {
    message += `📅 *DUE TODAY*\n`;
    dueToday.forEach(t => {
      message += `• ${t.title}\n`;
    });
    message += '\n';
  }

  message += `📊 *Summary*\n`;
  message += `• Deep Work: ${deepTasks.length} active\n`;
  message += `• Light Work: ${lightTasks.length} active\n`;
  message += `• Total: ${deepTasks.length + lightTasks.length} tasks\n\n`;

  message += '_Commands: /tasks, /deep, /light, /add_';

  return message;
}

// Handle task creation flow
async function handleTaskCreation(chatId, text, state) {
  switch (state.step) {
    case CREATION_STATES.AWAITING_TITLE:
      state.data.title = text;
      state.step = CREATION_STATES.AWAITING_TYPE;

      await bot.sendMessage(chatId,
        `Great! "${text}"\n\nIs this *Deep Work* (focused, creative) or *Light Work* (admin, quick tasks)?`, {
        parse_mode: 'Markdown',
        reply_markup: {
          inline_keyboard: [
            [{ text: '🔴 Deep Work', callback_data: 'type_deep' }],
            [{ text: '🟢 Light Work', callback_data: 'type_light' }]
          ]
        }
      });
      break;

    case CREATION_STATES.AWAITING_PRIORITY:
      state.data.priority = text.toUpperCase();
      state.step = CREATION_STATES.AWAITING_DURATION;

      await bot.sendMessage(chatId,
        `Priority set to *${state.data.priority}*\n\nHow long do you think this will take? (in minutes, or type "skip")`, {
        parse_mode: 'Markdown'
      });
      break;

    case CREATION_STATES.AWAITING_DURATION:
      if (text.toLowerCase() !== 'skip') {
        const duration = parseInt(text);
        if (!isNaN(duration)) {
          state.data.estimated_duration = duration;
        }
      }
      state.step = CREATION_STATES.AWAITING_DATE;

      await bot.sendMessage(chatId,
        `Got it! ${state.data.estimated_duration ? `Estimated: ${state.data.estimated_duration}m` : 'No estimate'}\n\nWhen is this due? (YYYY-MM-DD format, or type "skip")`, {
        parse_mode: 'Markdown'
      });
      break;

    case CREATION_STATES.AWAITING_DATE:
      if (text.toLowerCase() !== 'skip' && /^\d{4}-\d{2}-\d{2}$/.test(text)) {
        state.data.task_date = text;
      }

      // Create the task
      let result;
      if (state.data.type === 'deep') {
        result = await createDeepTask(state.data);
      } else {
        result = await createLightTask(state.data);
      }

      if (result && result[0]) {
        const taskId = result[0].id;
        state.taskId = taskId;
        state.step = CREATION_STATES.AWAITING_SUBTASKS;

        await bot.sendMessage(chatId,
          `✅ *Task created!*\n\n"${state.data.title}"\nPriority: ${state.data.priority}\n${state.data.estimated_duration ? `Duration: ${state.data.estimated_duration}m\n` : ''}${state.data.task_date ? `Due: ${state.data.task_date}\n` : ''}\nWould you like to add subtasks? (reply with subtask names, one per line, or "done")`, {
          parse_mode: 'Markdown'
        });
      } else {
        await bot.sendMessage(chatId, '❌ Failed to create task. Please try again.');
        userConversations.delete(chatId);
      }
      break;

    case CREATION_STATES.AWAITING_SUBTASKS:
      if (text.toLowerCase() === 'done') {
        await bot.sendMessage(chatId, '✅ Task creation complete! Use /tasks to see all your tasks.');
        userConversations.delete(chatId);
      } else {
        // Add subtask
        await createDeepSubtask(state.taskId, text);
        await bot.sendMessage(chatId, `✅ Added subtask: "${text}"\n\nAdd another or type "done"`);
      }
      break;
  }
}

// Handle callback queries
bot.on('callback_query', async (query) => {
  const chatId = query.message.chat.id;
  const data = query.data;

  if (data.startsWith('type_')) {
    const state = userConversations.get(chatId);
    if (state) {
      state.data.type = data === 'type_deep' ? 'deep' : 'light';
      state.step = CREATION_STATES.AWAITING_PRIORITY;

      await bot.editMessageText(
        `Great! "${state.data.title}"\n\nType: ${state.data.type === 'deep' ? '🔴 Deep Work' : '🟢 Light Work'}\n\nWhat's the priority? (URGENT, HIGH, MEDIUM, LOW)`,
        {
          chat_id: chatId,
          message_id: query.message.message_id,
          parse_mode: 'Markdown'
        }
      );
    }
  }

  await bot.answerCallbackQuery(query.id);
});

// Handle commands
bot.onText(/\/start/, async (msg) => {
  const welcome = `*🤖 SISO Task Agent*\n\nI can help you manage your tasks with full read/write access to your Supabase database.\n\n*Commands:*\n/tasks - Show deep work tasks with subtasks\n/light - Show light work tasks\n/add - Create a new task (interactive)\n/briefing - Morning briefing\n/complete [ID] - Mark task complete\n\n*Features:*\n• View tasks with connected subtasks\n• Create tasks with metadata (priority, duration, due date)\n• Add subtasks interactively\n• Mark tasks complete\n\nJust chat with me naturally or use commands!`;

  await bot.sendMessage(msg.chat.id, welcome, { parse_mode: 'Markdown' });
});

bot.onText(/\/tasks/, async (msg) => {
  bot.sendChatAction(msg.chat.id, 'typing');
  const message = await formatTasksWithSubtasks();
  await bot.sendMessage(msg.chat.id, message, { parse_mode: 'Markdown' });
});

bot.onText(/\/deep/, async (msg) => {
  bot.sendChatAction(msg.chat.id, 'typing');
  const message = await formatTasksWithSubtasks();
  await bot.sendMessage(msg.chat.id, message, { parse_mode: 'Markdown' });
});

bot.onText(/\/light/, async (msg) => {
  bot.sendChatAction(msg.chat.id, 'typing');
  const message = await formatLightTasks();
  await bot.sendMessage(msg.chat.id, message, { parse_mode: 'Markdown' });
});

bot.onText(/\/briefing/, async (msg) => {
  bot.sendChatAction(msg.chat.id, 'typing');
  const message = await generateMorningBriefing();
  await bot.sendMessage(msg.chat.id, message, { parse_mode: 'Markdown' });
});

bot.onText(/\/add/, async (msg) => {
  userConversations.set(msg.chat.id, {
    step: CREATION_STATES.AWAITING_TITLE,
    data: {}
  });

  await bot.sendMessage(msg.chat.id,
    '*Create New Task*\n\nWhat\'s the task title?', {
    parse_mode: 'Markdown'
  });
});

bot.onText(/\/complete (.+)/, async (msg, match) => {
  const taskId = match[1];
  bot.sendChatAction(msg.chat.id, 'typing');

  // Try deep work first, then light work
  let success = await completeDeepTask(taskId);
  if (!success) {
    success = await completeLightTask(taskId);
  }

  if (success) {
    await bot.sendMessage(msg.chat.id, '✅ Task marked as complete!');
  } else {
    await bot.sendMessage(msg.chat.id, '❌ Could not find task with that ID. Use /tasks to see task IDs.');
  }
});

// Handle natural language messages
bot.on('message', async (msg) => {
  if (msg.chat.id.toString() !== CHAT_ID) return;
  if (!msg.text || msg.text.startsWith('/')) return;

  const text = msg.text;
  const chatId = msg.chat.id;

  // Check if user is in a creation flow
  const state = userConversations.get(chatId);
  if (state && state.step !== CREATION_STATES.IDLE) {
    await handleTaskCreation(chatId, text, state);
    return;
  }

  bot.sendChatAction(chatId, 'typing');

  // Natural language processing
  const lowerText = text.toLowerCase();

  if (lowerText.includes('add') || lowerText.includes('create') || lowerText.includes('new task')) {
    userConversations.set(chatId, {
      step: CREATION_STATES.AWAITING_TITLE,
      data: {}
    });

    await bot.sendMessage(chatId,
      '*Create New Task*\n\nWhat\'s the task title?', {
      parse_mode: 'Markdown'
    });

  } else if (lowerText.includes('morning') || lowerText.includes('briefing') || lowerText.includes('today')) {
    const message = await generateMorningBriefing();
    await bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });

  } else if (lowerText.includes('deep work') || lowerText.includes('deep')) {
    const message = await formatTasksWithSubtasks();
    await bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });

  } else if (lowerText.includes('light work') || lowerText.includes('light')) {
    const message = await formatLightTasks();
    await bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });

  } else if (lowerText.includes('task') || lowerText.includes('what') || lowerText.includes('show')) {
    const message = await formatTasksWithSubtasks();
    await bot.sendMessage(chatId, message, { parse_mode: 'Markdown' });

  } else {
    // Helpful response
    await bot.sendMessage(chatId,
      `I'm not sure what you need. Try:\n\n• "show tasks" - See your tasks\n• "add task" - Create new task\n• "morning briefing" - Daily summary\n• /help - See all commands`, {
      parse_mode: 'Markdown'
    });
  }
});

console.log('Enhanced bridge is running. Press Ctrl+C to stop.');
