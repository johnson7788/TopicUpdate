import React, { useState, useEffect, useCallback} from 'react';
import {
  Plus,
  Edit,
  Trash2,
  History,
  X,
  Save,
  Settings,
  Bell,
  FileText,
  Clock,
  CheckCircle,
  AlertCircle,
  ChevronRight
} from 'lucide-react';

// Based on backend/Document.md
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Topic {
  id: number;
  name: string;
  keywords: string[];
  created_at: string;
  last_updated: string;
  frequency: 'weekly' | 'monthly' | 'quarter';
  custom_date_range: string;
  detection_time: string;
  notification_channels: string[];
  template: string;
}

interface TopicUpdate {
  timestamp: string;
  status: 'success' | 'failure';
  ppt_preview_link: string;
}

interface TopicHistory {
  topic_id: number;
  updates: TopicUpdate[];
}

const TopicSettings = () => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopic, setSelectedTopic] = useState<Partial<Topic> | null>(null);
  const [topicHistory, setTopicHistory] = useState<TopicHistory | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isHistoryModalOpen, setIsHistoryModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTopics = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/topics/`);
      if (!response.ok) throw new Error('Failed to fetch topics.');
      const data: Topic[] = await response.json();
      setTopics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTopics();
  }, [fetchTopics]);

  const handleOpenEditModal = (topic: Partial<Topic> | null) => {
    setSelectedTopic(topic ? { ...topic } : {
      name: '',
      keywords: [],
      frequency: 'daily',
      detection_time: '09:00:00',
      notification_channels: ['email'],
      template: 'default',
    });
    setIsEditModalOpen(true);
  };

  const handleCloseEditModal = () => {
    setIsEditModalOpen(false);
    setSelectedTopic(null);
  };

  const handleSaveTopic = async () => {
    if (!selectedTopic) return;

    const method = selectedTopic.id ? 'PUT' : 'POST';
    const url = selectedTopic.id ? `${API_URL}/topics/${selectedTopic.id}` : `${API_URL}/topics/`;
    
    const requestBody = {
      name: selectedTopic.name,
      keywords: selectedTopic.keywords,
      settings: {
        frequency: selectedTopic.frequency,
        custom_date_range: selectedTopic.custom_date_range,
        detection_time: selectedTopic.detection_time,
        notification_channels: selectedTopic.notification_channels,
      },
      ppt_settings: {
        template: selectedTopic.template,
      }
    };

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });
      if (!response.ok) throw new Error('Failed to save topic.');
      handleCloseEditModal();
      fetchTopics(); // Refresh list
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    }
  };

  const handleDeleteTopic = async (topicId: number) => {
    if (window.confirm('Are you sure you want to delete this topic?')) {
      try {
        const response = await fetch(`${API_URL}/topics/${topicId}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to delete topic.');
        fetchTopics(); // Refresh list
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An unknown error occurred.');
      }
    }
  };

  const handleShowHistory = async (topicId: number) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/topics/${topicId}/history`);
      if (!response.ok) throw new Error('Failed to fetch history.');
      const data = await response.json();
      setTopicHistory(data);
      setIsHistoryModalOpen(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setSelectedTopic(prev => prev ? { ...prev, [name]: value } : null);
  };

  const handleArrayChange = (name: 'keywords' | 'notification_channels', value: string) => {
    setSelectedTopic(prev => {
      if (!prev) return null;
      const currentValues = (prev[name] as string[]) || [];
      const newValues = currentValues.includes(value)
        ? currentValues.filter(item => item !== value)
        : [...currentValues, value];
      return { ...prev, [name]: newValues };
    });
  };

  const renderTopicList = () => (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">已有主题</h3>
      <div className="space-y-3">
        {topics.map(topic => (
          <div key={topic.id} className="border border-gray-200 rounded-lg p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
            <div className="flex-1">
              <p className="font-semibold text-gray-800">{topic.name}</p>
              <p className="text-sm text-gray-500 truncate">
                关键词: {topic.keywords.join(', ')}
              </p>
              <p className="text-xs text-gray-400 mt-1">
                上次更新: {new Date(topic.last_updated).toLocaleString()}
              </p>
            </div>
            <div className="flex items-center space-x-2 ml-4">
              <button onClick={() => handleShowHistory(topic.id)} className="p-2 hover:bg-gray-200 rounded-full" title="更新历史"><History className="h-4 w-4 text-gray-600" /></button>
              <button onClick={() => handleOpenEditModal(topic)} className="p-2 hover:bg-gray-200 rounded-full" title="编辑"><Edit className="h-4 w-4 text-gray-600" /></button>
              <button onClick={() => handleDeleteTopic(topic.id)} className="p-2 hover:bg-red-100 rounded-full" title="删除"><Trash2 className="h-4 w-4 text-red-600" /></button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderEditModal = () => {
    if (!isEditModalOpen || !selectedTopic) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b flex justify-between items-center">
            <h2 className="text-xl font-bold text-gray-900">{selectedTopic.id ? '编辑主题' : '新建主题'}</h2>
            <button onClick={handleCloseEditModal} className="p-2 rounded-full hover:bg-gray-100"><X className="h-5 w-5" /></button>
          </div>
          <div className="p-8 space-y-6">
            {/* Basic Info */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">主题名称</label>
              <input type="text" name="name" value={selectedTopic.name} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">关键词 (逗号分隔)</label>
              <input type="text" name="keywords" value={selectedTopic.keywords?.join(', ')} onChange={e => setSelectedTopic({...selectedTopic, keywords: e.target.value.split(',').map(k => k.trim())})} className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>

            {/* Detection Settings */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center"><Bell className="h-5 w-5 mr-2" />检测与通知</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">检测频率</label>
                  <select name="frequency" value={selectedTopic.frequency} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg">
                    <option value="weekly">每周</option>
                    <option value="monthly">每月</option>
                    <option value="quarter">季度</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">检测时间</label>
                  <input type="time" name="detection_time" value={selectedTopic.detection_time} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-2">通知方式</label>
                  <div className="flex space-x-4">
                    {['email', 'wechat', 'sms', 'app'].map(channel => (
                      <label key={channel} className="flex items-center space-x-2">
                        <input type="checkbox" checked={selectedTopic.notification_channels?.includes(channel)} onChange={() => handleArrayChange('notification_channels', channel)} />
                        <span>{channel.charAt(0).toUpperCase() + channel.slice(1)}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* PPT Settings */}
            <div className="border-t pt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center"><FileText className="h-5 w-5 mr-2" />PPT 生成设置</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">PPT 模板</label>
                  <input type="text" name="template" value={selectedTopic.template} onChange={handleInputChange} className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                </div>
              </div>
            </div>
          </div>
          <div className="p-6 bg-gray-50 border-t flex justify-end space-x-3">
            <button onClick={handleCloseEditModal} className="px-4 py-2 border rounded-lg hover:bg-gray-100">取消</button>
            <button onClick={handleSaveTopic} className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2"><Save className="h-4 w-4" /><span>保存</span></button>
          </div>
        </div>
      </div>
    );
  };

  const renderHistoryModal = () => {
    if (!isHistoryModalOpen || !topicHistory) return null;
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
        <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg">
          <div className="p-6 border-b flex justify-between items-center">
            <h2 className="text-xl font-bold text-gray-900">更新历史 (ID: {topicHistory.topic_id})</h2>
            <button onClick={() => setIsHistoryModalOpen(false)} className="p-2 rounded-full hover:bg-gray-100"><X className="h-5 w-5" /></button>
          </div>
          <div className="p-6 max-h-[60vh] overflow-y-auto">
            <ul className="space-y-4">
              {topicHistory.updates.map((update, index) => (
                <li key={index} className="flex items-start space-x-4">
                  <div>
                    {update.status === 'success' 
                      ? <CheckCircle className="h-5 w-5 text-green-500" /> 
                      : <AlertCircle className="h-5 w-5 text-red-500" />}
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-800">
                      {new Date(update.timestamp).toLocaleString()}
                    </p>
                    <p className={`text-sm ${update.status === 'success' ? 'text-green-700' : 'text-red-700'}`}>
                      Status: {update.status}
                    </p>
                    <a href={update.ppt_preview_link} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-600 hover:underline">
                      查看PPT预览
                    </a>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">主题设置</h2>
          <p className="text-gray-600 mt-2">创建和管理您的文献追踪主题</p>
        </div>
        <button onClick={() => handleOpenEditModal(null)} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg flex items-center space-x-2">
          <Plus className="h-5 w-5" />
          <span>新建主题</span>
        </button>
      </div>

      {isLoading && <p>Loading...</p>}
      {error && <p className="text-red-500 bg-red-50 p-3 rounded-lg">{error}</p>}
      
      {renderTopicList()}
      {renderEditModal()}
      {renderHistoryModal()}
    </div>
  );
};

export default TopicSettings;
