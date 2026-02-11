# Aspect-Pulse Web Application

A modern, professional web interface for the Aspect-Pulse Aspect-Based Sentiment Analysis system.

## Features

✨ **Modern Web Interface**
- Responsive design that works on desktop, tablet, and mobile
- Beautiful gradient UI with smooth animations
- Dark mode ready

🔍 **Real-Time Analysis**
- Instant sentiment analysis
- Aspect extraction and classification
- Beautiful data visualizations with Chart.js

📊 **Interactive Dashboard**
- Analytics overview
- Sentiment distribution charts
- Aspect performance metrics
- Recent analysis history

📱 **User-Friendly**
- Intuitive text input interface
- Live character counter
- Clear error messages
- Loading states

## Project Structure

```
web/
├── app.py                 # Flask application
├── templates/             # HTML templates
│   ├── index.html        # Home page with analyzer
│   ├── dashboard.html    # Analytics dashboard
│   ├── about.html        # About page
│   ├── 404.html          # Not found page
│   └── 500.html          # Server error page
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet (1000+ lines)
│   └── js/
│       ├── main.js       # Home page functionality
│       └── dashboard.js  # Dashboard functionality
└── README.md             # This file
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- Flask
- Chart.js (loaded via CDN)
- Font Awesome (loaded via CDN)

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Navigate to the web directory:**
```bash
cd web
```

3. **Run the Flask application:**
```bash
python app.py
```

4. **Open your browser:**
Navigate to `http://localhost:5000`

## Usage

### Home Page
1. Paste or type your review/comment text
2. Click the "Analyze" button
3. View detailed sentiment analysis results
4. Charts show sentiment distribution
5. Table displays sentence-by-sentence analysis

### Dashboard
- View overall analytics metrics
- Track sentiment trends
- See which aspects are most discussed
- Monitor recent analyses

### About Page
- Learn about ABSA technology
- Explore supported features
- Understand the system architecture
- View use cases and accuracy metrics

## Features in Detail

### Text Analysis
- **Character Counter:** Real-time character count (max 5000)
- **Sentiment Analysis:** Classify text as positive, negative, or neutral
- **Aspect Extraction:** Identify mentions of product aspects
- **Confidence Scores:** View model confidence for each prediction

### Visualizations
- **Sentiment Distribution:** Doughnut chart showing overall sentiment
- **Aspect Performance:** Stacked bar chart by aspect and sentiment
- **Real-time Charts:** Charts update instantly with analysis results

### Supported Aspects
- 🔋 Battery (life, charging, durability)
- 📷 Camera (quality, zoom, low-light)
- 📱 Display (quality, brightness, refresh rate)
- ⚡ Performance (speed, responsiveness)
- 💰 Value (price, worth, deal quality)

## API Endpoints

### POST `/analyze`
Analyzes text and returns sentiment and aspect classification.

**Request:**
```json
{
  "text": "Your review text here..."
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "sentence": "The battery is great.",
      "aspect": "Battery",
      "polarity": {
        "label": "POSITIVE",
        "score": 0.95
      },
      "score": 0.95
    }
  ],
  "summary": {
    "by_aspect": { ... },
    "overall_sentiment": { ... },
    "total_sentences": 1
  },
  "timestamp": "2026-02-11T10:30:00"
}
```

### GET `/api/aspects`
Returns the list of supported aspects.

**Response:**
```json
{
  "aspects": ["Battery", "Camera", "Display", "Performance", "Value"],
  "description": "List of product aspects that can be analyzed"
}
```

## Styling & Design

The website uses:
- **Color Palette:** Indigo (#6366f1) and Pink (#ec4899) primary colors
- **Typography:** Poppins font family
- **Layout:** CSS Grid and Flexbox
- **Responsive:** Mobile-first design with breakpoints at 1024px and 768px
- **Animations:** Smooth transitions and hover effects

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- **Client-side:** Minimal dependencies, fast load time
- **Server-side:** Flask with caching for ML models
- **Charts:** Efficient Chart.js implementation
- **CSS:** Optimized for performance

## Customization

### Colors
Edit the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    /* ... */
}
```

### Fonts
Currently using Google Fonts 'Poppins'. Change in template `<head>` tags.

### Charts
Chart configurations are in `static/js/main.js` and `static/js/dashboard.js`.

## Troubleshooting

### "Failed to load sentiment model"
- Ensure sentiment model files are present in `sentiment/`
- Check that transformers library is installed

### Charts not displaying
- Verify Chart.js CDN is accessible
- Check browser console for errors

### Slow performance
- Large text inputs may take longer to process
- Consider implementing text chunking for very long inputs

## Future Enhancements

- [ ] User authentication and accounts
- [ ] Result history/export
- [ ] Batch analysis upload
- [ ] Real-time streaming analysis
- [ ] Custom aspect configuration
- [ ] Multi-language support
- [ ] Advanced analytics and trends
- [ ] API key management

## License

Part of the Aspect-Pulse project. See main README.md for licensing information.

## Support

For issues or questions about the web interface, please refer to the main Aspect-Pulse repository documentation.
