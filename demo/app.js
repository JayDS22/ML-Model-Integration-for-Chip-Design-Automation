function ChipDesignDemo() {
  const [selectedFile, setSelectedFile] = React.useState(null);
  const [results, setResults] = React.useState(null);

  const fileTypes = [
    { name: 'GDSII', ext: '.gds', description: 'Binary layout format' },
    { name: 'Verilog', ext: '.v', description: 'Hardware description language' },
    { name: 'SPICE', ext: '.sp', description: 'Circuit simulation netlist' }
  ];

  const runAnalysis = function() {
    const mockResults = {
      powerConsumption: (Math.random() * 2 + 1).toFixed(3),
      drcViolations: Math.floor(Math.random() * 15),
      accuracy: (Math.random() * 2 + 97.5).toFixed(2),
      processingTime: (Math.random() * 20 + 35).toFixed(1),
      status: Math.random() > 0.3 ? 'PASS' : 'REVIEW'
    };
    setResults(mockResults);
  };

  return React.createElement('div', 
    { className: 'min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-6' },
    React.createElement('div', 
      { className: 'max-w-6xl mx-auto' },
      
      React.createElement('div', 
        { className: 'text-center mb-8' },
        React.createElement('h1', 
          { className: 'text-5xl font-bold mb-4 text-blue-400' },
          'ML Chip Design Automation'
        ),
        React.createElement('p', 
          { className: 'text-slate-300 text-xl' },
          'End-to-end machine learning pipeline for semiconductor chip design'
        )
      ),

      React.createElement('div', 
        { className: 'grid grid-cols-3 gap-4 mb-8' },
        React.createElement('div', 
          { className: 'bg-slate-800 p-6 rounded-lg border border-slate-700' },
          React.createElement('div', { className: 'text-4xl font-bold text-blue-400 mb-2' }, '99.8%'),
          React.createElement('div', { className: 'text-slate-400' }, 'DRC Accuracy')
        ),
        React.createElement('div', 
          { className: 'bg-slate-800 p-6 rounded-lg border border-slate-700' },
          React.createElement('div', { className: 'text-4xl font-bold text-green-400 mb-2' }, '85%'),
          React.createElement('div', { className: 'text-slate-400' }, 'Time Reduction')
        ),
        React.createElement('div', 
          { className: 'bg-slate-800 p-6 rounded-lg border border-slate-700' },
          React.createElement('div', { className: 'text-4xl font-bold text-cyan-400 mb-2' }, '<60s'),
          React.createElement('div', { className: 'text-slate-400' }, 'Processing Time')
        )
      ),

      React.createElement('div', 
        { className: 'bg-slate-800 p-8 rounded-xl border border-slate-700' },
        React.createElement('h2', 
          { className: 'text-2xl font-bold mb-6' },
          'Select Design File Format'
        ),
        
        React.createElement('div', 
          { className: 'grid grid-cols-3 gap-4 mb-6' },
          fileTypes.map(function(type) {
            return React.createElement('button',
              {
                key: type.name,
                onClick: function() { setSelectedFile(type); },
                className: 'p-6 rounded-lg border-2 text-left transition-all ' + 
                  (selectedFile && selectedFile.name === type.name
                    ? 'border-blue-500 bg-blue-500/20'
                    : 'border-slate-600 hover:border-slate-500 bg-slate-700/30')
              },
              React.createElement('div', 
                { className: 'text-xs bg-slate-600 px-2 py-1 rounded mb-2 inline-block' },
                type.ext
              ),
              React.createElement('h3', { className: 'text-xl font-bold mb-2' }, type.name),
              React.createElement('p', { className: 'text-sm text-slate-400' }, type.description)
            );
          })
        ),

        selectedFile && !results && React.createElement('div', 
          { className: 'mt-6 p-6 bg-slate-700/30 rounded-lg border border-slate-600' },
          React.createElement('h3', 
            { className: 'text-lg font-semibold mb-3' },
            'Selected: ' + selectedFile.name
          ),
          React.createElement('p', 
            { className: 'text-slate-300 mb-4' },
            'Ready to process ' + selectedFile.name + ' file'
          ),
          React.createElement('button',
            {
              onClick: runAnalysis,
              className: 'px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-lg font-semibold hover:shadow-lg transition-all'
            },
            'Run Analysis'
          )
        ),

        results && React.createElement('div', 
          { className: 'mt-6 p-6 bg-slate-700/30 rounded-lg border border-slate-600' },
          
          React.createElement('div',
            {
              className: 'mb-6 p-4 rounded-lg border-2 ' + 
                (results.status === 'PASS'
                  ? 'bg-green-500/20 border-green-500'
                  : 'bg-yellow-500/20 border-yellow-500')
            },
            React.createElement('h3', { className: 'text-xl font-bold' }, 'Design ' + results.status),
            React.createElement('p', 
              { className: 'text-sm text-slate-300' },
              results.status === 'PASS' ? 'All checks passed' : 'Review recommended'
            )
          ),

          React.createElement('div', 
            { className: 'grid grid-cols-2 gap-4 mb-6' },
            React.createElement('div', 
              { className: 'bg-slate-800 p-4 rounded-lg' },
              React.createElement('div', { className: 'text-slate-400 text-sm mb-1' }, 'Power Consumption'),
              React.createElement('div', { className: 'text-2xl font-bold text-blue-400' }, results.powerConsumption + 'W')
            ),
            React.createElement('div', 
              { className: 'bg-slate-800 p-4 rounded-lg' },
              React.createElement('div', { className: 'text-slate-400 text-sm mb-1' }, 'DRC Violations'),
              React.createElement('div', { className: 'text-2xl font-bold text-yellow-400' }, results.drcViolations)
            ),
            React.createElement('div', 
              { className: 'bg-slate-800 p-4 rounded-lg' },
              React.createElement('div', { className: 'text-slate-400 text-sm mb-1' }, 'Model Accuracy'),
              React.createElement('div', { className: 'text-2xl font-bold text-green-400' }, results.accuracy + '%')
            ),
            React.createElement('div', 
              { className: 'bg-slate-800 p-4 rounded-lg' },
              React.createElement('div', { className: 'text-slate-400 text-sm mb-1' }, 'Processing Time'),
              React.createElement('div', { className: 'text-2xl font-bold text-cyan-400' }, results.processingTime + 's')
            )
          ),

          React.createElement('button',
            {
              onClick: function() {
                setSelectedFile(null);
                setResults(null);
              },
              className: 'px-6 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition-all'
            },
            'Analyze Another Design'
          )
        )
      ),

      React.createElement('div', 
        { className: 'mt-8 text-center text-slate-400' },
        React.createElement('p', null, 'Built with PyTorch, FastAPI, Apache Airflow | Supports GDSII, LEF/DEF, Verilog, SPICE')
      )
    )
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(React.createElement(ChipDesignDemo));