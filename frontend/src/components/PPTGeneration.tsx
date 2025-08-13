import React, { useState, useEffect } from 'react';
import { 
  Presentation, 
  Download, 
  Eye,
  X,
  CheckCircle,
  XCircle,
  Clock,
  GitCommitHorizontal
} from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// --- TypeScript Interfaces ---
interface PPTPushRecord {
  id: number;
  push_time: string;
  topic_name: string;
  ppt_filename: string;
  recipients: string[];
  channel: string;
  status: 'success' | 'failed' | 'pending';
  diff_summary?: string;
}

const PPTGeneration = () => {
  const [records, setRecords] = useState<PPTPushRecord[]>([]);
  const [topics, setTopics] = useState<string[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRecord, setSelectedRecord] = useState<PPTPushRecord | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(`${API_URL}/ppt-history/`);
        if (!response.ok) throw new Error('Failed to fetch PPT history.');
        let data: PPTPushRecord[] = await response.json();

        setRecords(data);
        const uniqueTopics = [...new Set(data.map(r => r.topic_name))];
        setTopics(uniqueTopics);
        if (uniqueTopics.length > 0) {
            setSelectedTopic(uniqueTopics[0]);
        }

      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const getStatusIndicator = (status: PPTPushRecord['status']) => {
    switch (status) {
      case 'success':
        return <span className="flex items-center space-x-2 px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm"><CheckCircle className="h-4 w-4" /><span>成功</span></span>;
      case 'failed':
        return <span className="flex items-center space-x-2 px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm"><XCircle className="h-4 w-4" /><span>失败</span></span>;
      case 'pending':
        return <span className="flex items-center space-x-2 px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-sm"><Clock className="h-4 w-4" /><span>处理中</span></span>;
    }
  };

  const renderPreviewModal = () => {
    if (!selectedRecord) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[80vh] flex flex-col">
          <div className="flex items-center justify-between p-4 border-b">
            <h3 className="text-lg font-bold text-gray-900">预览: {selectedRecord.ppt_filename}</h3>
            <button onClick={() => setSelectedRecord(null)} className="p-2 rounded-full hover:bg-gray-200"><X className="h-5 w-5" /></button>
          </div>
          <div className="p-6 flex-grow flex items-center justify-center bg-gray-100">
            <div className="text-center">
              <Presentation className="h-24 w-24 text-gray-400 mx-auto" />
              <p className="mt-4 text-gray-600">PPT 预览区</p>
              <p className="text-sm text-gray-500">实际应用中可嵌入PPT预览插件</p>
            </div>
          </div>
          <div className="p-4 bg-gray-50 border-t flex justify-end">
            <a href={`${API_URL}/PPT/${selectedRecord.ppt_filename}`} download={selectedRecord.ppt_filename} className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
              <Download className="h-4 w-4" />
              <span>下载文件</span>
            </a>
          </div>
        </div>
      </div>
    );
  };
  
  const filteredRecords = records
    .filter(r => r.topic_name === selectedTopic)
    .slice(0, 10);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">PPT 生成历史</h2>
        <p className="text-gray-600 mt-2">选择一个主题，查看最近10条生成记录及其版本间的差异总结。</p>
      </div>

      {/* Topic Selection */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">选择主题</h3>
        <div className="flex flex-wrap gap-3">
          {isLoading ? <p>Loading topics...</p> : topics.map(topic => (
            <button
              key={topic}
              onClick={() => setSelectedTopic(topic)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ease-in-out ${
                selectedTopic === topic
                ? 'bg-blue-600 text-white shadow-md scale-105'
                : 'bg-gray-100 text-gray-700 hover:bg-blue-100 border border-gray-200'
              }`}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">推送时间</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">文件名称</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">接收人</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {isLoading ? (
              <tr><td colSpan={5} className="text-center p-8">Loading history...</td></tr>
            ) : error ? (
              <tr><td colSpan={5} className="text-center p-8 text-red-600">{error}</td></tr>
            ) : filteredRecords.length === 0 ? (
              <tr><td colSpan={5} className="text-center p-8 text-gray-500">没有找到该主题的记录</td></tr>
            ) : (
              filteredRecords.map((record) => (
                <React.Fragment key={record.id}>
                  <tr className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{new Date(record.push_time).toLocaleString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">{record.ppt_filename}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">{record.recipients.join(', ')}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{getStatusIndicator(record.status)}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium flex items-center space-x-4">
                      <button onClick={() => setSelectedRecord(record)} className="text-blue-600 hover:text-blue-800 flex items-center space-x-1">
                        <Eye className="h-4 w-4" /><span>查看</span>
                      </button>
                      <a href={`${API_URL}/PPT/${record.ppt_filename}`} download={record.ppt_filename} className="text-blue-600 hover:text-blue-800 flex items-center space-x-1">
                        <Download className="h-4 w-4" /><span>PPT下载</span>
                      </a>
                      <a href={`${API_URL}/PPT/${record.ppt_filename}`} download={record.ppt_filename} className="text-blue-600 hover:text-blue-800 flex items-center space-x-1">
                        <Download className="h-4 w-4" /><span>文献下载</span>
                      </a>
                    </td>
                  </tr>
                  {record.diff_summary && (
                    <tr className="bg-blue-50">
                      <td colSpan={5} className="px-6 py-3">
                        <div className="flex items-center space-x-3 text-sm">
                          <GitCommitHorizontal className="h-5 w-5 text-blue-500" />
                          <p className="text-blue-800">
                            <span className="font-semibold">版本环比差异:</span> {record.diff_summary}
                          </p>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))
            )}
          </tbody>
        </table>
      </div>
      {renderPreviewModal()}
    </div>
  );
};

export default PPTGeneration;
