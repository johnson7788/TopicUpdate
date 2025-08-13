import React, { useState } from 'react';
import Layout from './components/Layout';
import LiteratureAnalysis from './components/LiteratureAnalysis';
import PPTGeneration from './components/PPTGeneration';
import TopicSettings from './components/TopicSettings';
import HelpMe from './components/HelpMe';

function App() {
  const [activeTab, setActiveTab] = useState('helpme');

  const renderContent = () => {
    switch (activeTab) {
      case 'literature':
        return <LiteratureAnalysis />;
      case 'ppt':
        return <PPTGeneration />;
      case 'settings':
        return <TopicSettings />;
      case 'helpme':
        return <HelpMe />;
      default:
        return <HelpMe />;
    }
  };

  return (
    <Layout activeTab={activeTab} onTabChange={setActiveTab}>
      {renderContent()}
    </Layout>
  );
}

export default App;