document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    const toastElList = document.querySelectorAll('.toast');
    const toasts = [...toastElList].map(toastEl => new bootstrap.Toast(toastEl));

    // DOM elements
    const commandInput = document.getElementById('command-input');
    const sendButton = document.getElementById('send-command');
    const taskList = document.getElementById('task-list');
    const overallProgress = document.getElementById('overall-progress');
    const notificationToast = document.getElementById('notification-toast');
    const chatMessages = document.getElementById('chat-messages');

    // Load initial tasks
    loadTasks();

    // Event listeners
    sendButton.addEventListener('click', sendCommand);
    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendCommand();
    });

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
        taskList.innerHTML = tasks.map(task => `
            <div class="list-group-item task-card ${task.progress === 100 ? 'completed' : ''}" data-task-id="${task.id}">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5 class="mb-0">${task.title}</h5>
                    <span class="task-due-date">Due: ${task.due_date}</span>
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