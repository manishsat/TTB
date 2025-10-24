# TTB Label Verification Application

AI-powered web application that simulates the Alcohol and Tobacco Tax and Trade Bureau (TTB) label approval process. The application verifies alcohol beverage labels against submitted form data using OCR (Optical Character Recognition) technology.

## 🎯 Project Overview

This full-stack application allows users to:
- Submit product information through a web form (brand name, product class, alcohol content, net contents)
- Upload an alcohol label image
- Get AI-powered verification results comparing the label image with form data
- View detailed field-by-field verification results

## 🏗️ Tech Stack

### Backend
- **Python 3.x** - Core programming language
- **FastAPI** - Modern, fast web framework for building APIs
- **Tesseract OCR** - Optical character recognition engine
- **pytesseract** - Python wrapper for Tesseract
- **Pillow (PIL)** - Image processing library
- **python-Levenshtein** - Fuzzy string matching for OCR error tolerance

### Frontend
- **React 18+** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API requests

## 📋 Prerequisites

- Python 3.9+ installed
- Node.js 18+ and npm installed
- Tesseract OCR engine installed on your system

### Installing Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd TTB
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Start the backend server
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`
API documentation (Swagger UI): `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend application will be available at `http://localhost:5173`

## 📁 Project Structure

```
TTB/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models.py            # Pydantic models for request/response
│   │   ├── ocr.py               # OCR text extraction logic
│   │   └── verification.py      # Label verification logic
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LabelVerificationForm.tsx
│   │   │   └── VerificationResults.tsx
│   │   ├── services/
│   │   │   └── api.ts           # API client functions
│   │   ├── types/
│   │   │   └── index.ts         # TypeScript type definitions
│   │   ├── App.tsx              # Main React component
│   │   └── main.tsx             # Application entry point
│   ├── package.json
│   └── vite.config.ts
├── Requirements/                # Project requirements PDF
└── README.md
```

## 🔧 Configuration

### Matching Assumptions & Rules (Per PDF Requirements)

#### 1. Brand Name Matching
- **Method**: Fuzzy matching using Levenshtein distance
- **Threshold**: 0.75 similarity (75% match required)
- **Case**: Insensitive (ignores capitalization)
- **Whitespace**: Normalized (extra spaces removed)
- **Tolerance**: Allows minor OCR errors
- **Example**: "Eagle Peak" matches "Eagie Peak" (OCR typo tolerated)
- **Rationale**: OCR can misread individual characters; fuzzy matching prevents false negatives

#### 2. Product Class/Type Matching
- **Method**: Fuzzy matching with 0.75 similarity threshold
- **Case**: Insensitive
- **Tolerance**: Allows "very close/identical" matches per PDF requirement
- **Example**: "Bourbon Whiskey" matches "bourbon  whiskey" or "Bourbon Whisky"
- **Rationale**: Formatting variations and minor OCR errors shouldn't fail verification

#### 3. Alcohol Content Matching
- **Method**: Regex pattern extraction + numeric comparison
- **Formats Recognized**:
  - "45%", "45 %", "45% ABV", "45% Alc./Vol."
  - "alc. 45", "alcohol 45", "45 percent"
- **Tolerance**: ±0.5% for OCR reading errors
- **Must Match**: The number AND "%" symbol in extracted text
- **Example**: Label "45% Alc./Vol." matches form "45" → PASS
- **Example**: Label "45.3%" matches form "45" → PASS (within tolerance)
- **Example**: Label "40%" matches form "45" → FAIL (outside tolerance)
- **Rationale**: OCR may misread decimals; small tolerance accounts for this

#### 4. Net Contents Matching
- **Method**: Regex pattern extraction + exact number comparison
- **Formats Recognized**: "mL", "L", "oz", "fl oz", "fl. oz"
- **Tolerance**: None (exact number match required)
- **Volume Appears**: Yes, must contain the number on the label
- **Example**: Label "750 mL" matches form "750" → PASS
- **Example**: Label "355 mL" matches form "750" → FAIL
- **Prevention**: "1750" won't match "750" (no substring matching)
- **Rationale**: Volume is a precise regulatory requirement; no tolerance needed

#### 5. Government Warning Statement (Bonus Feature)
- **Requirement**: Mandatory by law for alcoholic beverages
- **Method**: Keyword detection with fuzzy matching
- **Threshold**: 0.85 similarity (stricter than brand/type)
- **Keywords Checked**:
  - "GOVERNMENT WARNING" (primary indicator)
  - "Surgeon General"
  - "pregnant" / "pregnancy"
  - "birth defects"
  - "operating machinery" / "drive a car"
- **Current Status**: Shows warning if missing but doesn't fail overall verification
- **Production Behavior**: Would fail verification if missing/incomplete
- **Rationale**: Real TTB requires exact warning text; this simplified check ensures presence

