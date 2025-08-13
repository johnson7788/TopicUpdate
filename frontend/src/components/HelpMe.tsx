import React from 'react';
import { Settings, BarChart3, Presentation, ArrowRight } from 'lucide-react';

const HelpMe = () => {
  const features = [
    {
      title: '监控主题设置',
      description: '这是您工作的起点。在这里，您可以创建、编辑和删除您想要追踪的医学主题。为每个主题设置关键词、监控频率和通知方式，系统将根据您的设定自动为您追踪相关文献。 ',
      icon: <Settings className="h-8 w-8 text-blue-600" />,
      link: 'settings',
    },
    {
      title: '主题文献更新',
      description: '创建主题后，请访问此页面。选择您感兴趣的主题，系统将为您展示最新的文献分析报告，包括文献数量、研究类型分布、发表趋势以及详细的文献列表。 ',
      icon: <BarChart3 className="h-8 w-8 text-green-600" />,
      link: 'literature',
    },
    {
      title: 'PPT推送记录',
      description: '系统会根据您的设置，定期生成分析报告PPT。在此页面，您可以查看所有历史推送记录，并下载已生成的PPT文件，方便您随时回顾和使用。 ',
      icon: <Presentation className="h-8 w-8 text-purple-600" />,
      link: 'ppt',
    },
  ];

  return (
    <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900">欢迎使用 MedBrief Pro</h1>
          <p className="mt-4 text-lg text-gray-600">
            您的专属医学文献情报分析专家。我们致力于将繁琐的文献追踪与分析工作自动化，为您节省宝贵时间。
          </p>
        </div>

        <div className="mb-12">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">核心功能概览</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature) => (
              <div key={feature.title} className="bg-gray-50 p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow">
                <div className="flex items-center justify-center h-16 w-16 rounded-full bg-white shadow-md mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">如何开始使用？</h2>
          <div className="relative">
            {/* Dashed line connector */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gray-200 border-t-2 border-dashed"></div>
            
            <div className="relative grid md:grid-cols-3 gap-8">
              <div className="flex flex-col items-center text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-blue-600 text-white font-bold text-xl border-4 border-white shadow-lg">1</div>
                <h3 className="mt-4 text-lg font-semibold">创建您的第一个主题</h3>
                <p className="mt-1 text-gray-500">前往“监控主题设置”，点击“新建主题”按钮，输入您关心的疾病或药物名称作为关键词。</p>
              </div>
              
              <div className="flex flex-col items-center text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-blue-600 text-white font-bold text-xl border-4 border-white shadow-lg">2</div>
                <h3 className="mt-4 text-lg font-semibold">查看文献分析</h3>
                <p className="mt-1 text-gray-500">系统将自动开始工作。稍后，您可以进入“主题文献更新”页面，查看为您生成的分析报告。</p>
              </div>

              <div className="flex flex-col items-center text-center">
                <div className="flex items-center justify-center h-12 w-12 rounded-full bg-blue-600 text-white font-bold text-xl border-4 border-white shadow-lg">3</div>
                <h3 className="mt-4 text-lg font-semibold">获取分析报告</h3>
                <p className="mt-1 text-gray-500">在“PPT推送记录”中找到您需要的报告，一键下载，即可用于会议汇报或学术交流。</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default HelpMe;
