'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ElegantCard, ElegantCardContent, ElegantCardDescription, ElegantCardHeader, ElegantCardTitle } from '@/components/ui/elegant-card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import { FileText, Send, CheckCircle, AlertCircle, Sparkles, Crown, Award, Target } from 'lucide-react';
import { JobDescriptionInput } from '@/components/job-description-input';
import { ResumeUpload } from '@/components/resume-upload';
import { ResultsPage } from '@/components/results-page';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { Logo } from '@/components/ui/logo';
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
      <div className="min-h-screen maroon-bg">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <Logo size="lg" />
            </div>
            <ElegantCard variant="default" glow={true}>
              <ElegantCardContent className="pt-6">
                <Alert variant="destructive" className="mb-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
                <Button variant="gold" onClick={handleBackToStart} className="w-full">
                  <Crown className="h-4 w-4 mr-2" />
                  Back to Start
                </Button>
              </ElegantCardContent>
            </ElegantCard>
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
    <div className="min-h-screen maroon-bg">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <Logo size="xl" className="mb-6" />
        </div>

        {/* Main Content */}
        <div className="max-w-5xl mx-auto">
          {appState === 'input' && (
            <>
              <div className="grid md:grid-cols-2 gap-8 mb-8">
                {/* Job URL Input */}
                <ElegantCard variant="default" glow={true}>
                  <ElegantCardHeader>
                    <ElegantCardTitle className="flex items-center gap-2 text-gray-800">
                      <Target className="h-5 w-5 text-red-700" />
                      Job Description
                    </ElegantCardTitle>
                    <ElegantCardDescription className="text-gray-600">
                      Extract job details from any posting URL
                    </ElegantCardDescription>
                  </ElegantCardHeader>
                  <ElegantCardContent>
                    <JobDescriptionInput 
                      onJobDescriptionExtracted={handleJobDescriptionExtracted}
                    />
                  </ElegantCardContent>
                </ElegantCard>

                {/* Resume Upload */}
                <ElegantCard variant="default" glow={true}>
                  <ElegantCardHeader>
                    <ElegantCardTitle className="flex items-center gap-2 text-gray-800">
                      <FileText className="h-5 w-5 text-red-700" />
                      Resume Upload
                    </ElegantCardTitle>
                    <ElegantCardDescription className="text-gray-600">
                      Upload your current resume for tailoring
                    </ElegantCardDescription>
                  </ElegantCardHeader>
                  <ElegantCardContent>
                    <ResumeUpload 
                      onResumeUploaded={handleResumeUploaded}
                    />
                  </ElegantCardContent>
                </ElegantCard>
              </div>

              {/* Status Indicators */}
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <ElegantCard 
                  variant={jobDescription ? 'gold' : 'default'} 
                  glow={true}
                  className="transition-all duration-300"
                >
                  <ElegantCardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      {jobDescription ? (
                        <div className="p-2 bg-green-100 rounded-full">
                          <CheckCircle className="h-5 w-5 text-green-600" />
                        </div>
                      ) : (
                        <div className="p-2 bg-gray-100 rounded-full">
                          <Target className="h-5 w-5 text-gray-400" />
                        </div>
                      )}
                      <div>
                        <span className="text-sm font-semibold text-gray-800">
                          Job Description: {jobDescription ? 'Extracted' : 'Pending'}
                        </span>
                        {jobDescription && (
                          <p className="text-xs text-gray-600 mt-1">
                            {jobDescription.title} at {jobDescription.company}
                          </p>
                        )}
                      </div>
                    </div>
                  </ElegantCardContent>
                </ElegantCard>

                <ElegantCard 
                  variant={resume ? 'gold' : 'default'} 
                  glow={true}
                  className="transition-all duration-300"
                >
                  <ElegantCardContent className="pt-6">
                    <div className="flex items-center gap-3">
                      {resume ? (
                        <div className="p-2 bg-green-100 rounded-full">
                          <CheckCircle className="h-5 w-5 text-green-600" />
                        </div>
                      ) : (
                        <div className="p-2 bg-gray-100 rounded-full">
                          <FileText className="h-5 w-5 text-gray-400" />
                        </div>
                      )}
                      <div>
                        <span className="text-sm font-semibold text-gray-800">
                          Resume: {resume ? 'Uploaded' : 'Pending'}
                        </span>
                        {resume && (
                          <p className="text-xs text-gray-600 mt-1">
                            {resume.filename}
                          </p>
                        )}
                      </div>
                    </div>
                  </ElegantCardContent>
                </ElegantCard>
              </div>

              {/* Generate Button */}
              <div className="text-center">
                <Button 
                  variant="gold"
                  size="xl"
                  className="font-semibold gold-shadow"
                  onClick={handleGenerateApplication}
                  disabled={!canGenerate}
                >
                  <Crown className="h-6 w-6 mr-3" />
                  Generate Tailored Resume & Cover Letter
                </Button>
                {!canGenerate && (
                  <p className="text-sm text-yellow-200 mt-4 font-medium">
                    Please provide both a job description and resume to continue
                  </p>
                )}
              </div>
            </>
          )}

          {appState === 'processing' && (
            <div className="max-w-2xl mx-auto text-center">
              <ElegantCard variant="default" glow={true}>
                <ElegantCardHeader>
                  <ElegantCardTitle className="flex items-center justify-center gap-3 text-gray-800">
                    <LoadingSpinner size="md" />
                    Processing Your Application
                  </ElegantCardTitle>
                  <ElegantCardDescription className="text-gray-600">
                    We're tailoring your resume and generating your cover letter with precision...
                  </ElegantCardDescription>
                </ElegantCardHeader>
                <ElegantCardContent className="space-y-6">
                  <Progress value={50} className="h-3" />
                  <p className="text-sm text-gray-600">
                    This may take a few minutes. Please don't close this page.
                  </p>
                  <Button 
                    variant="elegant" 
                    onClick={handleBackToStart}
                    className="mt-4"
                  >
                    Cancel
                  </Button>
                </ElegantCardContent>
              </ElegantCard>
            </div>
          )}

          {/* Features */}
          <div className="mt-20 grid md:grid-cols-3 gap-8">
            <ElegantCard variant="default" glow={true} className="hover:scale-105 transition-transform duration-300">
              <ElegantCardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-red-100 rounded-full">
                    <Target className="h-6 w-6 text-red-700" />
                  </div>
                  <ElegantCardTitle className="text-lg text-gray-800">Smart Extraction</ElegantCardTitle>
                </div>
              </ElegantCardHeader>
              <ElegantCardContent>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Automatically extract and normalize job descriptions from any job posting URL with advanced AI processing
                </p>
              </ElegantCardContent>
            </ElegantCard>
            
            <ElegantCard variant="default" glow={true} className="hover:scale-105 transition-transform duration-300">
              <ElegantCardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-yellow-100 rounded-full">
                    <Award className="h-6 w-6 text-yellow-700" />
                  </div>
                  <ElegantCardTitle className="text-lg text-gray-800">AI Tailoring</ElegantCardTitle>
                </div>
              </ElegantCardHeader>
              <ElegantCardContent>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Use advanced AI to tailor your resume and generate compelling cover letters that match job requirements
                </p>
              </ElegantCardContent>
            </ElegantCard>
            
            <ElegantCard variant="default" glow={true} className="hover:scale-105 transition-transform duration-300">
              <ElegantCardHeader>
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-green-100 rounded-full">
                    <Crown className="h-6 w-6 text-green-700" />
                  </div>
                  <ElegantCardTitle className="text-lg text-gray-800">Professional Output</ElegantCardTitle>
                </div>
              </ElegantCardHeader>
              <ElegantCardContent>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Get polished DOCX and PDF files ready for your job applications with professional formatting
                </p>
              </ElegantCardContent>
            </ElegantCard>
          </div>
        </div>
      </div>
    </div>
  );
}
