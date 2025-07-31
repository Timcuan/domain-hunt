// Penguin-OS Main JavaScript
// Terminal-style typing effect and utilities

// Typing effect function
function typeLine(element, text, speed = 50, callback = null) {
  let i = 0;
  element.innerHTML = '';
  
  const interval = setInterval(() => {
    if (i < text.length) {
      element.innerHTML += text.charAt(i++);
    } else {
      clearInterval(interval);
      if (callback) callback();
    }
  }, speed);
}

// Blinking cursor effect
function createBlinkingCursor(element) {
  let isVisible = true;
  setInterval(() => {
    isVisible = !isVisible;
    element.style.opacity = isVisible ? '1' : '0';
  }, 500);
}

// Simulate terminal boot sequence
function simulateBoot(element) {
  const bootMessages = [
    'Penguin-OS :: Abstract Chain Interface',
    'Initializing blockchain protocols...',
    'Loading Pudgy Penguin modules...',
    'Establishing secure connections...',
    'Penguin-OS ready for deployment!',
    '',
    'Welcome to Penguin-OS! 🐧',
    'Type --help for available commands'
  ];
  
  let currentIndex = 0;
  
  function typeNextMessage() {
    if (currentIndex < bootMessages.length) {
      const message = bootMessages[currentIndex];
      const line = document.createElement('div');
      line.className = 'text-cyan-300 font-mono';
      element.appendChild(line);
      
      typeLine(line, message, 30, () => {
        currentIndex++;
        setTimeout(typeNextMessage, 200);
      });
    }
  }
  
  typeNextMessage();
}

// Desktop window management
function toggleWindow(windowId) {
  const window = document.getElementById(windowId);
  if (window) {
    window.classList.toggle('hidden');
  }
}

// Simulate typing in chat
function simulateChatTyping(inputElement, messages) {
  let currentIndex = 0;
  
  function typeNextMessage() {
    if (currentIndex < messages.length) {
      const message = messages[currentIndex];
      inputElement.value = '';
      inputElement.placeholder = message;
      
      let i = 0;
      const interval = setInterval(() => {
        if (i < message.length) {
          inputElement.placeholder = message.substring(0, i + 1);
          i++;
        } else {
          clearInterval(interval);
          currentIndex++;
          setTimeout(typeNextMessage, 2000);
        }
      }, 100);
    }
  }
  
  typeNextMessage();
}

// Initialize page-specific functionality
document.addEventListener('DOMContentLoaded', function() {
  // Add blinking cursor to prompts
  const cursors = document.querySelectorAll('.cursor');
  cursors.forEach(cursor => createBlinkingCursor(cursor));
  
  // Initialize typing effects
  const typeElements = document.querySelectorAll('[data-type]');
  typeElements.forEach(element => {
    const text = element.getAttribute('data-type');
    const speed = parseInt(element.getAttribute('data-speed')) || 50;
    typeLine(element, text, speed);
  });
  
  // Initialize boot sequence if present
  const bootElement = document.getElementById('boot-sequence');
  if (bootElement) {
    simulateBoot(bootElement);
  }
  
  // Initialize chat simulation if present
  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    const chatMessages = [
      'Connecting to Penguin network...',
      'Establishing secure channel...',
      'Ready for communication!',
      'Type your message below...'
    ];
    simulateChatTyping(chatInput, chatMessages);
  }
});