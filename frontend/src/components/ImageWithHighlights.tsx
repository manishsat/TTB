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
      // Handle Government Warning (Detailed) separately with large box
      if (check.field_name === 'Government Warning (Detailed)') {
        // Collect all warning-related words
        const warningWords = ['government', 'warning:', 'warning', '(1)', '(2)', 
                              'according', 'surgeon', 'general', 'general,',
                              'women', 'pregnancy', 'defects', 'defects.',
                              'consumption', 'drive', 'machinery', 'health', 'problems'];
        
        let allBoxes: Array<{left: number, top: number, width: number, height: number}> = [];
        
        warningWords.forEach((word) => {
          const boxes = verificationResult.word_boxes?.[word.toLowerCase()];
          if (boxes) {
            const boxArray = Array.isArray(boxes) ? boxes : [boxes];
            allBoxes.push(...boxArray);
          }
        });
        
        if (allBoxes.length > 0) {
          // Calculate bounding box for all warning text
          const minLeft = Math.min(...allBoxes.map(b => b.left));
          const minTop = Math.min(...allBoxes.map(b => b.top));
          const maxRight = Math.max(...allBoxes.map(b => b.left + b.width));
          const maxBottom = Math.max(...allBoxes.map(b => b.top + b.height));
          
          if (check.matched) {
            // Green box for compliant warning
            ctx.strokeStyle = '#10b981';
            ctx.lineWidth = 4;
            ctx.strokeRect(minLeft - 5, minTop - 5, maxRight - minLeft + 10, maxBottom - minTop + 10);
            ctx.fillStyle = 'rgba(16, 185, 129, 0.1)';
            ctx.fillRect(minLeft - 5, minTop - 5, maxRight - minLeft + 10, maxBottom - minTop + 10);
          } else if (check.violations) {
            // Check if we should highlight entire warning or specific words
            let highlightEntireWarning = false;
            let wordsToHighlight: string[] = [];
            
            check.violations.forEach((violation: string) => {
              if (violation.includes('Surgeon General')) {
                wordsToHighlight.push('surgeon', 'general,');
              } else if (violation.includes('GOVERNMENT WARNING') || violation.includes('all capital')) {
                wordsToHighlight.push('government', 'warning');
              } else if (violation.includes('missing') ||
                         violation.includes('Missing required phrase') ||
                         violation.includes('differs from required regulatory text')) {
                highlightEntireWarning = true;
              }
            });
            
            if (highlightEntireWarning || wordsToHighlight.length === 0) {
              // One big red box for entire warning
              ctx.strokeStyle = '#ef4444';
              ctx.lineWidth = 4;
              ctx.strokeRect(minLeft - 5, minTop - 5, maxRight - minLeft + 10, maxBottom - minTop + 10);
              ctx.fillStyle = 'rgba(239, 68, 68, 0.1)';
              ctx.fillRect(minLeft - 5, minTop - 5, maxRight - minLeft + 10, maxBottom - minTop + 10);
            } else {
              // Individual red boxes for specific words
              wordsToHighlight.forEach((word) => {
                const boxes = verificationResult.word_boxes?.[word.toLowerCase()];
                if (boxes) {
                  const boxArray = Array.isArray(boxes) ? boxes : [boxes];
                  boxArray.forEach((box) => {
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
        }
        return;
      }

      // For matched fields, highlight the expected value
      if (check.matched) {
        let searchWords: string[];
        if (check.field_name === 'Alcohol Content') {
          // Highlight percentage - try with and without decimal
          const percentage = check.found_value?.trim() || '';
          const percentageNoDecimal = percentage.replace('.0%', '%');
          searchWords = [percentage, percentageNoDecimal];
        } else {
          searchWords = check.expected_value.toLowerCase().split(/\s+/);
        }
        
        searchWords.forEach((word) => {
          const boxes = verificationResult.word_boxes?.[word.toLowerCase()];
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
        // For failed fields, highlight what was found
        if (check.found_value && check.found_value !== 'Not found' && check.found_value !== 'Not found or mismatch') {
          let foundWords: string[];
          
          if (check.field_name === 'Alcohol Content') {
            const percentage = check.found_value.trim();
            const percentageNoDecimal = percentage.replace('.0%', '%');
            foundWords = [percentage, percentageNoDecimal];
          } else {
            foundWords = check.found_value.toLowerCase().split(/\s+/);
          }
          
          foundWords.forEach((word) => {
            const cleanWord = check.field_name === 'Alcohol Content' ? word : word.replace(/[%.,ml]/gi, '').trim();
            const boxes = verificationResult.word_boxes?.[cleanWord.toLowerCase()] || verificationResult.word_boxes?.[word.toLowerCase()];
            
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
      // Skip government warning (already handled) and government warning detailed
      if (check.field_name === 'Government Warning' || check.field_name === 'Government Warning (Detailed)') return;
      
      let firstWord = '';
      let labelY = 0;
      let labelX = 0;
      let labelText = '';
      
      // Special handling for Alcohol Content to show percentage
      if (check.field_name === 'Alcohol Content') {
        if (check.found_value) {
          const percentage = check.found_value.trim();
          const percentageNoDecimal = percentage.replace('.0%', '%');
          
          let boxes = verificationResult.word_boxes?.[percentage.toLowerCase()];
          if (!boxes) {
            boxes = verificationResult.word_boxes?.[percentageNoDecimal.toLowerCase()];
          }
          
          if (boxes) {
            const box = Array.isArray(boxes) ? boxes[0] : boxes;
            labelY = box.top - 5;
            labelX = box.left;
            labelText = check.matched ? 'Alcohol Content (%)' : `Alcohol Content (%) (Found: ${check.found_value})`;
            
            // Set color based on match status
            ctx.fillStyle = check.matched ? '#10b981' : '#ef4444';
            
            // Draw text with white outline for readability
            ctx.strokeText(labelText, labelX, labelY);
            ctx.fillText(labelText, labelX, labelY);
          }
        }
        return;
      }
      
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
        labelY = box.top - 5;
        labelX = box.left;
        labelText = check.matched ? check.field_name : `${check.field_name} (Found: ${check.found_value})`;
        
        // Set color based on match status
        ctx.fillStyle = check.matched ? '#10b981' : '#ef4444';
        
        // Draw text with white outline for readability
        ctx.strokeText(labelText, labelX, labelY);
        ctx.fillText(labelText, labelX, labelY);
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
