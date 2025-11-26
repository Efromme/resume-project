// Your API endpoint
const DEPLOYMENTS_API = 'https://dha8uvgm1f.execute-api.us-east-1.amazonaws.com/prod/deployments';

document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Loading deployment history...');
    fetchDeployments();
});

async function fetchDeployments() {
    try {
        const response = await fetch(DEPLOYMENTS_API);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('📊 Deployments received:', data);

        if (data.deployments && data.deployments.length > 0) {
            displayLatestDeployment(data.deployments[0]);
            displayDeploymentHistory(data.deployments);
        } else {
            document.getElementById('latest-deployment').innerHTML =
                '<p class="text-muted">No deployments recorded yet.</p>';
        }

    } catch (error) {
        console.error('❌ Error loading deployments:', error);
        document.getElementById('latest-deployment').innerHTML =
            '<p class="text-danger">Unable to load deployment status</p>';
    }
}

function displayLatestDeployment(deployment) {
    const timeAgo = getTimeAgo(deployment.timestamp * 1000);
    
    // Build commit link - only if URL exists and is valid
    const commitLink = (deployment.commit_url && deployment.commit_url.startsWith('http'))
        ? `<a href="${deployment.commit_url}" target="_blank" class="text-decoration-none">
             <code>${deployment.commit_sha}</code>
             <i class="fas fa-external-link-alt fa-xs ms-1"></i>
           </a>`
        : `<code>${deployment.commit_sha}</code>`;
    
    // Build workflow link - only if URL exists and is valid
    const workflowLink = (deployment.workflow_url && deployment.workflow_url.startsWith('http'))
        ? `<a href="${deployment.workflow_url}" target="_blank" class="text-decoration-none">
             View GitHub Actions
             <i class="fas fa-external-link-alt fa-xs ms-1"></i>
           </a>`
        : `<span class="text-muted">Not available</span>`;
    
    const html = `
        <div class="row">
            <div class="col-md-8">
                <h5>
                    <span class="badge bg-success">✅ SUCCESS</span>
                    <span class="ms-2">${escapeHtml(deployment.commit_message)}</span>
                </h5>
                <p class="mb-1">
                    <strong>Commit:</strong> ${commitLink}
                </p>
                <p class="mb-1">
                    <strong>Author:</strong> ${escapeHtml(deployment.commit_author)}
                </p>
                <p class="mb-1">
                    <strong>Branch:</strong> ${deployment.branch}
                </p>
                <p class="mb-0">
                    <strong>Pipeline:</strong> ${workflowLink}
                </p>
            </div>
            <div class="col-md-4 text-end">
                <p class="text-muted mb-3">${timeAgo}</p>
                <div class="badge bg-info mb-2">
                    <i class="fab fa-aws"></i> AWS Lambda
                </div>
                <br>
                <div class="badge bg-secondary">
                    <i class="fab fa-cloudflare"></i> CloudFront
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('latest-deployment').innerHTML = html;
}

function displayDeploymentHistory(deployments) {
    const html = deployments.map(dep => {
        // Use timestamp (Unix seconds) instead of deployed_at (ISO string)
        const timeAgo = getTimeAgo(dep.timestamp * 1000);

        return `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <span class="badge bg-success">✅</span>
                    <span class="ms-2">${escapeHtml(dep.commit_message)}</span>
                    <small class="text-muted ms-2">(${dep.commit_sha})</small>
                </div>
                <small class="text-muted">${timeAgo}</small>
            </div>
        `;
    }).join('');

    document.getElementById('deployment-history').innerHTML = html;
}

function getTimeAgo(timestampMs) {
    // timestampMs is Unix timestamp in milliseconds
    const now = Date.now();
    const diff = now - timestampMs;

    // Handle clock skew or future timestamps
    if (diff < 0) {
        return 'just now';
    }

    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) return `${days}d ago`;
    if (hours > 0) return `${hours}h ago`;
    if (minutes > 0) return `${minutes}m ago`;
    if (seconds > 10) return `${seconds}s ago`;
    return 'just now';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}