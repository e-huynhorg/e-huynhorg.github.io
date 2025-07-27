# Multi-language Website Structure

Your website now supports 3 languages with the following structure:

## Files Created:
- `lang/en.json` - English translations
- `lang/sv.json` - Swedish translations  
- `lang/vi.json` - Vietnamese translations
- Updated `index.html` with language switching functionality

## Features:
1. **Language Switcher**: Dropdown in the top-right corner
2. **URL Persistence**: Language preference saved in URL (`?lang=sv`)
3. **Local Storage**: Remembers user's language choice
4. **Browser Detection**: Automatically detects Swedish/Vietnamese browsers
5. **English Fallback**: Falls back to English if translation missing
6. **Dynamic Content**: Education list and CV links update based on language

## How to Edit Content:

### Adding/Editing Translations:
1. Edit the respective JSON files in the `lang/` folder
2. Follow the nested structure for new sections
3. Use HTML tags in content for formatting (`<strong>`, `<em>`, etc.)

### Adding New Sections:
1. Add the section to all language JSON files
2. Add HTML with `data-i18n` attribute in `index.html`
3. The JavaScript will automatically populate the content

### Example of adding a new section:

In each language file (`lang/en.json`, `lang/sv.json`, `lang/vi.json`):
```json
{
  "sections": {
    "skills": {
      "title": "Skills",
      "content": "My technical skills include..."
    }
  }
}
```

In `index.html`:
```html
<section id="skills">
  <h2 data-i18n="sections.skills.title">Skills</h2>
  <p data-i18n="sections.skills.content">Default content</p>
</section>
```

## Testing:
1. Open your website
2. Try switching languages using the dropdown
3. Refresh the page - it should remember your choice
4. Try URLs like `index.html?lang=sv` or `index.html?lang=vi`

The system is now ready for you to edit each language file independently!
