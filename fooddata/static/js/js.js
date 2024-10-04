function sortTable(columnKey) {
    const messageDiv = document.getElementById('sort-message');
    messageDiv.textContent = `Sorting column: ${columnKey}`;

    const table = document.getElementById('data-table');
    const tbody = table.getElementsByTagName('tbody')[0];
    const rows = Array.from(tbody.getElementsByTagName('tr'));

    // Find the index of the column to sort
    const columnIndex = Array.from(table.getElementsByTagName('th')).findIndex(th => th.textContent.trim() === columnKey);

    // If column not found, exit
    if (columnIndex === -1) {
        console.error(`Column ${columnKey} not found`);
        return;
    }

    // Determine the current sorting order
    const isAscending = !table.dataset.sortOrder || table.dataset.sortOrder === 'desc';
    table.dataset.sortOrder = isAscending ? 'asc' : 'desc';

    // Sort the rows
    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].textContent.trim();
        const cellB = rowB.cells[columnIndex].textContent.trim();

        if (columnKey === 'DATE') { // Adjust to your actual date column name
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