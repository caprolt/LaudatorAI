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

  const emblemSizes = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const taglineSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
    xl: 'text-lg'
  };

  return (
    <div className={`flex flex-col items-center ${className}`}>
      {/* Ornate Circular Emblem */}
      <div className={`relative ${emblemSizes[size]} mb-2`}>
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-yellow-400 via-yellow-300 to-yellow-500 p-0.5">
          <div className="w-full h-full rounded-full bg-gradient-to-br from-yellow-500 via-yellow-400 to-yellow-600 flex items-center justify-center">
            {/* Ornate pattern - simplified version */}
            <div className="w-3/4 h-3/4 rounded-full border-2 border-yellow-300 flex items-center justify-center">
              <div className="w-1/2 h-1/2 rounded-full border border-yellow-300 flex items-center justify-center">
                <span className="text-yellow-800 font-bold text-xs">L</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Logo Text */}
      <h1 className={`font-serif font-bold gradient-text ${sizeClasses[size]} tracking-wide`}>
        LaudatorAI
      </h1>

      {/* Tagline */}
      {showTagline && (
        <p className={`font-sans font-medium text-yellow-600 tracking-widest uppercase ${taglineSizes[size]} mt-1`}>
          Your AI Advocate in the Job Market
        </p>
      )}
    </div>
  );
};
