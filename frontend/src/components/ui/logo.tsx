import React, { useState } from 'react';
import Image from 'next/image';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showTagline?: boolean;
  className?: string;
}

export const Logo: React.FC<LogoProps> = ({ 
  size = 'md', 
  showTagline = true, 
  className = '' 
}) => {
  const [imageError, setImageError] = useState(false);

  const sizeClasses = {
    sm: 'text-lg',
    md: 'text-2xl',
    lg: 'text-4xl',
    xl: 'text-6xl'
  };

  const imageSizes = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32',
    xl: 'w-48 h-48'
  };

  const taglineSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  };

  const handleImageError = () => {
    setImageError(true);
  };

  return (
    <div className={`flex flex-col items-center ${className}`}>
      {/* Logo Image */}
      <div className={`${imageSizes[size]} mb-4 relative`}>
        {!imageError ? (
          <Image 
            src="/laudatorai-high-resolution-logo.png" 
            alt="LaudatorAI Logo" 
            fill
            className="object-contain"
            onError={handleImageError}
            priority
          />
        ) : (
          // Fallback to text-based logo if image fails to load
          <div className="w-full h-full flex flex-col items-center justify-center">
            <div className="w-3/4 h-3/4 rounded-full bg-gradient-to-br from-yellow-500 via-yellow-400 to-yellow-600 flex items-center justify-center mb-2">
              <span className="text-yellow-800 font-bold text-lg">L</span>
            </div>
            <h1 className={`font-serif font-bold gradient-text ${sizeClasses[size]} tracking-wide`}>
              LaudatorAI
            </h1>
          </div>
        )}
      </div>

      {/* Tagline - only show if not already in the logo image */}
      {showTagline && (
        <p className={`font-sans font-medium text-yellow-600 tracking-widest uppercase ${taglineSizes[size]} mt-1`}>
          Your AI Advocate in the Job Market
        </p>
      )}
    </div>
  );
};
