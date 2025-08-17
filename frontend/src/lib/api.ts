import { apiConfig } from './config';

const API_BASE_URL = apiConfig.baseUrl + apiConfig.endpoints.jobs.replace('/api/v1/jobs', '/api/v1');

export interface JobDescription {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements: string[];
  created_at: string;
}

export interface ResumeData {
  id: string;
  filename: string;
  content: any; // Structured JSON content
  created_at: string;
}

export interface Application {
  id: string;
  job_description_id: string;
  resume_id: string;
  tailored_resume_url?: string;
  cover_letter_url?: string;
  status: 'processing' | 'completed' | 'failed';
  created_at: string;
}

export interface CoverLetter {
  id: string;
  application_id: string;
  content: string;
  docx_url?: string;
  pdf_url?: string;
  created_at: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API request failed: ${response.status} ${response.statusText} - ${errorText}`);
    }

    return response.json();
  }

  // Job Description endpoints
  async extractJobDescription(url: string): Promise<JobDescription> {
    const response = await this.request<any>('/jobs/extract', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
    
    // Map backend response to frontend format
    return {
      id: response.id.toString(),
      title: response.title,
      company: response.company,
      location: response.location || '',
      description: response.description,
      requirements: response.requirements ? (Array.isArray(response.requirements) ? response.requirements : [response.requirements]) : [],
      created_at: response.created_at,
    };
  }

  async getJobDescription(id: string): Promise<JobDescription> {
    const response = await this.request<any>(`/jobs/${id}`);
    
    return {
      id: response.id.toString(),
      title: response.title,
      company: response.company,
      location: response.location || '',
      description: response.description,
      requirements: response.requirements ? (Array.isArray(response.requirements) ? response.requirements : [response.requirements]) : [],
      created_at: response.created_at,
    };
  }

  // Resume endpoints
  async uploadResume(file: File): Promise<ResumeData> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/resumes/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Resume upload failed: ${response.status} ${response.statusText} - ${errorText}`);
    }

    const data = await response.json();
    
    return {
      id: data.id.toString(),
      filename: data.filename,
      content: data.content || data.parsed_content,
      created_at: data.created_at,
    };
  }

  async getResume(id: string): Promise<ResumeData> {
    const response = await this.request<any>(`/resumes/${id}`);
    
    return {
      id: response.id.toString(),
      filename: response.filename,
      content: response.content || response.parsed_content,
      created_at: response.created_at,
    };
  }

  // Application endpoints
  async createApplication(
    jobDescriptionId: string,
    resumeId: string
  ): Promise<Application> {
    const response = await this.request<any>('/applications', {
      method: 'POST',
      body: JSON.stringify({
        job_id: parseInt(jobDescriptionId),
        resume_id: parseInt(resumeId),
      }),
    });
    
    return {
      id: response.id.toString(),
      job_description_id: response.job_id.toString(),
      resume_id: response.resume_id.toString(),
      tailored_resume_url: response.tailored_resume_url,
      cover_letter_url: response.cover_letter_url,
      status: response.status,
      created_at: response.created_at,
    };
  }

  async getApplication(id: string): Promise<Application> {
    const response = await this.request<any>(`/applications/${id}`);
    
    return {
      id: response.id.toString(),
      job_description_id: response.job_id.toString(),
      resume_id: response.resume_id.toString(),
      tailored_resume_url: response.tailored_resume_url,
      cover_letter_url: response.cover_letter_url,
      status: response.status,
      created_at: response.created_at,
    };
  }

  async getApplicationStatus(id: string): Promise<Application> {
    return this.getApplication(id); // Use the same endpoint for now
  }

  // Cover Letter endpoints
  async getCoverLetter(applicationId: string): Promise<CoverLetter> {
    const response = await this.request<any>(`/cover-letters/${applicationId}`);
    
    return {
      id: response.id.toString(),
      application_id: response.application_id.toString(),
      content: response.content,
      docx_url: response.docx_url,
      pdf_url: response.pdf_url,
      created_at: response.created_at,
    };
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health');
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
