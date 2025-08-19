'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { FileText, Send, AlertCircle, CheckCircle } from 'lucide-react';
import { apiClient, JobDescription } from '@/lib/api';

interface JobDescriptionInputProps {
  onJobDescriptionExtracted: (jobDescription: JobDescription) => void;
}

export function JobDescriptionInput({ onJobDescriptionExtracted }: JobDescriptionInputProps) {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleExtract = async () => {
    if (!url.trim()) {
      setError('Please enter a job posting URL');
      return;
    }

    setIsLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const jobDescription = await apiClient.extractJobDescription(url);
      setSuccess('Job description extracted successfully!');
      onJobDescriptionExtracted(jobDescription);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to extract job description');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="job-url" className="text-gray-700 font-medium">Job Posting URL</Label>
        <Input
          id="job-url"
          type="url"
          placeholder="https://example.com/job-posting"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full border-gray-300 focus:border-yellow-500 focus:ring-yellow-500"
          disabled={isLoading}
        />
      </div>
      
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="border-green-200 bg-green-50 text-green-800">
          <CheckCircle className="h-4 w-4" />
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      <Button 
        variant="maroon"
        className="w-full" 
        onClick={handleExtract}
        disabled={isLoading || !url.trim()}
      >
        <Send className="h-4 w-4 mr-2" />
        {isLoading ? 'Extracting...' : 'Extract Job Description'}
      </Button>
    </div>
  );
}
