document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('liveCustomerSearch');
    const resultsContainer = document.getElementById('liveSearchResults');
    const customerSelect = document.getElementById('id_customer_select');
    const searchApiUrl = searchInput ? (searchInput.dataset.searchUrl || '/service/customers/api/search/') : '/service/customers/api/search/';

    let debounceTimeout = null;

    if (searchInput && resultsContainer && customerSelect) {
        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimeout);
            const query = this.value.trim();

            if (query.length < 2) {
                resultsContainer.classList.add('d-none');
                resultsContainer.innerHTML = '';
                return;
            }

            debounceTimeout = setTimeout(() => {
                fetch(`${searchApiUrl}?q=${encodeURIComponent(query)}`)
                    .then((res) => res.json())
                    .then((data) => {
                        resultsContainer.innerHTML = '';
                        if (data.results && data.results.length > 0) {
                            resultsContainer.classList.remove('d-none');
                            data.results.forEach((c) => {
                                const item = document.createElement('a');
                                item.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center py-2 px-3';
                                item.href = '#';
                                item.innerHTML = `
                                    <div>
                                        <strong class="text-dark">${escapeHtml(c.name)}</strong> 
                                        <span class="text-muted small font-monospace">(${escapeHtml(c.customer_id)})</span>
                                        <div class="text-muted small">${escapeHtml(c.phone)} • ${escapeHtml(c.address || 'Musiri / Trichy')}</div>
                                    </div>
                                    <span class="btn btn-sm btn-primary rounded-pill py-0 px-2" style="font-size: 11px;">Select</span>
                                `;

                                item.addEventListener('click', (e) => {
                                    e.preventDefault();
                                    let option = Array.from(customerSelect.options).find((opt) => opt.value == c.id);
                                    if (!option) {
                                        option = new Option(`${c.name} (${c.customer_id} - ${c.phone})`, c.id, true, true);
                                        customerSelect.add(option);
                                    }
                                    customerSelect.value = c.id;
                                    resultsContainer.classList.add('d-none');
                                    searchInput.value = `${c.name} (${c.phone})`;
                                });

                                resultsContainer.appendChild(item);
                            });
                        } else {
                            resultsContainer.classList.remove('d-none');
                            resultsContainer.innerHTML = `
                                <div class="list-group-item text-muted small py-3 text-center">
                                    No customer matches found for "${escapeHtml(query)}".
                                    <br>Click <strong>"+ Quick Add New Customer"</strong> to create a new profile.
                                </div>
                            `;
                        }
                    })
                    .catch((err) => {
                        console.error('Customer search failed:', err);
                    });
            }, 250);
        });

        document.addEventListener('click', (e) => {
            if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
                resultsContainer.classList.add('d-none');
            }
        });
    }

    const saveQuickCustomerBtn = document.getElementById('saveQuickCustomerBtn');
    if (saveQuickCustomerBtn) {
        saveQuickCustomerBtn.addEventListener('click', () => {
            const nameInput = document.getElementById('quick_name');
            const phoneInput = document.getElementById('quick_phone');
            const addressInput = document.getElementById('quick_address');
            const alertBox = document.getElementById('quickCustomerAlert');

            const name = nameInput ? nameInput.value.trim() : '';
            const phone = phoneInput ? phoneInput.value.trim() : '';
            const address = addressInput ? addressInput.value.trim() : '';

            if (alertBox) {
                alertBox.classList.add('d-none');
                alertBox.textContent = '';
            }

            if (!name || !phone) {
                if (alertBox) {
                    alertBox.textContent = 'Please enter both customer name and mobile number.';
                    alertBox.classList.remove('d-none');
                } else {
                    alert('Please enter both customer name and mobile number.');
                }
                return;
            }

            const apiUrl = saveQuickCustomerBtn.dataset.apiUrl || '/service/customers/api/quick-create/';
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';

            const originalBtnText = saveQuickCustomerBtn.innerHTML;
            saveQuickCustomerBtn.disabled = true;
            saveQuickCustomerBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span> Saving...';

            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ name, phone, address })
            })
            .then((res) => res.json())
            .then((data) => {
                saveQuickCustomerBtn.disabled = false;
                saveQuickCustomerBtn.innerHTML = originalBtnText;

                if (data.success && data.customer) {
                    const c = data.customer;
                    if (customerSelect) {
                        let option = Array.from(customerSelect.options).find((opt) => opt.value == c.id);
                        if (!option) {
                            option = new Option(`${c.name} (${c.customer_id} - ${c.phone})`, c.id, true, true);
                            customerSelect.add(option);
                        }
                        customerSelect.value = c.id;
                    }

                    if (searchInput) {
                        searchInput.value = `${c.name} (${c.phone})`;
                    }

                    if (nameInput) nameInput.value = '';
                    if (phoneInput) phoneInput.value = '';
                    if (addressInput) addressInput.value = '';
                    if (alertBox) alertBox.classList.add('d-none');

                    const modalEl = document.getElementById('quickAddCustomerModal');
                    if (modalEl && window.bootstrap) {
                        const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                        modalInstance.hide();
                    }
                } else {
                    if (alertBox) {
                        alertBox.textContent = data.error || 'Failed to create customer.';
                        alertBox.classList.remove('d-none');
                    } else {
                        alert(data.error || 'Failed to create customer.');
                    }
                }
            })
            .catch((err) => {
                saveQuickCustomerBtn.disabled = false;
                saveQuickCustomerBtn.innerHTML = originalBtnText;
                console.error('Quick customer creation failed:', err);
                if (alertBox) {
                    alertBox.textContent = 'Server communication error. Please try again.';
                    alertBox.classList.remove('d-none');
                }
            });
        });
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
