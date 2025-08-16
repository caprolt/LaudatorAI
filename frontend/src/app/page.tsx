import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Upload, FileText, Send } from 'lucide-react'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            LaudatorAI
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Your AI advocate in the job market, automating resume tailoring and cover letter generation.
          </p>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Job URL Input */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Job Description
                </CardTitle>
                <CardDescription>
                  Paste the job posting URL to extract the job description
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="job-url">Job Posting URL</Label>
                  <Input
                    id="job-url"
                    placeholder="https://example.com/job-posting"
                    className="w-full"
                  />
                </div>
                <Button className="w-full">
                  <Send className="h-4 w-4 mr-2" />
                  Extract Job Description
                </Button>
              </CardContent>
            </Card>

            {/* Resume Upload */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Upload className="h-5 w-5" />
                  Resume Upload
                </CardTitle>
                <CardDescription>
                  Upload your base resume to get started
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <Upload className="h-8 w-8 mx-auto text-gray-400 mb-2" />
                  <p className="text-sm text-gray-600 mb-2">
                    Drag and drop your resume here, or click to browse
                  </p>
                  <Button variant="outline" size="sm">
                    Choose File
                  </Button>
                </div>
                <p className="text-xs text-gray-500">
                  Supported formats: PDF, DOCX (max 10MB)
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Generate Button */}
          <div className="mt-8 text-center">
            <Button size="lg" className="px-8 py-3">
              Generate Tailored Resume & Cover Letter
            </Button>
          </div>

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
  )
}
