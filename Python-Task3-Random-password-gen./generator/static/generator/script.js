document.addEventListener('DOMContentLoaded', () => {
    const lengthSlider = document.getElementById('length');
    const lengthInput = document.getElementById('lengthInput');
    const lengthValue = document.getElementById('lengthValue');
    const charTypeCheckboxes = document.querySelectorAll('input[name="char_type"]');
    const excludeAmbiguous = document.getElementById('excludeAmbiguous');
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const passwordText = document.getElementById('passwordText');
    const strengthSection = document.getElementById('strengthSection');
    const strengthBar = document.getElementById('strengthBar');
    const strengthLabel = document.getElementById('strengthLabel');
    const historyList = document.getElementById('historyList');
    const errorMsg = document.getElementById('errorMsg');
    const toast = document.getElementById('toast');

    let currentPassword = '';
    const history = [];

    // Sync slider and number input
    lengthSlider.addEventListener('input', () => {
        lengthInput.value = lengthSlider.value;
        lengthValue.textContent = lengthSlider.value;
    });

    lengthInput.addEventListener('input', () => {
        let val = parseInt(lengthInput.value);
        if (isNaN(val) || val < 8) val = 8;
        if (val > 64) val = 64;
        lengthInput.value = val;
        lengthSlider.value = val;
        lengthValue.textContent = val;
    });

    // Generate password
    generateBtn.addEventListener('click', () => {
        const length = parseInt(lengthInput.value) || 16;
        const selectedTypes = [];
        charTypeCheckboxes.forEach(cb => {
            if (cb.checked) selectedTypes.push(cb.value);
        });

        if (selectedTypes.length < 2) {
            errorMsg.textContent = 'Select at least 2 character types.';
            return;
        }
        if (length < 8) {
            errorMsg.textContent = 'Password length must be at least 8.';
            return;
        }

        errorMsg.textContent = '';

        const formData = new FormData();
        formData.append('length', length);
        selectedTypes.forEach(t => formData.append('char_types[]', t));
        formData.append('exclude_ambiguous', excludeAmbiguous.checked ? 'true' : 'false');
        formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        generateBtn.disabled = true;
        generateBtn.textContent = 'Generating...';

        fetch('/generate/', {
            method: 'POST',
            body: formData,
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                errorMsg.textContent = data.error;
                return;
            }

            currentPassword = data.password;
            passwordText.textContent = currentPassword;
            passwordText.classList.remove('placeholder');

            copyBtn.disabled = false;

            // Update strength bar
            strengthSection.style.display = 'flex';
            strengthBar.style.width = data.strength_percent + '%';
            strengthBar.style.background = data.strength_color;
            strengthLabel.textContent = data.strength_label;
            strengthLabel.style.color = data.strength_color;

            // Add to history
            addToHistory(currentPassword);
        })
        .catch(() => {
            errorMsg.textContent = 'Something went wrong. Try again.';
        })
        .finally(() => {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate Password';
        });
    });

    // Copy to clipboard
    copyBtn.addEventListener('click', () => {
        if (!currentPassword) return;
        navigator.clipboard.writeText(currentPassword).then(() => {
            showToast('Copied to clipboard!');
        }).catch(() => {
            // Fallback
            const textarea = document.createElement('textarea');
            textarea.value = currentPassword;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            showToast('Copied to clipboard!');
        });
    });

    function addToHistory(password) {
        history.unshift(password);
        if (history.length > 5) history.pop();
        renderHistory();
    }

    function renderHistory() {
        historyList.innerHTML = '';
        if (history.length === 0) {
            historyList.innerHTML = '<li class="empty-history">No passwords generated yet</li>';
            return;
        }
        history.forEach((pw, i) => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="history-pw">${escapeHtml(pw)}</span>
                <button class="history-copy" data-index="${i}">Copy</button>
            `;
            historyList.appendChild(li);
        });

        document.querySelectorAll('.history-copy').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.target.getAttribute('data-index'));
                navigator.clipboard.writeText(history[index]).then(() => {
                    showToast('Copied to clipboard!');
                });
            });
        });
    }

    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2000);
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
