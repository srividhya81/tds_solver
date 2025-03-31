def generate_total_sales_query(ticket_type):
    """
    Generate an SQL query to calculate the total sales of all items in the specified ticket type.

    Args:
        ticket_type (str): The ticket type to filter by (e.g., 'Gold').

    Returns:
        str: The SQL query to calculate the total sales.
    """
    query = f"""
    SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE LOWER(type) = LOWER('{ticket_type}');
    """
    return query