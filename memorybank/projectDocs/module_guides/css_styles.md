# CSS Styles Module Guide

## Overview
The `css/styles.py` module manages the dynamic generation of CSS styles for the Divrei Yoel AI Chat application. It handles proper styling for RTL Hebrew text, font configuration, and consistent visual appearance throughout the application.

## Key Functions

### `generate_app_css(text_direction, hebrew_font)`
- **Purpose**: Generates the main CSS for the application
- **Parameters**:
  - `text_direction`: Current text direction ("rtl" or "ltr")
  - `hebrew_font`: Selected Hebrew font
- **Returns**: String containing CSS rules
- **Key Features**:
  - Dynamic font configuration
  - RTL/LTR text handling
  - Consistent component styling
  - Responsive layout rules

### `generate_dynamic_css(text_direction, hebrew_font)`
- **Purpose**: Creates additional CSS for dynamically generated content
- **Parameters**:
  - `text_direction`: Current text direction ("rtl" or "ltr")
  - `hebrew_font`: Selected Hebrew font
- **Returns**: String containing CSS rules for dynamic content
- **Key Features**:
  - Styling for chat messages
  - RTL-specific overrides
  - Font consistency across dynamic elements

## CSS Component Categories

### Font Definitions
```css
@font-face {
    font-family: 'David';
    src: local('David');
}
@font-face {
    font-family: 'Narkisim';
    src: local('Narkisim');
}
```
- Font face declarations for Hebrew-compatible fonts
- Fallback fonts for cross-platform compatibility

### Global Element Styling
```css
body, button, div, p, h1, h2, h3, span {
    font-family: '${hebrew_font}', Arial, sans-serif !important;
}
```
- Universal font application
- Important declarations to override Streamlit defaults
- Consistent typography throughout the application

### RTL/LTR Text Handling
```css
.rtl-text {
    direction: rtl;
    text-align: right;
    font-family: '${hebrew_font}', Arial, sans-serif !important;
}
.ltr-text {
    direction: ltr;
    text-align: left;
}
```
- Direction-specific text styling
- Font family specifications for each direction
- Text alignment rules

### Button Styling
```css
button {
    font-family: '${hebrew_font}', Arial, sans-serif !important;
    font-size: 14px !important;
}
```
- Consistent button appearance
- Font size optimization for Hebrew text
- Overrides for Streamlit's default button styling

### App Title and Heading Styling
```css
.app-title {
    text-align: center;
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 1rem;
}
```
- Center-aligned title styling
- Proper sizing and margins
- Font weight and appearance rules

### Citation Display
```css
.citation {
    display: inline-block;
    border-radius: 3px;
    padding: 0 4px;
    margin: 0 2px;
    background-color: rgba(175, 184, 193, 0.2);
    font-size: 0.9em;
}
```
- Special formatting for citation numbers
- Visual distinction from regular text
- Subtle background highlighting

### Hebrew Source Text Display
```css
.hebrew-source {
    font-family: '${hebrew_font}', Arial, sans-serif !important;
    direction: rtl;
    text-align: right;
    padding: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
    margin: 5px 0;
}
```
- Specialized styling for Hebrew source text
- Visual container with background and borders
- Proper RTL configuration

### Prompt Gallery Styling
```css
.stButton button {
    width: 100%;
    text-align: ${text_direction === "rtl" ? "right" : "left"};
    direction: ${text_direction};
    white-space: normal !important;
    height: auto !important;
    padding: 0.5rem;
}
```
- Full-width buttons for the prompt gallery
- Direction-aware text alignment
- Multi-line text support with normal white space
- Consistent padding and sizing

### Streamlit Element Overrides
```css
.stTextInput input, .stTextArea textarea {
    font-family: '${hebrew_font}', Arial, sans-serif !important;
    direction: ${text_direction};
    text-align: ${text_direction === "rtl" ? "right" : "left"};
}
```
- Font family overrides for input elements
- Direction-aware alignment
- Consistent styling with rest of application

## RTL-Specific Adaptations
The module provides several RTL-specific adaptations:
- Text alignment for chat messages
- Button text alignment
- Input field direction
- Source document presentation
- Citation display positioning

## CSS Reloading Mechanism
The module works with app.py to ensure CSS updates are properly applied:
- Timestamped CSS keys force browser refreshes
- Separate dynamic and main CSS blocks
- Unique identifiers for CSS sections

## Recent Enhancements
- Improved RTL support for Hebrew text
- Added font preview capabilities
- Enhanced button styling for better usability
- Optimized responsive design for various screen sizes
- Improved citation display formatting
- Enhanced consistency across UI elements
- Added chat element styling overrides 