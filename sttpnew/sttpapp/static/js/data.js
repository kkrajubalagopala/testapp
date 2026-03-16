<script>
    document.addEventListener('DOMContentLoaded', () => {
    const trfForm = document.getElementById('trfForm');
    const savetrfButton = document.getElementById('savetrfButton');
    const trfTableBody = document.getElementById('trfTableBody');
    const messageDiv = document.getElementById('message');

    // Handle form submission
    trfForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(trfForm);
        const response = await fetch('/save_trf/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            },
        });

        const data = await response.json();
        messageDiv.innerText = data.msg || '';

        setTimeout(() => {
            messageDiv.innerText = '';
        }, 3000);

        if (data.trfdata) {
            updateTrfTable(data.trfdata);
            trfForm.reset();
            savetrfButton.innerHTML = 'Save <i class="bi bi-save-fill"></i>';
            trfForm.querySelector('#trans_id').value = '';  // Clear the hidden id field
        }
    });

    // Handle edit icon click
    trfTableBody.addEventListener('click', async (event) => {
        if (event.target.classList.contains('edit-icon')) {
            const trfId = event.target.dataset.trfId;
            const response = await fetch('/edit_trf/', {
                method: 'POST',
                body: new URLSearchParams({ 'trans_id': trfId }),
                headers: {
                    'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            });

            const data = await response.json();
            if (data.error) {
                messageDiv.innerText = data.error;
                setTimeout(() => {
                    messageDiv.innerText = '';
                }, 3000);
            } else {
                document.getElementById('trans_id').value = trfId;
                document.getElementById('trf_type').value = data.trf_type;
                document.getElementById('trf_rating').value = data.trf_rating;
                document.getElementById('trf_id').value = data.trf_id;
                document.getElementById('trf_title').value = data.trf_title;
                document.getElementById('prim_voltage').value = data.prim_voltage;
                document.getElementById('prim_busno').value = data.prim_busno;
                document.getElementById('sec_voltage').value = data.sec_voltage;
                document.getElementById('sec_busno').value = data.sec_busno;
                document.getElementById('prim_busname').value = data.prim_busname;
                document.getElementById('sec_busname').value = data.sec_busname;
                savetrfButton.innerHTML = 'Update <i class="bi bi-save-fill"></i>';
            }
        }
    });

    // Handle delete icon click
    trfTableBody.addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-icon')) {
            const trfId = event.target.dataset.trfId;
            if (confirm('Are you sure you want to delete this Transformer?')) {
                const response = await fetch('/delete_trf/', {
                    method: 'POST',
                    body: new URLSearchParams({ 'trans_id': trfId }),
                    headers: {
                        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                    },
                });

                const data = await response.json();
                messageDiv.innerText = data.msg || data.error;

                setTimeout(() => {
                    messageDiv.innerText = '';
                }, 3000);

                if (!data.error) {
                    const row = event.target.closest('tr');
                    row.remove();
                }
            }
        }
    });

    function updateTrfTable(trfdata) {
        trfTableBody.innerHTML = '';
        trfdata.forEach((tdata, index) => {
            const row = `<tr>
                <td>${index + 1}</td>
                <td>${tdata.trf_type}</td>
                <td>${tdata.trf_rating}</td>
                <td>${tdata.trf_id}</td>
                <td>${tdata.trf_title}</td>
                <td>${tdata.prim_voltage}</td>
                <td>${tdata.prim_busno}</td>
                <td>${tdata.sec_voltage}</td>
                <td>${tdata.sec_busno}</td>
                <td>${tdata.prim_busname}</td>
                <td>${tdata.sec_busname}</td>
                <td class="text-center"><i class="bi bi-pencil-fill edit-icon" style="cursor: pointer;" data-trf-id="${tdata.id}"></i></td>
                <td class="text-center"><i class="bi bi-trash-fill delete-icon" style="cursor: pointer;" data-trf-id="${tdata.id}"></i></td>
            </tr>`;
            trfTableBody.insertAdjacentHTML('beforeend', row);
        });
    }
});

</script>
