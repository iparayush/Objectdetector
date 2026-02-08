import React from "react";

function ManualPanel({ manual, type }) {
  if (!manual) return (
      <div className="manual placeholder">
          <h3>📘 Smart Manual</h3>
          <p>Waiting for detection...</p>
      </div>
  );

  // Simple Mode (Original Key-Value)
  if (type === "simple") {
    return (
      <div className="manual">
        <h3>📘 Smart Manual</h3>
        {Object.entries(manual).map(([key, value]) => (
          <div key={key} className="manual-item">
            <span className="manual-key">{key.toUpperCase()}:</span>
            <span className="manual-value"> {value}</span>
          </div>
        ))}
      </div>
    );
  }

  // Rich Mode (GoBOLT)
  return (
    <div className="manual rich-manual">
      <h3>🎧 {manual.product_name} Guide</h3>
      
      {/* Images Carousel (Simple grid for now) */}
      <div className="manual-images">
        {manual.images && manual.images.slice(0, 2).map((img, i) => (
          <img key={i} src={img} alt="Product" className="manual-img" />
        ))}
      </div>

      <div className="manual-content">
        {manual.sections && manual.sections.map((section, idx) => (
          <div key={idx} className="manual-section">
            <h4>{section.title}</h4>
            
            {section.type === "list" && (
              <ul>
                {section.content.map((item, i) => <li key={i}>{item}</li>)}
              </ul>
            )}

            {section.type === "steps" && (
              <ol>
                {section.content.map((item, i) => <li key={i}>{item}</li>)}
              </ol>
            )}

            {section.type === "mixed" && (
              <div>
                {section.content.map((sub, i) => (
                  <div key={i} className="sub-section">
                    <strong>{sub.subtitle}</strong>
                    <ul>
                      {sub.details.map((d, j) => <li key={j}>{d}</li>)}
                    </ul>
                  </div>
                ))}
              </div>
            )}

            {section.type === "table" && (
              <table className="manual-table">
                <thead>
                  <tr>
                    {section.headers.map((h, i) => <th key={i}>{h}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {section.rows.map((row, i) => (
                    <tr key={i}>
                      {row.map((cell, j) => <td key={j}>{cell}</td>)}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}

            {section.note && <p className="manual-note">{section.note}</p>}
          </div>
        ))}
      </div>
      
      {manual.ai_summary && (
        <div className="ai-summary">
            <strong>🤖 AI Summary:</strong> {manual.ai_summary}
        </div>
      )}
    </div>
  );
}

export default ManualPanel;
