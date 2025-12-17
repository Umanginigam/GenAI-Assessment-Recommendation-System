import { useState } from "react";
import { fetchRecommendations } from "./api";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    setError("");
    setResults([]);
    if (!query.trim()) {
      setError("Please enter a query or job description.");
      return;
    }
    try {
      setLoading(true);
      const data = await fetchRecommendations(query);
      setResults(data.recommendations || []);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      handleSubmit();
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #e0f2fe 0%, #e0e7ff 50%, #f3e8ff 100%)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '2rem 1rem'
    }}>
      <div style={{ width: '100%', maxWidth: '1200px' }}>
        {/* Header Section */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div style={{
            display: 'inline-block',
            padding: '0.75rem',
            background: 'linear-gradient(135deg, #2563eb, #4f46e5)',
            borderRadius: '1rem',
            marginBottom: '1rem',
            boxShadow: '0 10px 25px rgba(37, 99, 235, 0.3)'
          }}>
            <svg style={{ width: '3rem', height: '3rem', color: 'white' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h1 style={{
            fontSize: '2.5rem',
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #2563eb, #4f46e5)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            marginBottom: '0.75rem'
          }}>
            SHL Assessment Finder
          </h1>
          <p style={{ color: '#6b7280', fontSize: '1.125rem', maxWidth: '48rem', margin: '0 auto' }}>
            Discover the perfect assessments for your hiring needs with AI-powered recommendations
          </p>
        </div>

        {/* Main Card */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: '1rem',
          boxShadow: '0 20px 50px rgba(0, 0, 0, 0.1)',
          padding: '2rem',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{
              display: 'block',
              fontSize: '0.875rem',
              fontWeight: '600',
              color: '#374151',
              marginBottom: '0.75rem'
            }}>
              Job Description or Hiring Query
            </label>
            <textarea
              style={{
                width: '100%',
                border: '2px solid #e5e7eb',
                borderRadius: '0.75rem',
                padding: '1rem',
                fontSize: '0.875rem',
                outline: 'none',
                transition: 'all 0.2s',
                resize: 'none',
                fontFamily: 'inherit'
              }}
              placeholder="e.g., Java developer who works with business teams, needs strong communication skills..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyPress}
              onFocus={(e) => {
                e.target.style.borderColor = '#3b82f6';
                e.target.style.boxShadow = '0 0 0 4px rgba(59, 130, 246, 0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#e5e7eb';
                e.target.style.boxShadow = 'none';
              }}
              rows={6}
            />
            <p style={{ fontSize: '0.75rem', color: '#9ca3af', marginTop: '0.5rem' }}>
              Press Ctrl+Enter to submit
            </p>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            style={{
              width: '100%',
              padding: '1rem 1.5rem',
              borderRadius: '0.75rem',
              color: 'white',
              fontWeight: '600',
              fontSize: '1.125rem',
              background: loading ? '#9ca3af' : 'linear-gradient(135deg, #2563eb, #4f46e5)',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
              boxShadow: loading ? 'none' : '0 10px 25px rgba(37, 99, 235, 0.3)',
              transition: 'all 0.3s',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem'
            }}
            onMouseEnter={(e) => {
              if (!loading) {
                e.target.style.transform = 'scale(1.02)';
                e.target.style.boxShadow = '0 15px 35px rgba(37, 99, 235, 0.4)';
              }
            }}
            onMouseLeave={(e) => {
              if (!loading) {
                e.target.style.transform = 'scale(1)';
                e.target.style.boxShadow = '0 10px 25px rgba(37, 99, 235, 0.3)';
              }
            }}
          >
            {loading ? (
              <>
                <svg style={{ 
                  animation: 'spin 1s linear infinite',
                  height: '1.25rem',
                  width: '1.25rem'
                }} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle style={{ opacity: 0.25 }} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path style={{ opacity: 0.75 }} fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
                Finding Perfect Assessments...
              </>
            ) : (
              <>
                <svg style={{ width: '1.25rem', height: '1.25rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Get Recommendations
              </>
            )}
          </button>

          {error && (
            <div style={{
              marginTop: '1.5rem',
              padding: '1rem',
              background: '#fef2f2',
              borderLeft: '4px solid #ef4444',
              borderRadius: '0.5rem',
              display: 'flex',
              alignItems: 'center'
            }}>
              <svg style={{ width: '1.25rem', height: '1.25rem', color: '#ef4444', marginRight: '0.75rem' }} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p style={{ fontSize: '0.875rem', color: '#b91c1c', fontWeight: '500' }}>{error}</p>
            </div>
          )}

          {results.length > 0 && (
            <div style={{ marginTop: '2rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                <div style={{ padding: '0.5rem', background: '#dcfce7', borderRadius: '0.5rem' }}>
                  <svg style={{ width: '1.5rem', height: '1.5rem', color: '#16a34a' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#1f2937' }}>
                    Recommended Assessments
                  </h2>
                  <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
                    Found {results.length} matching assessment{results.length !== 1 ? 's' : ''}
                  </p>
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {results.map((item, idx) => (
                  <div
                    key={idx}
                    style={{
                      padding: '1.25rem',
                      background: 'linear-gradient(135deg, #f9fafb, #eff6ff)',
                      borderRadius: '0.75rem',
                      border: '2px solid #e5e7eb',
                      transition: 'all 0.3s',
                      cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.borderColor = '#93c5fd';
                      e.currentTarget.style.boxShadow = '0 10px 25px rgba(59, 130, 246, 0.15)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.borderColor = '#e5e7eb';
                      e.currentTarget.style.boxShadow = 'none';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
                      <div style={{ flex: 1, minWidth: '250px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                          <span style={{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            width: '2rem',
                            height: '2rem',
                            background: 'linear-gradient(135deg, #2563eb, #4f46e5)',
                            color: 'white',
                            fontSize: '0.875rem',
                            fontWeight: 'bold',
                            borderRadius: '0.5rem'
                          }}>
                            {idx + 1}
                          </span>
                          <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1f2937' }}>
                            {item.assessment_name}
                          </h3>
                        </div>
                      </div>
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noreferrer"
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '0.5rem',
                          padding: '0.5rem 1rem',
                          background: '#2563eb',
                          color: 'white',
                          borderRadius: '0.5rem',
                          textDecoration: 'none',
                          fontWeight: '500',
                          fontSize: '0.875rem',
                          boxShadow: '0 4px 12px rgba(37, 99, 235, 0.3)',
                          transition: 'all 0.2s'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.background = '#1d4ed8';
                          e.currentTarget.style.transform = 'scale(1.05)';
                          e.currentTarget.style.boxShadow = '0 6px 16px rgba(37, 99, 235, 0.4)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.background = '#2563eb';
                          e.currentTarget.style.transform = 'scale(1)';
                          e.currentTarget.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.3)';
                        }}
                      >
                        View Details
                        <svg style={{ width: '1rem', height: '1rem' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <p style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            Powered by AI-driven talent assessment technology
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;