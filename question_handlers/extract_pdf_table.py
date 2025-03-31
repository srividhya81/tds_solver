import fitz
import pandas as pd

def extract_total_marks(pdf_path, subject_filter, min_marks, target_subject, group_range, include_groups=True):
    """
    Extracts the total marks of a target subject for students who meet the criteria in a specific subject.

    Args:
        pdf_path (str): Path to the PDF file containing tables.
        subject_filter (str): The subject to filter by (e.g., 'Biology').
        min_marks (int): Minimum marks required in the subject_filter.
        target_subject (str): The subject whose total marks need to be calculated (e.g., 'English').
        group_range (tuple): A tuple specifying the range of groups (e.g., (1, 39)).
        include_groups (bool): Whether to include or exclude the specified group range.

    Returns:
        int: Total marks of the target subject for students meeting the criteria.
    """
    if not all([pdf_path, subject_filter, min_marks, target_subject, group_range]):
        raise ValueError("All arguments must be provided and valid.")

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    total_marks = 0

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        tables = page.get_text("blocks")

        for block in tables:
            try:
                # Convert block text to DataFrame
                df = pd.read_csv(pd.compat.StringIO(block[4]))

                # Ensure required columns exist
                if subject_filter in df.columns and target_subject in df.columns and 'Group' in df.columns:
                    # Filter rows based on group range and marks
                    if include_groups:
                        filtered_df = df[(df['Group'].between(group_range[0], group_range[1])) & (df[subject_filter] >= min_marks)]
                    else:
                        filtered_df = df[~(df['Group'].between(group_range[0], group_range[1])) & (df[subject_filter] >= min_marks)]

                    # Sum the target subject marks
                    total_marks += filtered_df[target_subject].sum()
            except Exception as e:
                # Handle parsing errors gracefully
                print(f"Error processing block: {e}")

    pdf_document.close()
    return total_marks