import { useEffect, useRef, useState } from 'react';
import type { VerificationResponse } from '../types';

interface Props {
  imageUrl: string;
  verificationResult: VerificationResponse | null;
}

const ImageWithHighlights: React.FC<Props> = ({ imageUrl, verificationResult }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const imgRef = useRef<HTMLImageElement>(null);
  const [imageLoaded, setImageLoaded] = useState(false);

  useEffect(() => {
    if (!imageLoaded || !canvasRef.current || !imgRef.current || !verificationResult?.word_boxes) {
      return;
    }

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const img = imgRef.current;

    if (!ctx) return;

    // Set canvas size to match image
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;

    // Draw the image
    ctx.drawImage(img, 0, 0);

    // Draw bounding boxes for all fields
    // For matched fields: highlight what was found on the label (green)
    // For failed fields: try to find what OCR detected instead (if available)
    verificationResult.checks.forEach((check) => {
      // Skip government warning (too many words to highlight)
      if (check.field_name === 'Government Warning') return;

      // For matched fields, highlight the expected value
      if (check.matched) {
        const searchWords = check.expected_value.toLowerCase().split(/\s+/);
        
        searchWords.forEach((word) => {
          const boxes = verificationResult.word_boxes?.[word];
          if (!boxes) return;

          const boxArray = Array.isArray(boxes) ? boxes : [boxes];

          boxArray.forEach((box) => {
            // Green for matched
            ctx.strokeStyle = '#10b981';
            ctx.lineWidth = 3;
            ctx.strokeRect(box.left, box.top, box.width, box.height);
            ctx.fillStyle = 'rgba(16, 185, 129, 0.1)';
            ctx.fillRect(box.left, box.top, box.width, box.height);
          });
        });
      } else {
        // For failed fields, try to highlight what was actually found
        // Extract actual value from found_value if available
        if (check.found_value && check.found_value !== 'Not found' && check.found_value !== 'Not found or mismatch') {
          const foundWords = check.found_value.toLowerCase().split(/\s+/);
          
          foundWords.forEach((word) => {
            // Clean up word (remove %, mL, etc for better matching)
            const cleanWord = word.replace(/[%.,ml]/gi, '').trim();
            
            // Try both cleaned and original word
            const boxes = verificationResult.word_boxes?.[cleanWord] || verificationResult.word_boxes?.[word];
            
            if (boxes) {
              const boxArray = Array.isArray(boxes) ? boxes : [boxes];

              boxArray.forEach((box) => {
                // Red for mismatched
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 3;
                ctx.strokeRect(box.left, box.top, box.width, box.height);
                ctx.fillStyle = 'rgba(239, 68, 68, 0.1)';
                ctx.fillRect(box.left, box.top, box.width, box.height);
              });
            }
          });
        }
      }
    });

    // Draw labels for field names
    ctx.font = '14px sans-serif';
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;

    verificationResult.checks.forEach((check) => {
      // Skip government warning
      if (check.field_name === 'Government Warning') return;
      
      let firstWord = '';
      
      if (check.matched) {
        const searchWords = check.expected_value.toLowerCase().split(/\s+/);
        firstWord = searchWords[0];
      } else if (check.found_value && check.found_value !== 'Not found' && check.found_value !== 'Not found or mismatch') {
        const foundWords = check.found_value.toLowerCase().split(/\s+/);
        firstWord = foundWords[0].replace(/[%.,ml]/gi, '').trim();
      }
      
      if (!firstWord) return;
      
      const boxes = verificationResult.word_boxes?.[firstWord];
      
      if (boxes) {
        const box = Array.isArray(boxes) ? boxes[0] : boxes;
        const labelY = box.top - 5;
        const labelText = check.matched ? check.field_name : `${check.field_name} (Found: ${check.found_value})`;
        
        // Set color based on match status
        ctx.fillStyle = check.matched ? '#10b981' : '#ef4444';
        
        // Draw text with white outline for readability
        ctx.strokeText(labelText, box.left, labelY);
        ctx.fillText(labelText, box.left, labelY);
      }
    });

  }, [imageLoaded, verificationResult]);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  return (
    <div className="relative">
      <img
        ref={imgRef}
        src={imageUrl}
        alt="Label"
        className="hidden"
        onLoad={handleImageLoad}
        crossOrigin="anonymous"
      />
      <canvas
        ref={canvasRef}
        className="max-w-full h-auto border border-gray-300 rounded-md"
      />
      {verificationResult?.word_boxes && (
        <div className="mt-2 text-sm text-gray-600">
          <span className="inline-block w-4 h-4 bg-green-500 opacity-20 mr-1 align-middle"></span>
          <span className="mr-3">Green boxes = matched text</span>
          <span className="inline-block w-4 h-4 bg-red-500 opacity-20 mr-1 align-middle"></span>
          <span>Red boxes = you entered this but it wasn't found on label</span>
        </div>
      )}
    </div>
  );
};

export default ImageWithHighlights;
