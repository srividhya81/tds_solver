from PIL import Image
import io
import base64
import logging

def reconstruct_image(image, mapping):
    logging.info(f"Received mapping: {mapping}")
    # Ensure mapping is a list of tuples
    try:
        mapping = [tuple(item) for item in mapping]
        for item in mapping:
            if len(item) != 4:
                raise ValueError(f"Invalid mapping item: {item}. Each item must have exactly four elements.")
        logging.info(f"Validated mapping: {mapping}")
    except Exception as e:
        logging.error(f"Error validating mapping: {e}")
        raise ValueError("Invalid mapping format. Each item must be a list or tuple with exactly four elements.")

    img_width, img_height = image.size
    piece_size = img_width // 5  

    reconstructed = Image.new('RGB', (img_width, img_height))

    for original_row, original_col, scrambled_row, scrambled_col in mapping:
        left = scrambled_col * piece_size
        upper = scrambled_row * piece_size
        right = left + piece_size
        lower = upper + piece_size
        
        piece = image.crop((left, upper, right, lower))
        
        new_left = original_col * piece_size
        new_upper = original_row * piece_size
        reconstructed.paste(piece, (new_left, new_upper))

    buffered = io.BytesIO()
    reconstructed.save(buffered, format="PNG")
    base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"image_base64": base64_str}


