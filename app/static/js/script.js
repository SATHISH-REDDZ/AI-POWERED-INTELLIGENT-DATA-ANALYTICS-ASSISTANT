/* ==========================================================================
   AI-POWERED INTELLIGENT DATA ANALYTICS ASSISTANT - FRONTEND ENGINE
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    loadDatasetOverview();
    setupUpload();
    setupCleaningForm();
    setupMLStudio();
    setupPredictionForm();
    setupChat();
    setupReport();
});

// Tab Switching System
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-tab');

            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetId).classList.add('active');

            // Trigger specific tab lazy loads
            if (targetId === 'eda-tab') loadEDA();
            if (targetId === 'visuals-tab') loadVisualizations();
            if (targetId === 'database-tab') loadDatabaseHistory();
            if (targetId === 'report-tab') loadReport();
        });
    });
}

// Load Dataset Metadata & Preview Table
async function loadDatasetOverview() {
    try {
        const res = await fetch('/api/dataset');
        const data = await res.json();

        if (data.error) return;

        // Update Quick Stats Bar
        document.getElementById('stat-rows').innerText = data.rows.toLocaleString();
        document.getElementById('stat-cols').innerText = data.columns;
        document.getElementById('stat-missing').innerText = data.total_missing;
        
        // Render Dataset Preview Table
        const headContainer = document.getElementById('dataset-table-head');
        const bodyContainer = document.getElementById('dataset-table-body');
        
        if (data.sample && data.sample.length > 0) {
            const cols = Object.keys(data.sample[0]);
            headContainer.innerHTML = `<tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr>`;
            
            bodyContainer.innerHTML = data.sample.map(row => {
                return `<tr>${cols.map(c => `<td>${row[c] !== null ? row[c] : '<span style="color:#f43f5e">NaN</span>'}</td>`).join('')}</tr>`;
            }).join('');
        }

        // Populate column selectors for ML
        populateColumnOptions(data.column_names);

    } catch (err) {
        console.error('Failed to load dataset overview:', err);
    }
}

// File Upload Handler
function setupUpload() {
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadStatus = document.getElementById('upload-status');

    if (uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', async () => {
            if (!fileInput.files.length) {
                alert('Please select a CSV file first.');
                return;
            }

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            uploadStatus.innerHTML = '<span style="color:#3b82f6">⏳ Uploading and analyzing dataset...</span>';

            try {
                const res = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await res.json();

                if (result.success) {
                    uploadStatus.innerHTML = `<span style="color:#10b981">✅ ${result.message}</span>`;
                    loadDatasetOverview();
                } else {
                    uploadStatus.innerHTML = `<span style="color:#f43f5e">❌ Error: ${result.error}</span>`;
                }
            } catch (err) {
                uploadStatus.innerHTML = '<span style="color:#f43f5e">❌ Upload failed.</span>';
            }
        });
    }
}

// Preprocessing & Cleaning Form
function setupCleaningForm() {
    const cleanBtn = document.getElementById('run-cleaning-btn');
    const statusBox = document.getElementById('cleaning-status');

    if (cleanBtn) {
        cleanBtn.addEventListener('click', async () => {
            const strategy = document.getElementById('missing-strategy').value;
            const removeDuplicates = document.getElementById('remove-duplicates').checked;
            const encodeCat = document.getElementById('encode-categorical').checked;

            statusBox.innerHTML = '<span style="color:#3b82f6">⏳ Cleaning and updating dataset...</span>';

            try {
                const res = await fetch('/api/clean', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        strategy: strategy,
                        remove_duplicates: removeDuplicates,
                        encode_categorical: encodeCat
                    })
                });
                const result = await res.json();

                if (result.success) {
                    statusBox.innerHTML = `
                        <div style="background:rgba(16,185,129,0.1); border:1px solid #10b981; padding:12px; border-radius:8px; margin-top:10px;">
                            <strong>✅ ${result.message}</strong><br>
                            Initial Shape: ${result.initial_shape[0]} rows × ${result.initial_shape[1]} cols<br>
                            Final Shape: ${result.final_shape[0]} rows × ${result.final_shape[1]} cols<br>
                            Remaining Missing Values: ${result.final_missing}<br>
                            Duplicates Removed: ${result.duplicates_removed}
                        </div>
                    `;
                    loadDatasetOverview();
                }
            } catch (err) {
                statusBox.innerHTML = '<span style="color:#f43f5e">❌ Cleaning process failed.</span>';
            }
        });
    }
}

// Exploratory Data Analysis
async function loadEDA() {
    const edaContainer = document.getElementById('eda-stats-container');
    const insightsBox = document.getElementById('eda-insights-box');

    try {
        const res = await fetch('/api/analysis');
        const data = await res.json();

        if (data.insights) {
            insightsBox.innerText = data.insights;
        }

        if (data.descriptive_stats) {
            const stats = data.descriptive_stats;
            const cols = Object.keys(stats);
            if (cols.length > 0) {
                const metrics = Object.keys(stats[cols[0]]);
                
                let html = `
                    <div class="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Metric / Column</th>
                                    ${cols.map(c => `<th>${c}</th>`).join('')}
                                </tr>
                            </thead>
                            <tbody>
                                ${metrics.map(m => `
                                    <tr>
                                        <td><strong>${m}</strong></td>
                                        ${cols.map(c => `<td>${stats[c][m] !== null && stats[c][m] !== undefined ? (typeof stats[c][m] === 'number' ? stats[c][m].toFixed(2) : stats[c][m]) : '-'}</td>`).join('')}
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
                edaContainer.innerHTML = html;
            }
        }
    } catch (err) {
        console.error('Failed to load EDA stats:', err);
    }
}

// Visualizations Gallery
async function loadVisualizations() {
    const gallery = document.getElementById('visuals-gallery');
    try {
        const res = await fetch('/api/visualizations');
        const data = await res.json();

        if (data.success && data.charts) {
            gallery.innerHTML = `
                <div class="chart-card">
                    <h3>Survival Distribution</h3>
                    <img src="/static/${data.charts.survival}?t=${Date.now()}" alt="Survival Distribution">
                </div>
                <div class="chart-card">
                    <h3>Gender Breakdown</h3>
                    <img src="/static/${data.charts.gender}?t=${Date.now()}" alt="Gender Breakdown">
                </div>
                <div class="chart-card">
                    <h3>Age Distribution Histogram</h3>
                    <img src="/static/${data.charts.age}?t=${Date.now()}" alt="Age Histogram">
                </div>
                <div class="chart-card">
                    <h3>Correlation Heatmap</h3>
                    <img src="/static/${data.charts.heatmap}?t=${Date.now()}" alt="Correlation Heatmap">
                </div>
                <div class="chart-card">
                    <h3>Fare Box Plot by Class</h3>
                    <img src="/static/${data.charts.box_plot}?t=${Date.now()}" alt="Box Plot">
                </div>
            `;
        }
    } catch (err) {
        console.error('Failed to load charts:', err);
    }
}

// Machine Learning Studio Setup
function setupMLStudio() {
    const trainBtn = document.getElementById('train-model-btn');
    const resultBox = document.getElementById('ml-results-box');

    if (trainBtn) {
        trainBtn.addEventListener('click', async () => {
            const algo = document.getElementById('ml-algo-select').value;
            const testSize = document.getElementById('test-size-input').value;

            resultBox.innerHTML = '<span style="color:#3b82f6">⏳ Training Machine Learning Model...</span>';

            try {
                const res = await fetch('/api/train', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        algorithm: algo,
                        test_size: testSize
                    })
                });
                const result = await res.json();

                if (result.success) {
                    // Update global accuracy stat
                    document.getElementById('stat-accuracy').innerText = `${result.accuracy}%`;

                    let cmHtml = '';
                    if (result.confusion_matrix) {
                        cmHtml = `
                            <div style="margin-top:14px;">
                                <strong>Confusion Matrix:</strong>
                                <pre style="background:rgba(0,0,0,0.3); padding:10px; border-radius:6px; margin-top:5px;">TN: ${result.confusion_matrix[0][0]} | FP: ${result.confusion_matrix[0][1]}\nFN: ${result.confusion_matrix[1][0]} | TP: ${result.confusion_matrix[1][1]}</pre>
                            </div>
                        `;
                    }

                    let impHtml = '';
                    if (result.feature_importances && Object.keys(result.feature_importances).length > 0) {
                        impHtml = `
                            <div style="margin-top:14px;">
                                <strong>Feature Importances:</strong>
                                <ul>
                                    ${Object.entries(result.feature_importances).map(([k, v]) => `<li>${k}: ${(v * 100).toFixed(2)}%</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    }

                    resultBox.innerHTML = `
                        <div style="background:rgba(59,130,246,0.1); border:1px solid #3b82f6; padding:16px; border-radius:10px;">
                            <h3 style="color:#10b981;">🎉 Model Trained Successfully!</h3>
                            <p><strong>Algorithm:</strong> ${result.algorithm}</p>
                            <p><strong>Accuracy:</strong> <span style="font-size:1.4rem; color:#10b981; font-weight:700;">${result.accuracy}%</span></p>
                            ${cmHtml}
                            ${impHtml}
                        </div>
                    `;
                }
            } catch (err) {
                resultBox.innerHTML = '<span style="color:#f43f5e">❌ Model training failed.</span>';
            }
        });
    }
}

// Live Interactive Prediction Form Handler
function setupPredictionForm() {
    const predictBtn = document.getElementById('predict-btn');
    const outputBox = document.getElementById('prediction-output');

    if (predictBtn) {
        predictBtn.addEventListener('click', async () => {
            const pclass = document.getElementById('pred-pclass').value;
            const sex = document.getElementById('pred-sex').value;
            const age = document.getElementById('pred-age').value;
            const sibsp = document.getElementById('pred-sibsp').value;
            const parch = document.getElementById('pred-parch').value;
            const fare = document.getElementById('pred-fare').value;
            const embarked = document.getElementById('pred-embarked').value;

            outputBox.innerHTML = '<span style="color:#3b82f6">⏳ Computing prediction...</span>';

            try {
                const res = await fetch('/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        Pclass: pclass,
                        Sex: sex,
                        Age: age,
                        SibSp: sibsp,
                        Parch: parch,
                        Fare: fare,
                        Embarked: embarked
                    })
                });
                const result = await res.json();

                if (result.label) {
                    const color = result.prediction === 1 ? '#10b981' : '#f43f5e';
                    outputBox.innerHTML = `
                        <div style="background:rgba(0,0,0,0.3); border:2px solid ${color}; padding:20px; border-radius:12px; text-align:center;">
                            <h2 style="color:${color}; margin-bottom:8px;">${result.label.toUpperCase()}</h2>
                            <p style="font-size:1.1rem;">Confidence Score: <strong>${result.probability}%</strong></p>
                        </div>
                    `;
                }
            } catch (err) {
                outputBox.innerHTML = '<span style="color:#f43f5e">❌ Prediction request failed.</span>';
            }
        });
    }
}

// AI Assistant Chat Handler
function setupChat() {
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('chat-send-btn');
    const messagesBox = document.getElementById('chat-messages');

    async function sendMessage(text) {
        const q = text || chatInput.value.trim();
        if (!q) return;

        // User Bubble
        const userDiv = document.createElement('div');
        userDiv.className = 'chat-bubble user';
        userDiv.innerText = q;
        messagesBox.appendChild(userDiv);

        if (!text) chatInput.value = '';
        messagesBox.scrollTop = messagesBox.scrollHeight;

        // AI Typing Indicator
        const aiDiv = document.createElement('div');
        aiDiv.className = 'chat-bubble ai';
        aiDiv.innerText = 'Thinking...';
        messagesBox.appendChild(aiDiv);
        messagesBox.scrollTop = messagesBox.scrollHeight;

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: q })
            });
            const data = await res.json();
            aiDiv.innerText = data.response;
            messagesBox.scrollTop = messagesBox.scrollHeight;
        } catch (err) {
            aiDiv.innerText = 'Sorry, could not process query.';
        }
    }

    if (sendBtn) sendBtn.addEventListener('click', () => sendMessage());
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // Prompt chips
    document.querySelectorAll('.chip').forEach(chip => {
        chip.addEventListener('click', () => {
            sendMessage(chip.innerText);
        });
    });
}

// Load Database Logs
async function loadDatabaseHistory() {
    const runsTable = document.getElementById('db-runs-body');
    const predsTable = document.getElementById('db-preds-body');

    try {
        const res = await fetch('/api/history');
        const data = await res.json();

        if (data.model_runs && runsTable) {
            runsTable.innerHTML = data.model_runs.map(r => `
                <tr>
                    <td>#${r.id}</td>
                    <td><strong>${r.algorithm}</strong></td>
                    <td><span style="color:#10b981; font-weight:bold;">${r.accuracy}%</span></td>
                    <td>${r.created_at}</td>
                </tr>
            `).join('');
        }

        if (data.recent_predictions && predsTable) {
            predsTable.innerHTML = data.recent_predictions.map(p => `
                <tr>
                    <td>#${p.id}</td>
                    <td>${p.prediction_label}</td>
                    <td>${p.probability ? p.probability + '%' : '-'}</td>
                    <td><small>${p.input_data_json}</small></td>
                    <td>${p.created_at}</td>
                </tr>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load database logs:', err);
    }
}

// Report Generator
async function loadReport() {
    const reportBox = document.getElementById('executive-report-text');
    try {
        const res = await fetch('/api/report');
        const data = await res.json();
        if (data.report && reportBox) {
            reportBox.innerText = data.report;
        }
    } catch (err) {
        console.error('Failed to load report:', err);
    }
}

function populateColumnOptions(columns) {
    // Optional utility to populate dropdowns if needed
}
