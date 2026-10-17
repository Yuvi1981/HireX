import React, { useState } from 'react';
import { Mic, ShieldCheck, BadgeCheck } from 'lucide-react';
import { StudentProfile } from '../types';
import { InterviewSimulatorView } from './InterviewSimulatorView';
import { CertificateScannerWorkspace } from '../components/certificates/CertificateScannerWorkspace';

interface PortfolioTranscriptViewProps {
  student: StudentProfile;
}

export const PortfolioTranscriptView: React.FC<PortfolioTranscriptViewProps> = ({ student }) => {
  const [activeTab, setActiveTab] = useState<'certificate_scanner' | 'mock_interview'>('certificate_scanner');

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* 1. Header with Tab Switcher */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-white dark:bg-card-dark border border-slate-200/90 dark:border-slate-800 shadow-sm">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-indigo-50 dark:bg-indigo-950/60 text-brand-indigo border border-indigo-200/80 dark:border-indigo-800/80">
              <BadgeCheck className="w-5 h-5" />
            </div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              Certificate Scanner & Skill Verification
            </h1>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-3xl">
            OCR & AI-powered document parsing for Microsoft certifications and recognized industry providers. Extracted skills are mapped to competencies and verified in your student profile.
          </p>
        </div>

        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200/60 dark:border-slate-700 shrink-0">
          <button
            onClick={() => setActiveTab('certificate_scanner')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'certificate_scanner'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5 text-brand-indigo" />
            <span>Certificate Scanner & Skills</span>
          </button>
          <button
            onClick={() => setActiveTab('mock_interview')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'mock_interview'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            <Mic className="w-3.5 h-3.5" />
            <span>AI Mock Interviewer</span>
          </button>
        </div>
      </div>

      {activeTab === 'certificate_scanner' ? (
        /* Working Certificate Scanner & Skill Verification Workspace */
        <CertificateScannerWorkspace student={student} />
      ) : (
        /* AI Mock Technical Interview Simulator */
        <InterviewSimulatorView student={student} />
      )}
    </div>
  );
};

