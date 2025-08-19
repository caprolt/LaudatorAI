import React from 'react';

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

  return (
    <div className={`flex flex-col items-center ${className}`}>
      {/* Logo Image */}
      <div className={`${imageSizes[size]} mb-4`}>
        <img 
          src="/laudatorai-high-resolution-logo.png" 
          alt="LaudatorAI Logo" 
          className="w-full h-full object-contain"
        />
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
