const API_BASE_URL = 'http://localhost:8000';

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Update menu
    document.querySelectorAll('.menu a').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected tab
    const tab = document.getElementById(tabName);
    if (tab) {
        tab.classList.add('active');
        // Update title
        const titles = {
            'dashboard': 'Dashboard',
            'market-analysis': 'Market Analysis',
            'user-research': 'User Research',
            'roadmap': 'Roadmap Planning',
            'features': 'Feature Prioritization',
            'strategy': 'Strategy Development',
            'analytics': 'Analytics & Metrics'
        };
        document.getElementById('page-title').textContent = titles[tabName] || 'Dashboard';
    }
}

function switchResearchTab(tabName) {
    document.querySelectorAll('.research-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
}

function switchStrategyTab(tabName) {
    document.querySelectorAll('.strategy-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
}

// Utility functions
async function fetchAPI(endpoint, data) {
    try {
        updateStatus('Loading...');
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const result = await response.json();
        updateStatus('Ready');
        return result;
    } catch (error) {
        console.error('API Error:', error);
        updateStatus('Error');
        throw error;
    }
}

function updateStatus(message) {
    document.getElementById('status').textContent = message;
}

function showResults(containerId, data) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<h4>Results:</h4><pre>${JSON.stringify(data, null, 2)}</pre>`;
        container.classList.add('show');
    }
}

function showError(containerId, error) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `<div class="error">Error: ${error}</div>`;
        container.classList.add('show');
    }
}

// Form handlers
async function analyzeMarket(event) {
    event.preventDefault();
    const market = document.getElementById('market-input').value;
    const competitors = document.getElementById('competitors-input').value
        .split(',').map(c => c.trim()).filter(c => c);
    const focus_areas = document.getElementById('focus-areas').value
        .split(',').map(c => c.trim()).filter(c => c);

    try {
        const result = await fetchAPI('/analyze/market', {
            market,
            competitors: competitors.length ? competitors : undefined,
            focus_areas: focus_areas.length ? focus_areas : undefined
        });
        showResults('market-results', result.data);
    } catch (error) {
        showError('market-results', error.message);
    }
}

async function analyzeInterviews(event) {
    event.preventDefault();
    const transcripts = document.getElementById('interviews-input').value
        .split('---')
        .map(t => t.trim())
        .filter(t => t);

    if (!transcripts.length) {
        showError('interview-results', 'Please provide at least one interview transcript');
        return;
    }

    try {
        const result = await fetchAPI('/analyze/interviews', { transcripts });
        showResults('interview-results', result.data);
    } catch (error) {
        showError('interview-results', error.message);
    }
}

async function analyzeSurveys(event) {
    event.preventDefault();
    try {
        const data = JSON.parse(document.getElementById('surveys-input').value);
        const result = await fetchAPI('/synthesize/user-research', data);
        showResults('survey-results', result.data);
    } catch (error) {
        showError('survey-results', 'Invalid JSON or ' + error.message);
    }
}

async function synthesizeResearch(event) {
    event.preventDefault();
    try {
        const data = JSON.parse(document.getElementById('synthesis-input').value);
        const result = await fetchAPI('/synthesize/user-research', data);
        showResults('synthesis-results', result.data);
    } catch (error) {
        showError('synthesis-results', 'Invalid JSON or ' + error.message);
    }
}

async function generateRoadmap(event) {
    event.preventDefault();
    try {
        const product_vision = document.getElementById('product-vision').value;
        const goals = document.getElementById('roadmap-goals').value
            .split('\n').map(g => g.trim()).filter(g => g);
        const features = JSON.parse(document.getElementById('roadmap-features').value);
        const timeline_quarters = parseInt(document.getElementById('timeline-quarters').value);

        const result = await fetchAPI('/generate/roadmap', {
            product_vision,
            goals,
            features,
            timeline_quarters
        });
        showResults('roadmap-results', result.data);
    } catch (error) {
        showError('roadmap-results', 'Invalid input or ' + error.message);
    }
}

async function scoreFeatures(event) {
    event.preventDefault();
    try {
        const features = JSON.parse(document.getElementById('features-list').value);
        const framework = document.getElementById('framework').value;

        const result = await fetchAPI('/score/features', {
            features,
            framework
        });
        showResults('features-results', result.data);
    } catch (error) {
        showError('features-results', 'Invalid JSON or ' + error.message);
    }
}

async function generateStrategy(event) {
    event.preventDefault();
    try {
        const context = JSON.parse(document.getElementById('strategy-context').value);
        const objectives = document.getElementById('strategy-objectives').value
            .split('\n').map(o => o.trim()).filter(o => o);

        const result = await fetchAPI('/generate/strategy', {
            context,
            objectives
        });
        showResults('strategy-results', result.data);
    } catch (error) {
        showError('strategy-results', 'Invalid input or ' + error.message);
    }
}

async function generateGTM(event) {
    event.preventDefault();
    try {
        const product_info = JSON.parse(document.getElementById('gtm-product').value);
        const market_info = JSON.parse(document.getElementById('gtm-market').value);

        const result = await fetchAPI('/generate/gtm', {
            product_info,
            market_info
        });
        showResults('gtm-results', result.data);
    } catch (error) {
        showError('gtm-results', 'Invalid JSON or ' + error.message);
    }
}

async function analyzeMetrics(event) {
    event.preventDefault();
    try {
        const metrics = JSON.parse(document.getElementById('metrics-input').value);

        const result = await fetchAPI('/analyze/metrics', { metrics });
        showResults('analytics-results', result.data);
    } catch (error) {
        showError('analytics-results', 'Invalid JSON or ' + error.message);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set up menu links
    document.querySelectorAll('.menu a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            document.querySelectorAll('.menu a').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });

    // Initialize with dashboard
    switchTab('dashboard');
});
