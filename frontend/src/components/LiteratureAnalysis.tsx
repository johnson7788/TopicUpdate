import React, { useState, useEffect, useCallback } from 'react';
import { TrendingUp, PieChart, Download, Eye, Filter, Calendar, BookOpen, FileText } from 'lucide-react';
import TrendChart from './TrendChart';
import DistributionChart from './DistributionChart';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// --- TypeScript Interfaces ---
interface Topic {
  id: number;
  name: string;
}

interface Literature {
  id: number;
  title: string;
  authors: string[];
  publication_date: string;
  journal_name: string;
  literature_type: string;
  summary: string;
}

interface LiteratureAnalysisData {
  stats: {
    total_count: number;
    high_citation_count: number;
    clinical_trial_count: number;
    meta_analysis_count: number;
  };
  trend_data: { date: string; count: number }[];
  distribution_data: { type: string; count: number }[];
  literature: Literature[];
}

const LiteratureAnalysis = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);
  const [analysisData, setAnalysisData] = useState<LiteratureAnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedIds, setExpandedIds] = useState<Set<number>>(new Set());

  const toggleSummary = (id: number) => {
    setExpandedIds(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  // Fetch all topics for the dropdown
  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await fetch(`${API_URL}/topics/`);
        if (!response.ok) throw new Error('Failed to fetch topics');
        const data: Topic[] = await response.json();
        setTopics(data);
        if (data.length > 0) {
          setSelectedTopicId(data[0].id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Could not fetch topics');
      }
    };
    fetchTopics();
  }, []);

  // Fetch analysis data when a topic is selected
  useEffect(() => {
    if (!selectedTopicId) return;

    const fetchAnalysisData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`${API_URL}/topics/${selectedTopicId}/literature-analysis`);
        if (!response.ok) throw new Error(`Failed to fetch analysis for topic ${selectedTopicId}`);
        const data: LiteratureAnalysisData = await response.json();
        setAnalysisData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
        setAnalysisData(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchAnalysisData();
  }, [selectedTopicId]);

  const StatCard = ({ title, value, total, icon, color }) => (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">{title}</p>
          <p className={`text-3xl font-bold text-gray-900 ${color}`}>{value}</p>
          {total && <p className="text-xs text-gray-500 mt-1">占总数 {total}</p>}
        </div>
        <div className={`bg-${color}-100 p-3 rounded-full`}>{icon}</div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">相关的主题文献更新</h2>
          <p className="text-gray-600 mt-1">查看已监控主题的最新文献分析</p>
        </div>
        <div className="flex items-center space-x-3">
          <select 
            value={selectedTopicId || ''}
            onChange={(e) => setSelectedTopicId(Number(e.target.value))}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 min-w-[250px]"
            disabled={!topics.length}
          >
            {topics.length > 0 ? (
              topics.map(topic => <option key={topic.id} value={topic.id}>{topic.name}</option>)
            ) : (
              <option>Loading topics...</option>
            )}
          </select>
        </div>
      </div>

      {isLoading && <div className="text-center p-8">Loading analysis...</div>}
      {error && <div className="text-center p-8 text-red-600 bg-red-50 rounded-lg">Error: {error}</div>}
      
      {analysisData && !isLoading && (
        <>
          {/* Statistics Overview */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard title="文献总数" value={analysisData.stats.total_count} icon={<BookOpen className="h-6 w-6 text-blue-600" />} color="blue" />
            <StatCard title="临床试验" value={analysisData.stats.clinical_trial_count} icon={<PieChart className="h-6 w-6 text-green-600" />} color="green" />
            <StatCard title="Meta分析" value={analysisData.stats.meta_analysis_count} icon={<PieChart className="h-6 w-6 text-purple-600" />} color="purple" />
            <StatCard title="高被引文献" value={analysisData.stats.high_citation_count} icon={<TrendingUp className="h-6 w-6 text-orange-600" />} color="orange" />
          </div>

          {/* Charts Section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">文献发表趋势</h3>
              <div className="h-64">
                 <TrendChart data={analysisData.trend_data} />
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">研究类型分布</h3>
              <div className="h-64">
                <DistributionChart data={analysisData.distribution_data} />
              </div>
            </div>
          </div>

          {/* Literature List */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="p-6 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">文献列表</h3>
            </div>
            <div className="divide-y divide-gray-200">
              {analysisData.literature.map((paper) => (
                <div key={paper.id} className="p-6 hover:bg-gray-50 cursor-pointer" onClick={() => toggleSummary(paper.id)}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="text-lg font-medium text-gray-900 mb-2">{paper.title}</h4>
                      <p className="text-sm text-gray-600 mb-2">{paper.authors.join(', ')}</p>
                      {expandedIds.has(paper.id) && (
                        <div className="my-3 p-3 bg-gray-50 border rounded-md">
                          <div className="flex items-center text-sm font-semibold text-gray-800 mb-2">
                            <FileText className="h-4 w-4 mr-2 flex-shrink-0" />
                            <span>中英文介绍</span>
                          </div>
                          <p className="text-sm text-gray-700 pl-6">{paper.summary}</p>
                        </div>
                      )}
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span><strong>{paper.journal_name}</strong> ({new Date(paper.publication_date).getFullYear()})</span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                          {paper.literature_type}
                        </span>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-4">
                      <button className="p-2 hover:bg-gray-100 rounded-full" title="Download" onClick={(e) => e.stopPropagation()}>
                        <Download className="h-4 w-4 text-gray-600" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default LiteratureAnalysis;
