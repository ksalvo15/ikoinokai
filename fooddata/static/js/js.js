function sortTable(columnKey) {
    const messageDiv = document.getElementById('sort-message');

    // Log the column key to ensure the click event is triggered
    messageDiv.textContent = `Sorting column: ${columnKey}`;

    const table = document.getElementById('data-table');
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = Array.from(tbody.getElementsByTagName('tr'));

    const columnIndex = Array.from(table.getElementsByTagName('th')).findIndex(th => th.textContent === columnKey);

    // Determine the current sorting order
    const isAscending = !table.dataset.sortOrder || table.dataset.sortOrder === 'desc';
    table.dataset.sortOrder = isAscending ? 'asc' : 'desc';

    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].textContent;
        const cellB = rowB.cells[columnIndex].textContent;

        if (columnKey === 'DATE') {
            // Convert cell values to Date objects for comparison
            const dateA = new Date(cellA);
            const dateB = new Date(cellB);
            return isAscending ? dateA - dateB : dateB - dateA;
        } else {
            return isAscending ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        }
    });

    // Clear and append the sorted rows
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
}