<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart AI Irrigation System</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-green: #10b981;
            --secondary-blue: #3b82f6;
            --dark-bg: #0f172a;
            --card-bg: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--dark-bg) 0%, #1e293b 50%, var(--secondary-blue) 100%);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Login Page */
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .login-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
            animation: slideUp 0.8s ease-out;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .logo {
            text-align: center;
            margin-bottom: 30px;
        }

        .logo h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, var(--primary-green), var(--secondary-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        .google-login {
            background: linear-gradient(45deg, #4285f4, #34a853);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 16px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .google-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(66, 133, 244, 0.4);
        }

        /* Dashboard */
        .dashboard-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .header-title {
            font-size: 2rem;
            background: linear-gradient(45deg, var(--primary-green), var(--secondary-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
            background: var(--card-bg);
            padding: 10px 20px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }

        /* Metrics Cards */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .metric-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
            animation: fadeInUp 0.6s ease-out forwards;
            opacity: 0;
        }

        .metric-card:nth-child(1) { animation-delay: 0.1s; }
        .metric-card:nth-child(2) { animation-delay: 0.2s; }
        .metric-card:nth-child(3) { animation-delay: 0.3s; }
        .metric-card:nth-child(4) { animation-delay: 0.4s; }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .metric-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 30px 60px rgba(0,0,0,0.4);
        }

        .metric-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            opacity: 0.8;
        }

        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 5px;
            background: linear-gradient(45deg, var(--primary-green), var(--secondary-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .metric-label {
            font-size: 0.95rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* AI Decision */
        .ai-decision {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(59, 130, 246, 0.2));
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
        }

        .decision-status {
            font-size: 1.5rem;
            font-weight: 700;
            padding: 15px 30px;
            border-radius: 50px;
            display: inline-block;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }

        .status-on { background: rgba(16, 185, 129, 0.3); color: var(--success); }
        .status-off { background: rgba(239, 68, 68, 0.3); color: var(--danger); }
        .status-moderate { background: rgba(245, 158, 11, 0.3); color: var(--warning); }

        /* Controls Section */
        .controls-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .control-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .form-group select,
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            font-size: 1rem;
        }

        .form-group select:focus,
        .form-group input:focus {
            outline: none;
            border-color: var(--primary-green);
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
        }

        /* Charts */
        .charts-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }

        .chart-container {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 25px;
            height: 300px;
        }

        .chart-title {
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }

        /* Alerts */
        .alerts {
            display: flex;
            flex-direction: column;
            gap: 15px;
            margin-bottom: 30px;
        }

        .alert {
            padding: 15px 20px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            animation: slideInRight 0.5s ease-out;
        }

        .alert.warning { background: rgba(245, 158, 11, 0.2); border-left: 4px solid var(--warning); }
        .alert.danger { background: rgba(239, 68, 68, 0.2); border-left: 4px solid var(--danger); }

        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* Buttons */
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: linear-gradient(45deg, var(--primary-green), #059669);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
        }

        /* Future Scope */
        .future-scope {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .container { padding: 15px; }
            .dashboard-header { flex-direction: column; text-align: center; }
            .metrics-grid,
            .charts-grid,
            .controls-section { grid-template-columns: 1fr; }
            .login-card { padding: 30px 20px; }
            .logo h1 { font-size: 2rem; }
        }

        @media (max-width: 480px) {
            .metric-value { font-size: 2rem; }
            .chart-container { height: 250px; }
        }

        .hidden { display: none; }
    </style>
</head>
<body>
    <!-- Login Page -->
    <div id="loginPage" class="login-container">
        <div class="login-card">
            <div class="logo">
                <h1><i class="fas fa-seedling"></i> Smart AI Irrigation</h1>
                <p style="color: var(--text-secondary); margin-top: 10px;">Intelligent Farm Management System</p>
            </div>
            <button class="google-login" onclick="loginWithGoogle()">
                <i class="fab fa-google"></i>
                Continue with Google
            </button>
        </div>
    </div>

    <!-- Dashboard -->
    <div id="dashboard" class="container hidden">
        <div class="dashboard-header">
            <div>
                <h1 class="header-title">
                    <i class="fas fa-tachometer-alt"></i> Smart Irrigation Dashboard
                </h1>
            </div>
            <div class="user-profile">
                <i class="fas fa-user-circle" style="font-size: 2rem;"></i>
                <span>Farm Owner</span>
                <button class="btn btn-primary" onclick="logout()" style="padding: 8px 16px; font-size: 0.9rem;">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </button>
            </div>
        </div>

        <!-- Metrics -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-icon" style="color: #10b981;"><i class="fas fa-tint"></i></div>
                <div class="metric-value" id="soilMoisture">0%</div>
                <div class="metric-label">Soil Moisture</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon" style="color: #f59e0b;"><i class="fas fa-thermometer-half"></i></div>
                <div class="metric-value" id="temperature">0°C</div>
                <div class="metric-label">Temperature</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon" style="color: #3b82f6;"><i class="fas fa-water"></i></div>
                <div class="metric-value" id="waterLevel">0%</div>
                <div class="metric-label">Water Level</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon" style="color: #8b5cf6;"><i class="fas fa-cloud-rain"></i></div>
                <div class="metric-value" id="rainProb">0%</div>
                <div class="metric-label">Rain Probability</div>
            </div>
        </div>

        <!-- AI Decision -->
        <div class="ai-decision">
            <div class="decision-status" id="decisionStatus">Loading...</div>
            <div id="decisionReason" style="font-size: 1.1rem; color: var(--text-secondary); margin-top: 10px;"></div>
            <div id="nextIrrigation" style="font-size: 1rem; color: var(--text-secondary); margin-top: 5px;"></div>
        </div>

        <!-- Controls & Alerts -->
        <div class="controls-section">
            <div class="control-card">
                <h3 style="margin-bottom: 20px; color: var(--text-primary);"><i class="fas fa-seedling"></i> Crop Selection</h3>
                <div class="form-group">
                    <label>Crop Type</label>
                    <select id="cropSelect" onchange="updateIrrigationMethod()">
                        <option value="Rice">Rice</option>
                        <option value="Wheat">Wheat</option>
                        <option value="Maize">Maize</option>
                        <option value="Cotton">Cotton</option>
                    </select>
                </div>
                <div id="irrigationMethod" style="font-size: 1.1rem; font-weight: 700; color: var(--primary-green);"></div>
            </div>
            <div class="control-card">
                <h3 style="margin-bottom: 20px; color: var(--text-primary);"><i class="fas fa-bell"></i> Farm Alerts</h3>
                <div class="alerts" id="alertsContainer"></div>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
            <div class="chart-container">
                <div class="chart-title">Soil Moisture Trend (Last 5 Days)</div>
                <canvas id="moistureChart"></canvas>
            </div>
            <div class="chart-container">
                <div class="chart-title">Water Usage vs Saved</div>
                <canvas id="waterChart"></canvas>
            </div>
        </div>

        <!-- Future Scope -->
        <div class="future-scope">
            <h3 style="margin-bottom: 20px;"><i class="fas fa-rocket"></i> Future Scope</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; text-align: left;">
                <div><i class="fas fa-satellite" style="color: var(--primary-green); margin-right: 10px;"></i>IoT Sensors Integration</div>
                <div><i class="fas fa-cloud-sun" style="color: var(--secondary-blue); margin-right: 10px;"></i>Real-time Weather API</div>
                <div><i class="fas fa-brain" style="color: #8b5cf6; margin-right: 10px;"></i>ML-based Prediction Model</div>
                <div><i class="fas fa-mobile-alt" style="color: var(--warning); margin-right: 10px;"></i>Mobile App</div>
            </div>
        </div>
    </div>

    <script>
        // Simulated user data
        const userData = { loggedIn: false, email: '' };

        // Real-time sensor data
        let sensors = {
            soilMoisture: 50,
            temperature: 25,
            waterLevel: 70,
            rainProb: 30
        };

        // Charts data
        let moistureChart, waterChart;
        let moistureData = [45, 52, 48, 55, 62];
        let waterUsageData = [120, 110, 95, 105, 88];
        let waterSavedData = [30, 35, 42, 38, 45];

        // Initialize app
        function init() {
            setupCharts();
            simulateSensors();
            setInterval(simulateSensors, 2500);
            setInterval(checkAlerts, 1000);
        }

        // Google Login Simulation
        function loginWithGoogle() {
            userData.loggedIn = true;
            userData.email = 'farmer@example.com';
            document.getElementById('loginPage').classList.add('hidden');
            document.getElementById('dashboard').classList.remove('hidden');
            init();
        }

        function logout() {
            userData.loggedIn = false;
            document.getElementById('dashboard').classList.add('hidden');
            document.getElementById('loginPage').classList.remove('hidden');
        }

        // Sensor Simulation
        function simulateSensors() {
            sensors.soilMoisture = Math.max(10, Math.min(95, sensors.soilMoisture + (Math.random() - 0.5) * 8));
            sensors.temperature = Math.max(15, Math.min(45, sensors.temperature + (Math.random() - 0.5) * 3));
            sensors.waterLevel = Math.max(20, Math.min(100, sensors.waterLevel + (Math.random() - 0.5) * 5));
            sensors.rainProb = Math.max(0, Math.min(100, sensors.rainProb + (Math.random() - 0.5) * 15));

            updateDisplay();
            updateAI decision();
            updateCharts();
        }

        function updateDisplay() {
            document.getElementById('soilMoisture').textContent = `${Math.round(sensors.soilMoisture)}%`;
            document.getElementById('temperature').textContent = `${Math.round(sensors.temperature)}°C`;
            document.getElementById('waterLevel').textContent = `${Math.round(sensors.waterLevel)}%`;
            document.getElementById('rainProb').textContent = `${Math.round(sensors.rainProb)}%`;
        }

        // AI Decision Engine
        function updateAIDecision() {
            const { soilMoisture, rainProb } = sensors;
            const statusEl = document.getElementById('decisionStatus');
            const reasonEl = document.getElementById('decisionReason');
            const nextEl = document.getElementById('nextIrrigation');

            let status, reason, nextTime;

            if (soilMoisture < 30 && rainProb < 40) {
                status = 'Irrigation ON';
                reason = 'Low soil moisture and minimal rain expected';
                nextTime = 'Irrigating now...';
                statusEl.className = 'decision-status status-on';
            } else if (rainProb > 60) {
                status = 'Irrigation OFF';
                reason = 'High rain probability detected';
                nextTime = 'Next check in 2 hours';
                statusEl.className = 'decision-status status-off';
            } else {
                status = 'Moderate Irrigation';
                reason = 'Optimal conditions - conserving water';
                nextTime = 'Scheduled for evening';
                statusEl.className = 'decision-status status-moderate';
            }

            statusEl.textContent = status;
            reasonEl.textContent = reason;
            nextEl.textContent = nextTime;
        }

        // Crop Intelligence
        const cropMethods = {
            Rice: 'Flood Irrigation',
            Wheat: 'Drip Irrigation',
            Maize: 'Sprinkler',
            Cotton: 'Drip Irrigation'
        };

        function updateIrrigationMethod() {
            const crop = document.getElementById('cropSelect').value;
            document.getElementById('irrigationMethod').textContent = 
                `Recommended: ${cropMethods[crop]}`;
        }

        // Alerts System
        function checkAlerts() {
            const alertsContainer = document.getElementById('alertsContainer');
            let alerts = [];

            if (sensors.soilMoisture < 25) {
                alerts.push({ type: 'danger', message: 'Critical: Soil moisture very low!' });
            } else if (sensors.soilMoisture < 35) {
                alerts.push({ type: 'warning', message: 'Low soil moisture detected' });
            }

            if (sensors.temperature > 38) {
                alerts.push({ type: 'danger', message: `High temperature: ${Math.round(sensors.temperature)}°C` });
            } else if (sensors.temperature > 35) {
                alerts.push({ type: 'warning', message: 'Temperature rising' });
            }

            if (sensors.waterLevel < 25) {
                alerts.push({ type: 'danger', message: 'Water tank critically low!' });
            }

            alertsContainer.innerHTML = alerts.map(alert => 
                `<div class="alert ${alert.type}">
                    <i class="fas fa-exclamation-triangle"></i>
                    ${alert.message}
                </div>`
            ).join('');
        }

        // Charts Setup
        function setupCharts() {
            const moistureCtx = document.getElementById('moistureChart').getContext('2d');
            moistureChart = new Chart(moistureCtx, {
                type: 'line',
                data: {
                    labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
                    datasets: [{
                        label: 'Soil Moisture (%)',
                        data: moistureData,
                        borderColor: 'rgba(16, 185, 129, 1)',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    },
                    plugins: { legend: { display: false } }
                }
            });

            const waterCtx = document.getElementById('waterChart').getContext('2d');
            waterChart = new Chart(waterCtx, {
                type: 'bar',
                data: {
                    labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
                    datasets: [
                        {
                            label: 'Water Used (L)',
                            data: waterUsageData,
                            backgroundColor: 'rgba(59, 130, 246, 0.7)'
                        },
                        {
                            label: 'Water Saved (L)',
                            data: waterSavedData,
                            backgroundColor: 'rgba(16, 185, 129, 0.7)'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        function updateCharts() {
            // Update moisture trend
            moistureData.push(sensors.soilMoisture);
            if (moistureData.length > 5) moistureData.shift();
            moistureChart.data.datasets[0].data = moistureData;
            moistureChart.update('none');

            // Update water charts
            waterUsageData.push(Math.round(Math.random() * 50 + 80));
            waterSavedData.push(Math.round(Math.random() * 20 + 30));
            if (waterUsageData.length > 5) {
                waterUsageData.shift();
                waterSavedData.shift();
            }
            waterChart.data.datasets[0].data = waterUsageData;
            waterChart.data.datasets[1].data = waterSavedData;
            waterChart.update('none');
        }

        // Initialize crop method on load
        updateIrrigationMethod();
    </script>
</body>
</html>
