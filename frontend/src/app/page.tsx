'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { FileText, Send, CheckCircle, AlertCircle, Sparkles } from 'lucide-react';
import { JobDescriptionInput } from '@/components/job-description-input';
import { ResumeUpload } from '@/components/resume-upload';
import { ResultsPage } from '@/components/results-page';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { apiClient, JobDescription, ResumeData, Application } from '@/lib/api';

type AppState = 'input' | 'processing' | 'results';

export default function Home() {
  const [appState, setAppState] = useState<AppState>('input');
  const [jobDescription, setJobDescription] = useState<JobDescription | null>(null);
  const [resume, setResume] = useState<ResumeData | null>(null);
  const [application, setApplication] = useState<Application | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleJobDescriptionExtracted = (jd: JobDescription) => {
    setJobDescription(jd);
    setError(null);
  };

  const handleResumeUploaded = (resumeData: ResumeData) => {
    setResume(resumeData);
    setError(null);
  };

  const handleGenerateApplication = async () => {
    if (!jobDescription || !resume) {
      setError('Please provide both a job description and resume');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const newApplication = await apiClient.createApplication(
        jobDescription.id,
        resume.id
      );
      setApplication(newApplication);
      setAppState('processing');
    } catch (err) {
      console.error('Error creating application:', err);
      setError(err instanceof Error ? err.message : 'Failed to create application');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleBackToStart = () => {
    setAppState('input');
    setJobDescription(null);
    setResume(null);
    setApplication(null);
    setError(null);
  };

  const canGenerate = jobDescription && resume && !isProcessing;

  // Show error alert if there's an error
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto">
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
            <Button onClick={handleBackToStart} className="w-full">
              Back to Start
            </Button>
          </div>
        </div>
      </div>
    );
  }

  if (appState === 'results' && application) {
    return (
      <ResultsPage 
        applicationId={application.id} 
        onBack={handleBackToStart}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center gap-2">
            <Sparkles className="h-8 w-8 text-blue-600" />
            LaudatorAI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Your AI advocate in the job market, automating resume tailoring and cover letter generation.
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          {appState === 'input' && (
            <>
              <div className="grid md:grid-cols-2 gap-8 mb-8">
                {/* Job URL Input */}
                <JobDescriptionInput 
                  onJobDescriptionExtracted={handleJobDescriptionExtracted}
                />

                {/* Resume Upload */}
                <ResumeUpload 
                  onResumeUploaded={handleResumeUploaded}
                />
              </div>

              {/* Status Indicators */}
              <div className="grid md:grid-cols-2 gap-4 mb-8">
                <Card className={jobDescription ? 'border-green-500 bg-green-50' : ''}>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-2">
                      {jobDescription ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <FileText className="h-5 w-5 text-gray-400" />
                      )}
                      <span className="text-sm font-medium">
                        Job Description: {jobDescription ? 'Extracted' : 'Pending'}
                      </span>
                    </div>
                    {jobDescription && (
                      <p className="text-xs text-gray-600 mt-1">
                        {jobDescription.title} at {jobDescription.company}
                      </p>
                    )}
                  </CardContent>
                </Card>

                <Card className={resume ? 'border-green-500 bg-green-50' : ''}>
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-2">
                      {resume ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <FileText className="h-5 w-5 text-gray-400" />
                      )}
                      <span className="text-sm font-medium">
                        Resume: {resume ? 'Uploaded' : 'Pending'}
                      </span>
                    </div>
                    {resume && (
                      <p className="text-xs text-gray-600 mt-1">
                        {resume.filename}
                      </p>
                    )}
                  </CardContent>
                </Card>
              </div>

              {/* Error Display */}
              {/* Error Display */}

              {/* Generate Button */}
              <div className="text-center">
                <Button 
                  size="lg" 
                  className="px-8 py-3"
                  onClick={handleGenerateApplication}
                  disabled={!canGenerate}
                >
                  <Sparkles className="h-5 w-5 mr-2" />
                  Generate Tailored Resume & Cover Letter
                </Button>
                {!canGenerate && (
                  <p className="text-sm text-gray-500 mt-2">
                    Please provide both a job description and resume to continue
                  </p>
                )}
              </div>
            </>
          )}

          {appState === 'processing' && (
            <div className="max-w-2xl mx-auto text-center">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-center gap-2">
                    <LoadingSpinner size="md" />
                    Processing Your Application
                  </CardTitle>
                  <CardDescription>
                    We're tailoring your resume and generating your cover letter...
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Progress value={50} />
                  <p className="text-sm text-gray-600">
                    This may take a few minutes. Please don't close this page.
                  </p>
                  <Button 
                    variant="outline" 
                    onClick={handleBackToStart}
                    className="mt-4"
                  >
                    Cancel
                  </Button>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Features */}
          <div className="mt-16 grid md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Smart Extraction</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Automatically extract and normalize job descriptions from any job posting URL
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">AI Tailoring</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Use advanced AI to tailor your resume and generate compelling cover letters
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Professional Output</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600">
                  Get polished DOCX and PDF files ready for your job applications
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
