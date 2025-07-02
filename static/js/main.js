// Main JavaScript for Square Game Fundraiser

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Slug generation for fundraiser form
    const nameInput = document.getElementById('name');
    const slugInput = document.getElementById('slug');
    if (nameInput && slugInput) {
        nameInput.addEventListener('input', function() {
            if (!slugInput.dataset.manual) {
                const slug = nameInput.value
                    .toLowerCase()
                    .replace(/[^a-z0-9]+/g, '-')
                    .replace(/(^-|-$)/g, '');
                slugInput.value = slug;
            }
        });

        slugInput.addEventListener('input', function() {
            slugInput.dataset.manual = 'true';
        });
    }

    // Image preview on file upload
    const imageInput = document.querySelector('input[type="file"][accept*="image"]');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Progress bar animation
    animateProgressBars();
});

// Show image preview
function showImagePreview(src) {
    let previewContainer = document.getElementById('imagePreview');
    if (!previewContainer) {
        const container = document.createElement('div');
        container.id = 'imagePreview';
        container.className = 'mt-3';
        container.innerHTML = `
            <p class="text-muted">Preview:</p>
            <img src="${src}" alt="Preview" class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
        `;
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput && fileInput.parentElement) {
            fileInput.parentElement.appendChild(container);
        }
    } else {
        const img = previewContainer.querySelector('img');
        if (img) {
            img.src = src;
        }
    }
}

// Animate progress bars
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(function() {
            bar.style.width = width;
        }, 100);
    });
}

// Helper function for AJAX requests
function fetchJSON(url, options = {}) {
    return fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    });
}

// Export data function
function exportData(fundraiserId, type) {
    window.location.href = `/admin/fundraiser/${fundraiserId}/export?type=${type}`;
}

// Update grid progress via AJAX
function updateProgress(fundraiserId) {
    fetchJSON(`/api/fundraiser/${fundraiserId}/progress`)
        .then(data => {
            const progressBar = document.querySelector(`#progress-${fundraiserId} .progress-bar`);
            if (progressBar) {
                progressBar.style.width = `${data.progress_percentage}%`;
                progressBar.textContent = `${data.sold_squares} / ${data.total_squares} sold`;
            }
        })
        .catch(error => console.error('Error updating progress:', error));
} 