#### 6. Text Normalization Strategy
- **Case Normalization**: All text converted to lowercase before comparison
- **Whitespace Handling**: `\s+` regex collapses multiple spaces to single space
- **Leading/Trailing Spaces**: Removed via `.strip()`
- **OCR Error Handling**: Fuzzy matching (Levenshtein distance) handles common OCR mistakes:
  - "l" (lowercase L) vs "I" (capital i)
  - "O" (letter) vs "0" (zero)
  - Missing/extra characters
- **Strictness**: 
  - Brand/Type: 75% match (more forgiving)
  - Warning: 85% match (stricter)
  - Alcohol/Volume: Exact numbers with defined tolerance

### OCR Configuration

### Backend Configuration

The backend uses environment variables for configuration. Create a `.env` file in the `backend/` directory if needed:

```env
# Optional configurations
HOST=0.0.0.0
PORT=8000
```

### Frontend Configuration

Create `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

For production deployment, update `.env.production`:

```env
VITE_API_URL=https://your-backend-url.com
```

## 🧪 How It Works

### Verification Process

1. **Form Submission**: User enters product details and uploads label image
2. **OCR Processing**: Backend uses Tesseract to extract text from the image
3. **Text Matching**: Extracted text is compared against form inputs using:
   - Fuzzy matching (Levenshtein distance) for text fields
   - Exact numerical matching (with tolerance) for alcohol content
   - Pattern matching for percentages and volumes
4. **Results Display**: Frontend shows detailed results with:
   - Overall pass/fail status
   - Field-by-field verification
   - Extracted text preview
   - Specific mismatch details

### Key Features

- **Fuzzy Matching**: Tolerates minor OCR errors and formatting differences
- **Government Warning Detection**: Checks for required warning text
- **Image Preview**: Shows uploaded label before submission
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Graceful handling of invalid images or processing errors

## 📝 API Endpoints

### POST /api/verify

Verify an alcohol label against form data.

**Request:**
- `brand_name` (string, required): Brand name from form
- `product_class` (string, required): Product class/type
- `alcohol_content` (float, required): Alcohol by volume percentage
- `net_contents` (string, optional): Net contents/volume
- `label_image` (file, required): Label image file

**Response:**
```json
{
  "success": true,
  "overall_match": true,
  "message": "✅ The label matches the form data...",
  "extracted_text": "OLD TOM DISTILLERY\\nKentucky Straight Bourbon Whiskey...",
  "checks": [
    {
      "field_name": "Brand Name",
      "expected_value": "Old Tom Distillery",
      "found_value": "Old Tom Distillery",
      "matched": true,
      "message": "✓ Brand name 'Old Tom Distillery' found on label"
    }
  ]
}
```

### GET /

Health check endpoint.

## 🎨 Design Decisions

### Text Matching Strategy
- **Case-insensitive**: Ignores capitalization differences
- **Whitespace normalization**: Handles spacing variations
- **Fuzzy threshold**: 75-80% similarity for text fields
- **ABV tolerance**: ±0.5% for alcohol content

### OCR Configuration
- Uses Tesseract's default English language model
- PSM mode 6 (Assumes uniform block of text)
- OEM mode 3 (Default, based on available data)

## 🚧 Known Limitations

1. **OCR Accuracy**: Results depend on image quality and text clarity
2. **Language Support**: Currently optimized for English text
3. **Complex Layouts**: May struggle with highly decorative or non-standard label designs
4. **Government Warning**: Basic keyword detection (not full text comparison)

## 🔮 Future Enhancements

- [ ] Support for multiple product types (beer, wine, spirits) with specific rules
- [ ] Image preprocessing for better OCR accuracy
- [ ] Bounding box highlighting on label image
- [ ] Database storage for verification history
- [ ] User authentication and session management
- [ ] Batch processing for multiple labels
- [ ] Export verification reports as PDF
- [ ] Enhanced government warning text validation

## 📦 Deployment

### Backend Deployment (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables as needed
5. Deploy

### Frontend Deployment (Vercel)

1. Install Vercel CLI: `npm i -g vercel`
2. From frontend directory: `vercel`
3. Follow the prompts
4. Update `.env.production` with backend URL
5. Deploy: `vercel --prod`

## 🤝 Contributing

This is a take-home project for educational purposes. Feel free to fork and enhance!

## 📄 License

MIT License - feel free to use this project for learning and development.

## 👨‍💻 Author

Developed as part of a technical assessment demonstrating full-stack development skills with AI/OCR integration.

---

**Note**: This is a simplified simulation for educational purposes. Actual TTB label approval involves more comprehensive review and regulatory compliance checks.
