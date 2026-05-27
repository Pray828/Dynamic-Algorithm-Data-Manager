def bubble_sort(data, column, reverse=False):
    """Sorts a list of dictionaries using the Bubble Sort algorithm."""
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            val1 = data[j][column]
            val2 = data[j+1][column]
            
            # Comparison flags based on sort order (Ascending vs Descending)
            if (not reverse and val1 > val2) or (reverse and val1 < val2):
                data[j], data[j+1] = data[j+1], data[j]
    return data

def selection_sort(data, column, reverse=False):
    """An alternative sorting option (Selection Sort) to fulfill 'choose an algorithm'."""
    n = len(data)
    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            val1 = data[j][column]
            val2 = data[target_idx][column]
            if (not reverse and val1 < val2) or (reverse and val1 > val2):
                target_idx = j
        data[i], data[target_idx] = data[target_idx], data[i]
    return data

def linear_search(data, column, search_term):
    """Searches a column for a specific value (Supports case-insensitive partial match)."""
    results = []
    for record in data:
        # Convert values to strings safely to handle dates, booleans, and numbers
        if search_term.lower() in str(record[column]).lower():
            results.append(record)
    return results