'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { FileText, Download, RefreshCw, CheckCircle, AlertCircle, ArrowLeft } from 'lucide-react';
import { apiClient, Application, CoverLetter } from '@/lib/api';
import { PreviewDiff } from './preview-diff';

interface ResultsPageProps {
  applicationId: string;
  onBack: () => void;
}

export function ResultsPage({ applicationId, onBack }: ResultsPageProps) {
  const [application, setApplication] = useState<Application | null>(null);
  const [coverLetter, setCoverLetter] = useState<CoverLetter | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    loadApplication();
    
    // Set up polling for status updates
    const interval = setInterval(() => {
      if (application?.status === 'processing') {
        loadApplication();
      }
    }, 2000);
    
    setPollingInterval(interval);

    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [applicationId]);

  const loadApplication = async () => {
    try {
      const app = await apiClient.getApplication(applicationId);
      setApplication(app);
      
      if (app.status === 'completed') {
        try {
          const cover = await apiClient.getCoverLetter(applicationId);
          setCoverLetter(cover);
        } catch (err) {
          console.warn('Failed to load cover letter:', err);
        }
        setIsLoading(false);
      } else if (app.status === 'failed') {
        setError('Application processing failed. Please try again.');
        setIsLoading(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load application');
      setIsLoading(false);
    }
  };

  const handleDownloadResume = () => {
    if (application?.tailored_resume_url) {
      window.open(application.tailored_resume_url, '_blank');
    }
  };

  const handleDownloadCoverLetter = () => {
    if (coverLetter?.docx_url) {
      window.open(coverLetter.docx_url, '_blank');
    }
  };

  const handleSaveResume = async (content: string) => {
    // This would typically call an API to save the edited content
    console.log('Saving resume content:', content);
    // For now, just simulate success
    return Promise.resolve();
  };

  const handleSaveCoverLetter = async (content: string) => {
    // This would typically call an API to save the edited content
    console.log('Saving cover letter content:', content);
    // For now, just simulate success
    return Promise.resolve();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto text-center">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-center gap-2">
                  <RefreshCw className="h-5 w-5 animate-spin" />
                  Processing Your Application
                </CardTitle>
                <CardDescription>
                  We're tailoring your resume and generating your cover letter...
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Progress value={application?.status === 'processing' ? 50 : 0} />
                <p className="text-sm text-gray-600">
                  This may take a few minutes. Please don't close this page.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto">
            <Button variant="outline" onClick={onBack} className="mb-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <Button variant="outline" onClick={onBack} className="mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Start
        </Button>

        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Your Application is Ready!
          </h1>
          <p className="text-lg text-gray-600">
            Review, edit, and download your tailored resume and cover letter.
          </p>
        </div>

        <div className="max-w-6xl mx-auto space-y-6">
          {/* Resume Preview */}
          {application?.tailored_resume_url && (
            <PreviewDiff
              title="Tailored Resume"
              originalContent="Your original resume content would appear here..."
              generatedContent="Your tailored resume content would appear here with AI-generated improvements..."
              onSave={handleSaveResume}
              onDownload={handleDownloadResume}
              fileType="resume"
            />
          )}

          {/* Cover Letter Preview */}
          {coverLetter && (
            <PreviewDiff
              title="Cover Letter"
              originalContent=""
              generatedContent={coverLetter.content}
              onSave={handleSaveCoverLetter}
              onDownload={handleDownloadCoverLetter}
              fileType="cover-letter"
            />
          )}

          {/* Download All */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Download className="h-5 w-5" />
                Download All Files
              </CardTitle>
              <CardDescription>
                Download both your tailored resume and cover letter
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-4">
                <Button 
                  onClick={handleDownloadResume}
                  disabled={!application?.tailored_resume_url}
                  className="flex-1"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Download Resume
                </Button>
                <Button 
                  onClick={handleDownloadCoverLetter}
                  disabled={!coverLetter?.docx_url}
                  className="flex-1"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Download Cover Letter
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Success Message */}
          <Alert>
            <CheckCircle className="h-4 w-4" />
            <AlertDescription>
              Your application materials have been successfully generated! You can now review, edit, and download your tailored resume and cover letter.
            </AlertDescription>
          </Alert>
        </div>
      </div>
    </div>
  );
}
