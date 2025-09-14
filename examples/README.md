# Example Images for Car Condition Assessment

This folder contains example images that are displayed to users to help them understand what types of photos to upload for each analysis section.

## Folder Structure

```
examples/
├── dirtiness/          # Example images for dirtiness check (4 photos)
│   ├── front.jpg       # Front view of car
│   ├── side.jpg        # Side view of car
│   ├── rear.jpg        # Rear view of car
│   └── interior.jpg    # Interior view of car
└── condition/          # Example images for condition check (8 photos)
    ├── front_left.jpg      # Front left area
    ├── front_right.jpg     # Front right area
    ├── back_left.jpg       # Back left area
    ├── back_right.jpg      # Back right area
    ├── left_side_1.jpg     # Left side (front)
    ├── left_side_2.jpg     # Left side (rear)
    ├── right_side_1.jpg    # Right side (front)
    └── right_side_2.jpg    # Right side (rear)
```

## How to Add Example Images

1. **Prepare your images**: 
   - Use JPG format for best compatibility
   - Recommended size: 400x300 pixels or similar aspect ratio
   - Keep file sizes reasonable (under 500KB each)

2. **Add dirtiness examples**:
   - Place 4 images in the `dirtiness/` folder
   - Name them exactly as shown above
   - These should show examples of clean and dirty cars from different angles

3. **Add condition examples**:
   - Place 8 images in the `condition/` folder
   - Name them exactly as shown above
   - These should show examples of cars with and without damage from different angles

4. **Fallback behavior**:
   - If an image file is missing, the system will automatically show the text placeholder
   - This ensures the interface still works even if some example images are missing

## Image Guidelines

- **Dirtiness examples**: Show clear examples of clean vs dirty cars
- **Condition examples**: Show examples of cars with various types of damage (scratches, dents, etc.)
- **Quality**: Use clear, well-lit photos that clearly show the relevant features
- **Variety**: Include different car types, colors, and lighting conditions

## File Naming

The file names must match exactly as shown in the folder structure above. The HTML code references these specific filenames, so any changes to the names will require updating the HTML as well.
