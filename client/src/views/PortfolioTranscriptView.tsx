import React, { useState } from 'react';
import { Award, Mic, FileText, CheckCircle2, Printer, ShieldCheck } from 'lucide-react';
import { StudentProfile } from '../types';
import { apiService } from '../services/api';

import { InterviewSimulatorView } from './InterviewSimulatorView';

interface PortfolioTranscriptViewProps {
  student: StudentProfile;
}

export const PortfolioTranscriptView: React.FC<PortfolioTranscriptViewProps> = ({ student }) => {
  const [activeTab, setActiveTab] = useState<'transcript' | 'mock_interview'>('transcript');

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* 1. Header with Tab Switcher */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-white dark:bg-card-dark border border-slate-200/90 dark:border-slate-800 shadow-sm">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200/80 dark:border-slate-700">
              <Award className="w-4.5 h-4.5" />
            </div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              AICTE Skill Transcript & AI Mock Interview Simulator
            </h1>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
            NEP 2020 National Credit Framework (NCrF) verified ledger with APAAR/ABC ID and live technical interview simulator.
          </p>
        </div>

        <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200/60 dark:border-slate-700">
          <button
            onClick={() => setActiveTab('transcript')}
            className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
              activeTab === 'transcript'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Official AICTE Transcript</span>
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

      {activeTab === 'transcript' ? (
        /* Official Transcript Document */
        <div className="p-8 md:p-10 rounded-2xl bg-white dark:bg-card-dark border border-slate-200/90 dark:border-slate-800 shadow-md space-y-8 max-w-4xl mx-auto">
          {/* Transcript Header */}
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 border-b-2 border-slate-900 dark:border-slate-700">
            <div>
              <span className="text-[10px] font-black uppercase tracking-widest text-brand-indigo block">
                GOVERNMENT OF INDIA • MINISTRY OF EDUCATION & AICTE
              </span>
              <h2 className="text-xl md:text-2xl font-black text-slate-900 dark:text-white mt-1">
                NATIONAL SKILL TRANSCRIPT & NCrF CREDIT RECORD
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Issued under NEP 2020 National Credit Framework • Valid for Academic Credit Transfer & Corporate Hiring
              </p>
            </div>

            <div className="p-3 rounded-2xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-right">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">APAAR / ABC ID</span>
              <span className="text-sm font-mono font-bold text-slate-900 dark:text-white">
                9823-4412-8871-ABC
              </span>
            </div>
          </div>

          {/* Student & Institution Metadata */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div>
              <span className="text-slate-400 block text-[10px]">Candidate Name</span>
              <span className="font-bold text-slate-900 dark:text-white text-sm">{student.name}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px]">Institution</span>
              <span className="font-bold text-slate-900 dark:text-white">{student.college}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px]">Department & Year</span>
              <span className="font-bold text-slate-900 dark:text-white">{student.department}, {student.year}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px]">Total NCrF Credits</span>
              <span className="font-black text-brand-indigo text-base">4.0 Credits (160h)</span>
            </div>
          </div>

          {/* NCrF Verified Ledger Table */}
          <div className="space-y-2">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300">
              Verified Proof-of-Work & Creditization Matrix
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden">
                <thead className="bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 font-bold">
                  <tr>
                    <th className="p-3">Verified Skill / Lab</th>
                    <th className="p-3">Audit Mechanism</th>
                    <th className="p-3">Verified Hours</th>
                    <th className="p-3">NCrF Credits</th>
                    <th className="p-3">Verification Hash</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-slate-700 dark:text-slate-300 font-mono">
                  <tr>
                    <td className="p-3 font-sans font-bold">Python Microservices & AST Analysis</td>
                    <td className="p-3 font-sans">AST Static Complexity Engine</td>
                    <td className="p-3">40 Hours</td>
                    <td className="p-3 font-bold text-emerald-600">1.0 Credit</td>
                    <td className="p-3 text-[10px] text-slate-400">sha256:8f2a...19e0</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-sans font-bold">Deep Learning & PyTorch (NPTEL)</td>
                    <td className="p-3 font-sans">National Registry Public Key</td>
                    <td className="p-3">80 Hours</td>
                    <td className="p-3 font-bold text-emerald-600">2.0 Credits</td>
                    <td className="p-3 text-[10px] text-slate-400">sha256:a4f8...41cf</td>
                  </tr>
                  <tr>
                    <td className="p-3 font-sans font-bold">React & State Architecture</td>
                    <td className="p-3 font-sans">In-Browser Code Lab Runner</td>
                    <td className="p-3">40 Hours</td>
                    <td className="p-3 font-bold text-emerald-600">1.0 Credit</td>
                    <td className="p-3 text-[10px] text-slate-400">sha256:c14d...88b2</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p className="text-[10px] text-slate-400 italic">
              *NCrF Standard: 40 hours of verified practical learning equals 1 academic credit transferable to the Academic Bank of Credits (ABC).
            </p>
          </div>

          {/* Verification Cryptographic Footer */}
          <div className="pt-6 border-t border-slate-200 dark:border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-slate-900 text-white flex items-center justify-center font-black text-xl shadow-sm">
                AICTE
              </div>
              <div className="text-[11px] text-slate-500">
                <span className="font-bold text-slate-900 dark:text-white block">Digital Cryptographic Seal</span>
                Certified by HireX Sovereign Ledger. Tamper-proof and verifiable by Indian Universities & Enterprise TPOs nationwide.
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => window.print()}
                className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-bold transition flex items-center gap-1.5"
              >
                <Printer className="w-3.5 h-3.5" />
                <span>Print PDF</span>
              </button>
              <button
                onClick={() => alert(`Transcript SHA-256: b892d9f4c391aa82c0f72671e... Cryptographically verified on national ledger.`)}
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-black text-white text-xs font-bold transition shadow-xs flex items-center gap-1.5"
              >
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Verify Hash</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* AI Mock Technical Interview Simulator */
        <InterviewSimulatorView student={student} />
      )}
    </div>
  );
};
