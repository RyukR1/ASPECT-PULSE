# Aspect-Pulse Website - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Flask
```bash
pip install flask
```

### 2. Navigate to Web Directory
```bash
cd /home/ryukr2/Projects/SenAnalysis/Aspect-Pulse/web
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open in Browser
```
http://localhost:5000
```

## 📁 What's Been Created

Your new professional website includes:

### ✅ **Pages**
- **Home** - Hero section with feature highlights and real-time analyzer
- **Dashboard** - Analytics overview with charts and metrics
- **About** - Detailed information about the technology
- **Error Pages** - 404 and 500 error handling

### ✅ **Features**
- Real-time text analysis
- Interactive charts (sentiment distribution, aspect breakdown)
- Responsive design (mobile, tablet, desktop)
- Modern UI with gradients and animations
- Character counter
- Live results display
- Beautiful data visualizations

### ✅ **Technology Stack**
- **Backend:** Flask (Python web framework)
- **Frontend:** HTML5, CSS3, JavaScript
- **Charts:** Chart.js
- **Icons:** Font Awesome
- **Fonts:** Google Fonts (Poppins)

## 🎨 Design Highlights

- **Color Scheme:** Indigo and Pink gradients
- **Responsive:** Works on all devices
- **Modern:** Smooth animations and transitions
- **Professional:** Clean, organized layout
- **Fast:** Optimized performance

## 📊 Pages Overview

### Home Page (`/`)
- Hero section with call-to-action
- Feature cards highlighting ABSA benefits
- Real-time text analyzer
- Results visualization with charts
- Detailed results table
- Statistics section
- Footer with links

### Dashboard (`/dashboard`)
- Key performance metrics
- Overall sentiment distribution chart
- Top discussed aspects
- Sentiment by aspect stacked bar chart
- Recent analyses list

### About Page (`/about`)
- Project overview
- Technology stack explanation
- Supported product aspects
- Data sources information
- How it works (4-step process)
- Use cases
- Accuracy metrics

## 🔧 Configuration

All settings are in `app.py`:
- `DEBUG = True` - Development mode
- `MAX_CONTENT_LENGTH = 16MB` - Max file size
- Port: `5000` - Change with `port=XXXX`

## 📝 Text Analyzer Usage

1. Paste review text (max 5000 characters)
2. Click "Analyze" button
3. View results:
   - Summary cards (sentiment percentages)
   - Charts (visual distribution)
   - Table (detailed results per sentence)

## 🌐 Access Points

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Main analyzer interface |
| Dashboard | `/dashboard` | Analytics & metrics |
| About | `/about` | Project information |
| API | `/analyze` | Text analysis endpoint |
| API | `/api/aspects` | Get supported aspects |

## ⚡ Performance Tips

- ML models are cached for faster processing
- CSS is optimized and minified
- JavaScript is lightweight and efficient
- Charts render efficiently with Chart.js

## 🎯 Next Steps

1. ✅ Run the server
2. ✅ Test the analyzer on the home page
3. ✅ Check the dashboard
4. ✅ Explore the about page
5. ✅ Review the code structure

## 📂 File Structure

```
web/
├── app.py                           # Flask app (270+ lines)
├── README.md                        # Full documentation
├── QUICKSTART.md                   # This file
├── templates/
│   ├── index.html                  # Home (250+ lines)
│   ├── dashboard.html              # Dashboard (120+ lines)
│   ├── about.html                  # About page (200+ lines)
│   ├── 404.html                    # Not found
│   └── 500.html                    # Server error
└── static/
    ├── css/
    │   └── style.css               # Styles (1000+ lines)
    └── js/
        ├── main.js                 # Home JS (200+ lines)
        └── dashboard.js            # Dashboard JS (180+ lines)
```

## 🐛 Troubleshooting

**Port 5000 already in use?**
```bash
python app.py --port 8000
# Or modify in app.py: app.run(port=8000)
```

**ModuleNotFoundError: No module named 'flask'?**
```bash
pip install flask
```

**Import errors for NLP modules?**
```bash
pip install -r requirements.txt
```

**Sentiment model not loading?**
- Ensure NLP modules are properly set up
- Check that transformers library is installed
- Verify model files exist in sentiment/ directory

## 💡 Tips

- The homepage analyzer saves results to browser localStorage
- Results automatically load on the dashboard
- Character counter prevents oversized submissions
- All charts are responsive and interactive
- Mobile-friendly design adapts to screen size

## 🎉 You're All Set!

Your professional Aspect-Pulse website is ready to go. Start the server, open a browser, and begin analyzing!

Need help? Check the full README.md in the web directory for detailed documentation.
