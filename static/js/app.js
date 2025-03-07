document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    const toastElList = document.querySelectorAll('.toast');
    const toasts = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl));
    const voiceModal = new bootstrap.Modal(document.getElementById('voiceModal'));

    // DOM elements
    const commandInput = document.getElementById('command-input');
    const sendButton = document.getElementById('send-command');
    const voiceButton = document.getElementById('voice-input');
    const voiceRecordButton = document.getElementById('voice-record');
    const voiceStatus = document.getElementById('voice-status');
    const voiceTranscript = document.getElementById('voice-transcript');
    const taskList = document.getElementById('task-list');
    const overallProgress = document.getElementById('overall-progress');
    const notificationToast = document.getElementById('notification-toast');
    const chatMessages = document.getElementById('chat-messages');

    // Speech Recognition setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            voiceStatus.textContent = 'Listening...';
            voiceRecordButton.classList.remove('btn-secondary');
            voiceRecordButton.classList.add('btn-danger');
        };

        recognition.onend = () => {
            voiceStatus.textContent = 'Click the microphone to start recording';
            voiceRecordButton.classList.remove('btn-danger');
            voiceRecordButton.classList.add('btn-secondary');
        };

        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0].transcript)
                .join('');
            voiceTranscript.textContent = transcript;

            if (event.results[0].isFinal) {
                commandInput.value = transcript;
                setTimeout(() => {
                    voiceModal.hide();
                    sendCommand();
                }, 1000);
            }
        };

        recognition.onerror = (event) => {
            voiceStatus.textContent = `Error: ${event.error}`;
            voiceRecordButton.classList.remove('btn-danger');
            voiceRecordButton.classList.add('btn-secondary');
        };
    }

    // Load initial tasks
    loadTasks();

    // Event listeners
    sendButton.addEventListener('click', sendCommand);
    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendCommand();
    });

    if (recognition) {
        voiceButton.addEventListener('click', () => {
            voiceModal.show();
            voiceTranscript.textContent = '';
        });

        voiceRecordButton.addEventListener('click', () => {
            if (voiceRecordButton.classList.contains('btn-danger')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    } else {
        voiceButton.style.display = 'none';
    }

    async function loadTasks() {
        try {
            const response = await fetch('/api/tasks');
            const tasks = await response.json();
            renderTasks(tasks);
            updateOverallProgress(tasks);
        } catch (error) {
            showNotification('Error loading tasks', 'danger');
        }
    }

    async function sendCommand() {
        const command = commandInput.value.trim();
        if (!command) return;

        // Add user message to chat
        addMessage(command, 'user');
        commandInput.value = '';

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ command })
            });

            const result = await response.json();

            if (result.success) {
                renderTasks(result.tasks);
                updateOverallProgress(result.tasks);
                addMessage(result.message, 'ai');
            } else {
                addMessage(`I encountered an error: ${result.error}`, 'ai');
            }
        } catch (error) {
            addMessage("I'm sorry, I encountered an error processing your request.", 'ai');
        }
    }

    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = type === 'user' ? 'user-message' : 'ai-message';
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function renderTasks(tasks) {
        console.log('Rendering tasks:', tasks); // Debug log

        if (!tasks || !Array.isArray(tasks)) {
            console.error('Invalid tasks data:', tasks);
            taskList.innerHTML = '<div class="alert alert-warning">No tasks available</div>';
            return;
        }

        // Group tasks by category
        const tasksByCategory = {};
        const uncategorizedTasks = [];

        tasks.forEach(task => {
            console.log('Processing task:', task); // Debug log
            if (task.category && task.category.name) {
                if (!tasksByCategory[task.category.name]) {
                    tasksByCategory[task.category.name] = {
                        color: task.category.color || '#6c757d',
                        tasks: []
                    };
                }
                tasksByCategory[task.category.name].tasks.push(task);
            } else {
                uncategorizedTasks.push(task);
            }
        });

        // Generate HTML for each category
        let html = '';

        // Render categorized tasks
        Object.entries(tasksByCategory).forEach(([categoryName, category]) => {
            html += `
                <div class="category-group">
                    <div class="category-header">
                        <h6 class="category-name" style="background-color: ${category.color}">${categoryName}</h6>
                    </div>
                    ${renderTaskList(category.tasks)}
                </div>
            `;
        });

        // Render uncategorized tasks
        if (uncategorizedTasks.length > 0) {
            html += `
                <div class="category-group uncategorized-tasks">
                    <div class="category-header">
                        <h6 class="category-name" style="background-color: var(--bs-gray-600)">Uncategorized</h6>
                    </div>
                    ${renderTaskList(uncategorizedTasks)}
                </div>
            `;
        }

        // If no tasks at all, show a message
        if (html === '') {
            html = '<div class="alert alert-info">No tasks to display</div>';
        }

        taskList.innerHTML = html;
    }

    function renderTaskList(tasks) {
        return tasks.map(task => `
            <div class="card task-card mb-2 ${task.progress === 100 ? 'completed' : ''}" data-task-id="${task.id}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h5 class="card-title mb-0">${task.title}</h5>
                        <span class="task-due-date">${task.due_date}</span>
                    </div>
                    <p class="task-estimated-time mb-2">
                        <i class="bi bi-clock"></i> ${task.estimated_time}
                    </p>
                    <div class="progress task-progress">
                        <div class="progress-bar" 
                             role="progressbar" 
                             style="width: ${task.progress}%" 
                             aria-valuenow="${task.progress}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    function updateOverallProgress(tasks) {
        if (!tasks.length) {
            overallProgress.style.width = '0%';
            overallProgress.textContent = '0%';
            return;
        }

        const totalProgress = tasks.reduce((sum, task) => sum + task.progress, 0);
        const averageProgress = Math.round(totalProgress / tasks.length);

        overallProgress.style.width = `${averageProgress}%`;
        overallProgress.textContent = `${averageProgress}%`;
    }

    function showNotification(message, type = 'info') {
        const toastBody = notificationToast.querySelector('.toast-body');
        toastBody.textContent = message;
        notificationToast.classList.remove('bg-success', 'bg-danger', 'bg-info');
        notificationToast.classList.add(`bg-${type}`);
        bootstrap.Toast.getOrCreateInstance(notificationToast).show();
    }
});