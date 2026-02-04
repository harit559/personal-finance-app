# Custom Fonts Guide

Your app now uses custom fonts! Here's everything you need to know.

## Current Fonts

✅ **Inter** - Main font for all text (clean, modern, professional)
✅ **JetBrains Mono** - For numbers and amounts (monospace, easy to read)

## How to Use

### 1. Regular Text (automatically applied)
All text uses **Inter** by default - no changes needed!

### 2. Numbers/Amounts
Add classes to make numbers look great:

```html
<!-- Option 1: Use the 'amount' class -->
<span class="amount">$1,234.56</span>

<!-- Option 2: Use Tailwind's font-mono class -->
<span class="font-mono">$1,234.56</span>
```

### 3. Headings with custom weight
```html
<h1 class="font-light">Light Heading</h1>
<h2 class="font-normal">Normal Heading</h2>
<h3 class="font-medium">Medium Heading</h3>
<h4 class="font-semibold">Semibold Heading</h4>
<h5 class="font-bold">Bold Heading</h5>
```

## Want Different Fonts?

### Option A: Change Google Fonts (Easy)

1. **Visit Google Fonts:**
   - Go to https://fonts.google.com/
   - Browse and select fonts you like

2. **Popular Choices:**
   - **Poppins** - Friendly, rounded
   - **Roboto** - Clean, professional
   - **Montserrat** - Elegant, geometric
   - **Open Sans** - Highly readable
   - **Lato** - Modern, warm
   - **Source Code Pro** - Great for numbers

3. **Copy the link:**
   - Click "Get font" → "Get embed code"
   - Copy the `<link>` tag

4. **Update `templates/base.html`:**
   - Replace line 9 (the Google Fonts link) with your new link
   - Update the Tailwind config (lines 15-23) with your font names

**Example - Changing to Poppins:**

```html
<!-- Replace the Google Fonts link -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<!-- Update the Tailwind config -->
<script>
    tailwind.config = {
        theme: {
            extend: {
                fontFamily: {
                    'sans': ['Poppins', 'system-ui', 'sans-serif'],
                }
            }
        }
    }
</script>
```

### Option B: Use Local Font Files (Advanced)

If you have custom `.ttf`, `.woff`, or `.woff2` font files:

1. **Create fonts directory:**
   ```
   static/fonts/
   └── YourFont.woff2
   ```

2. **Add to `templates/base.html`:**
   ```html
   <style>
       @font-face {
           font-family: 'YourFont';
           src: url('/static/fonts/YourFont.woff2') format('woff2');
           font-weight: 400;
           font-style: normal;
       }
       
       body {
           font-family: 'YourFont', sans-serif;
       }
   </style>
   ```

## Font Weight Reference

When using Google Fonts, you can use these weights:

- `font-light` = 300
- `font-normal` = 400 (default)
- `font-medium` = 500
- `font-semibold` = 600
- `font-bold` = 700

**Example:**
```html
<p class="font-medium">This text uses weight 500</p>
```

## Tips for Finance Apps

✅ **DO:**
- Use monospace fonts (like JetBrains Mono) for numbers/amounts
- Keep font weights consistent (use 2-3 weights max)
- Test readability with real data

❌ **DON'T:**
- Use more than 2-3 different fonts (looks messy)
- Use decorative/script fonts for numbers (hard to read)
- Mix too many font weights

## Testing Your Changes

1. Save the file
2. Refresh your browser (hard refresh: `Cmd+Shift+R`)
3. Check that text looks different

If fonts don't load:
- Check browser console for errors (F12 → Console)
- Make sure you have internet connection (for Google Fonts)
- Clear browser cache

## Examples in Your App

You can update any template to use the new fonts:

### Dashboard numbers:
```html
<div class="text-2xl font-bold amount">
    {{ primary_currency|currency_symbol }}{{ total_balance|round(2) }}
</div>
```

### Transaction amounts:
```html
<td class="font-mono text-green-400">
    +{{ transaction.amount }}
</td>
```

### Category labels:
```html
<span class="font-medium">{{ category.name }}</span>
```

---

**Need help?** Just ask me to:
- Change to a different font
- Add more font weights
- Use local font files
- Update specific pages to use the fonts
