'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { FileText, Download, Edit, Save, X, CheckCircle, AlertCircle } from 'lucide-react';

interface PreviewDiffProps {
  title: string;
  originalContent: string;
  generatedContent: string;
  onSave: (content: string) => void;
  onDownload: () => void;
  fileType: 'resume' | 'cover-letter';
}

export function PreviewDiff({ 
  title, 
  originalContent, 
  generatedContent, 
  onSave, 
  onDownload,
  fileType 
}: PreviewDiffProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedContent, setEditedContent] = useState(generatedContent);
  const [isSaving, setIsSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const handleSave = async () => {
    setIsSaving(true);
    setSaveStatus('idle');
    
    try {
      await onSave(editedContent);
      setSaveStatus('success');
      setIsEditing(false);
    } catch (error) {
      setSaveStatus('error');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditedContent(generatedContent);
    setIsEditing(false);
    setSaveStatus('idle');
  };

  const renderDiff = () => {
    const originalLines = originalContent.split('\n');
    const generatedLines = generatedContent.split('\n');
    
    return (
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {generatedLines.map((line, index) => {
          const originalLine = originalLines[index] || '';
          const isModified = line !== originalLine;
          
          return (
            <div 
              key={index} 
              className={`p-2 rounded ${
                isModified 
                  ? 'bg-green-50 border-l-4 border-green-500' 
                  : 'bg-gray-50'
              }`}
            >
              <div className="text-sm font-mono">
                {isModified && (
                  <span className="text-red-500 line-through mr-2">
                    {originalLine}
                  </span>
                )}
                <span className={isModified ? 'text-green-700 font-medium' : 'text-gray-700'}>
                  {line}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              {title}
            </CardTitle>
            <CardDescription>
              Preview and edit your generated {fileType === 'resume' ? 'resume' : 'cover letter'}
            </CardDescription>
          </div>
          <div className="flex gap-2">
            {!isEditing ? (
              <>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setIsEditing(true)}
                >
                  <Edit className="h-4 w-4 mr-2" />
                  Edit
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={onDownload}
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
              </>
            ) : (
              <>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleCancel}
                  disabled={isSaving}
                >
                  <X className="h-4 w-4 mr-2" />
                  Cancel
                </Button>
                <Button
                  size="sm"
                  onClick={handleSave}
                  disabled={isSaving}
                >
                  <Save className="h-4 w-4 mr-2" />
                  {isSaving ? 'Saving...' : 'Save'}
                </Button>
              </>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {saveStatus === 'success' && (
          <Alert>
            <CheckCircle className="h-4 w-4" />
            <AlertDescription>Changes saved successfully!</AlertDescription>
          </Alert>
        )}

        {saveStatus === 'error' && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>Failed to save changes. Please try again.</AlertDescription>
          </Alert>
        )}

        {isEditing ? (
          <div className="space-y-2">
            <label className="text-sm font-medium">Edit Content</label>
            <Textarea
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              className="min-h-[400px] font-mono text-sm"
              placeholder="Edit your content here..."
            />
          </div>
        ) : (
          <div className="space-y-2">
            <label className="text-sm font-medium">Preview (Changes Highlighted)</label>
            {renderDiff()}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
