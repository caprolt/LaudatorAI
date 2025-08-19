import log from 'loglevel';

// Only import and configure remote logging on the client side
let remote: any = null;
if (typeof window !== 'undefined') {
  import('loglevel-plugin-remote').then((module) => {
    remote = module.default;
    
    // Configure loglevel
    log.setLevel(process.env.NODE_ENV === 'production' ? log.levels.INFO : log.levels.DEBUG);

    // Configure remote logging for production
    if (process.env.NODE_ENV === 'production' && remote) {
      remote.apply(log, {
        url: '/api/logs', // We'll create this endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        format: (level: string, name: string, timestamp: string, message: string) => ({
          level,
          name,
          timestamp,
          message,
          url: typeof window !== 'undefined' ? window.location.href : '',
          userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : '',
          sessionId: getSessionId(),
        }),
      });
    }
  });
} else {
  // Server-side configuration
  log.setLevel(process.env.NODE_ENV === 'production' ? log.levels.INFO : log.levels.DEBUG);
}

// Session ID for tracking user sessions
let sessionId: string | null = null;

function getSessionId(): string {
  if (sessionId) return sessionId;
  
  // Try to get from localStorage
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('laudatorai_session_id');
    if (stored) {
      sessionId = stored;
      return sessionId;
    }
  }
  
  // Generate new session ID
  sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  // Store in localStorage
  if (typeof window !== 'undefined') {
    localStorage.setItem('laudatorai_session_id', sessionId);
  }
  
  return sessionId;
}

// Enhanced logger with structured logging
class Logger {
  private logger: log.Logger;
  private context: Record<string, any>;

  constructor(name: string, context: Record<string, any> = {}) {
    this.logger = log.getLogger(name);
    this.context = context;
  }

  private formatMessage(level: string, message: string, data?: any): string {
    const timestamp = new Date().toISOString();
    const baseInfo = {
      timestamp,
      level,
      logger: (this.logger as any).name || 'unknown',
      sessionId: getSessionId(),
      url: typeof window !== 'undefined' ? window.location.href : '',
      ...this.context,
    };

    if (data) {
      return JSON.stringify({
        ...baseInfo,
        message,
        data,
      });
    }

    return JSON.stringify({
      ...baseInfo,
      message,
    });
  }

  info(message: string, data?: any): void {
    const formattedMessage = this.formatMessage('INFO', message, data);
    this.logger.info(formattedMessage);
  }

  warn(message: string, data?: any): void {
    const formattedMessage = this.formatMessage('WARN', message, data);
    this.logger.warn(formattedMessage);
  }

  error(message: string, error?: Error | any, data?: any): void {
    const errorData = error instanceof Error ? {
      name: error.name,
      message: error.message,
      stack: error.stack,
    } : error;

    const formattedMessage = this.formatMessage('ERROR', message, {
      ...data,
      error: errorData,
    });
    this.logger.error(formattedMessage);
  }

  debug(message: string, data?: any): void {
    const formattedMessage = this.formatMessage('DEBUG', message, data);
    this.logger.debug(formattedMessage);
  }

  // Specialized logging methods
  logUserAction(action: string, resource: string, success: boolean, data?: any): void {
    this.info('User Action', {
      action,
      resource,
      success,
      ...data,
    });
  }

  logApiCall(method: string, endpoint: string, status: number, duration: number, data?: any): void {
    this.info('API Call', {
      method,
      endpoint,
      status,
      duration,
      ...data,
    });
  }

  logPageView(page: string, data?: any): void {
    this.info('Page View', {
      page,
      ...data,
    });
  }

  logError(error: Error, context?: string, data?: any): void {
    this.error('Application Error', error, {
      context,
      ...data,
    });
  }

  logPerformance(metric: string, value: number, unit: string, data?: any): void {
    this.info('Performance Metric', {
      metric,
      value,
      unit,
      ...data,
    });
  }

  logPerformanceMeasurement(name: string, duration: number, data?: any): void {
    this.logPerformance(name, duration, 'ms', data);
  }

  logSecurityEvent(event: string, severity: 'low' | 'medium' | 'high' | 'critical', data?: any): void {
    this.warn('Security Event', {
      event,
      severity,
      ...data,
    });
  }

  // Add context to logger
  withContext(context: Record<string, any>): Logger {
    return new Logger((this.logger as any).name || 'unknown', { ...this.context, ...context });
  }
}

// Create default logger
export const logger = new Logger('LaudatorAI');

// Create specialized loggers
export const apiLogger = new Logger('LaudatorAI.API');
export const uiLogger = new Logger('LaudatorAI.UI');
export const authLogger = new Logger('LaudatorAI.Auth');
export const performanceLogger = new Logger('LaudatorAI.Performance');

// Utility functions for common logging patterns
export const logUtils = {
  // Log component lifecycle
  logComponentMount: (componentName: string, props?: any) => {
    uiLogger.info('Component Mounted', { componentName, props });
  },

  logComponentUnmount: (componentName: string) => {
    uiLogger.info('Component Unmounted', { componentName });
  },

  // Log form interactions
  logFormSubmit: (formName: string, success: boolean, data?: any) => {
    uiLogger.info('Form Submitted', { formName, success, data });
  },

  logFormValidation: (formName: string, errors: any) => {
    uiLogger.warn('Form Validation Failed', { formName, errors });
  },

  // Log file operations
  logFileUpload: (fileName: string, fileSize: number, success: boolean, data?: any) => {
    uiLogger.info('File Upload', { fileName, fileSize, success, data });
  },

  logFileDownload: (fileName: string, success: boolean, data?: any) => {
    uiLogger.info('File Download', { fileName, success, data });
  },

  // Log navigation
  logNavigation: (from: string, to: string, method: 'link' | 'button' | 'back' | 'forward') => {
    uiLogger.info('Navigation', { from, to, method });
  },

  // Log errors with context
  logErrorWithContext: (error: Error, context: string, additionalData?: any) => {
    logger.error('Error with Context', error, { context, ...additionalData });
  },

  // Log performance measurements
  logPerformanceMeasurement: (name: string, duration: number, data?: any) => {
    performanceLogger.logPerformance(name, duration, 'ms', data);
  },

  // Log user interactions
  logUserInteraction: (element: string, action: string, data?: any) => {
    uiLogger.info('User Interaction', { element, action, data });
  },
};

// Error boundary logging
export const logErrorBoundary = (error: Error, errorInfo: any) => {
  logger.error('React Error Boundary Caught Error', error, {
    componentStack: errorInfo.componentStack,
  });
};

// Performance monitoring
export const measurePerformance = (name: string, fn: () => any) => {
  const start = performance.now();
  try {
    const result = fn();
    const duration = performance.now() - start;
    performanceLogger.logPerformanceMeasurement(name, duration);
    return result;
  } catch (error) {
    const duration = performance.now() - start;
    performanceLogger.logPerformanceMeasurement(name, duration, { error: true });
    throw error;
  }
};

export const measureAsyncPerformance = async (name: string, fn: () => Promise<any>) => {
  const start = performance.now();
  try {
    const result = await fn();
    const duration = performance.now() - start;
    performanceLogger.logPerformanceMeasurement(name, duration);
    return result;
  } catch (error) {
    const duration = performance.now() - start;
    performanceLogger.logPerformanceMeasurement(name, duration, { error: true });
    throw error;
  }
};

// Export default logger for backward compatibility
export default logger;
